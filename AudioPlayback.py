"""Audio playback manager.

Portions of this file are adapted from the sounddevice examples
https://github.com/spatialaudio/python-sounddevice
#
Copyright (c) 2015–2024
Pauli Virtanen, Matthias Geier, and contributors
Licensed under the MIT License
"""

import threading
import time
import numpy as np
import queue as q
import sounddevice as sd
import soundfile as sf
from PySide6.QtCore import QObject, Signal, QTimer, QMetaObject, Qt
from enum import Enum, auto


class PlaybackArea(Enum):
    INPUT = auto()
    IR = auto()
    OUTPUT = auto()


class AreaManager:
    """
    The current state of audio playback for a specific area_manager.

    Attributes
    ----------
    position : float
        The current playback position in seconds.
    is_paused : bool
        Whether playback is currently paused.
    is_stopped : bool
        Whether playback has been stopped.
    """

    def __init__(self, area):
        self.position = 0.0
        self.is_paused = False
        self.is_stopped = True
        self.output_stream = None
        self.area = area
        self.sound_file = None
        self.fill_thread = None  # Thread for filling the queue
        self.start_time = 0.0
        self.curr_time = 0.0
        self.duration = 0.0
        self.finished_naturally = False
        self.pause_start_time = None
        self.audio_file = None
        self.gain_change = 0
        self.q = PlaybackQueue(1024, 20, self)

    def reset(self):
        self.position = 0.0
        self.is_paused = False
        self.is_stopped = True
        self.pause_start_time = None
        self.audio_file = None
        self.duration = 0.0
        self.gain_change = 0
        if self.output_stream is not None:
            self.output_stream.abort()
            self.output_stream.close()
            self.output_stream = None
        if self.sound_file is not None:
            self.sound_file.close()
            self.sound_file = None
        if self.fill_thread is not None:
            self.q.stop_fill_thread()
            self.q.clear_queue()
            self.fill_thread.join(timeout=0.5)
            self.fill_thread = None

    def callback(self, outdata, frames, time, status):
        """
        Callback function for sounddevice playback.

        Credit: https://github.com/spatialaudio/python-sounddevice/blob/master/examples/playraw.py
        """

        if status.output_underflow:
            print("Output underflow. Increase blocksize?")
            raise sd.CallbackAbort
        assert not status
        if self.is_paused:
            outdata.fill(0)
            return
        try:
            data = self.q.queue.get_nowait()
        except q.Empty as e:
            print("Buffer is empty. Increase buffersize?")
            raise sd.CallbackStop from e
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):].fill(0)
            raise sd.CallbackStop
        else:
            outdata[:] = data


class PlaybackQueue:
    def __init__(self, blocksize, buffersize, area_manager: AreaManager):
        super().__init__()
        self.blocksize = blocksize
        self.buffersize = buffersize
        self.area_manager = area_manager
        self.stop_fill = False
        self.queue = q.Queue(maxsize=self.buffersize)

    def fill_queue(self):
        """Background thread to fill the audio queue."""
        try:
            while not self.stop_fill and self.area_manager.sound_file is not None:
                data = self.area_manager.sound_file.read(self.blocksize, always_2d=True)
                if len(data) == 0:
                    break
                if self.area_manager.gain_change != 0:
                    data *= 10 ** (self.area_manager.gain_change / 20)
                    data = np.clip(data, a_min=-1.0, a_max=1.0)
                try:
                    timeout = self.blocksize * self.buffersize / self.area_manager.sound_file.samplerate
                    self.queue.put(data, timeout=timeout)
                except q.Full:
                    if self.stop_fill:
                        break
                    continue
        except Exception as e:
            print(f"Error filling queue: {e}")

    def clear_queue(self):
        self.stop_fill = True
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except q.Empty:
                break
        self.stop_fill = False

    def stop_fill_thread(self):
        self.stop_fill = True


class AudioPlaybackManager(QObject):
    position_updated = Signal(PlaybackArea, float)
    playback_finished = Signal(PlaybackArea)
    _int_stream_finished = Signal(object)

    def __init__(self):
        super().__init__()

        self._current_area = None
        self._curr_area_manager = None
        self._current_audio = None
        self.input_area = AreaManager(PlaybackArea.INPUT)
        self.ir_area = AreaManager(PlaybackArea.IR)
        self.output_area = AreaManager(PlaybackArea.OUTPUT)

        self._int_stream_finished.connect(self._handle_stream_finished)

        # Track the playback state for each playback area_manager
        self._area_managers = {
            PlaybackArea.INPUT: self.input_area,
            PlaybackArea.IR: self.ir_area,
            PlaybackArea.OUTPUT: self.output_area
        }

        # Timer to update the playback position
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_position2)
        self._update_timer.setInterval(50)
        self._session_offset_sec = 0.0
        self.duration = 0.0
        self.stop_fill_thread = False

    def get_current_area(self):
        return self._current_area

    def get_current_area_manager(self):
        return self._curr_area_manager

    def get_current_audio(self):
        return self._current_audio

    def _play2(self, audio_file, area_manager: AreaManager, parent=None):
        if audio_file is None or audio_file.data.size == 0:
            return

        if area_manager.is_paused and self._current_area == area_manager.area:
            self._resume2(area_manager)
            return

        pos = area_manager.position if area_manager.is_paused else 0.0
        self._session_offset_sec = pos
        area_manager.audio_file = audio_file

        try:
            if audio_file.file_path == "":
                sf.write("output.flac", audio_file.data, audio_file.samplerate,
                                audio_file.channels, endian="FILE")
                area_manager.sound_file = sf.SoundFile("output.flac")

            else:
                area_manager.sound_file = sf.SoundFile(audio_file.file_path)
            f = area_manager.sound_file

            area_manager.duration = len(audio_file.data) / audio_file.samplerate

            if pos > 0:
                seek_frame = int(pos * f.samplerate)
                f.seek(seek_frame)

            # Pre-fill the queue with 1 buffer's worth of data
            for _ in range(area_manager.q.buffersize):
                data = f.read(area_manager.q.blocksize, always_2d=True)
                if not len(data):
                    break
                if data.ndim == 1:
                    data = data.reshape(-1, f.channels)
                area_manager.q.queue.put_nowait(data)

            area_manager.finished_naturally = True

            self.current_area_manager = area_manager
            area_manager.output_stream = sd.OutputStream(
                samplerate=f.samplerate,
                blocksize=area_manager.q.blocksize,
                channels=f.channels,
                callback=area_manager.callback,
                finished_callback=lambda: self._stream_finished(area_manager)
            )
            area_manager.output_stream.start()

            # Start background thread to fill queue
            area_manager.q.stop_fill = False
            area_manager.fill_thread = threading.Thread(
                target=area_manager.q.fill_queue, daemon=True)
            area_manager.fill_thread.start()
            self._curr_area_manager = area_manager
            self._current_area = area_manager.area
            self._current_audio = audio_file
            area_manager.is_paused = False
            area_manager.is_stopped = False
            area_manager.start_time = time.time() - pos
            area_manager.curr_time = pos
            # self._start_updates()
            QTimer.singleShot(50, self._start_updates)

        except Exception as e:
            print(f"Error during playback: {e}")

    def _stream_finished(self, area_manager: AreaManager):
        if area_manager.finished_naturally:
            self._int_stream_finished.emit(area_manager)
        area_manager.finished_naturally = False

    def _handle_stream_finished(self, area_manager: AreaManager):
        self.stop2(area_manager.area)

    def _pause2(self, area_manager: AreaManager = None):
        if area_manager is None:
            if self._current_area is None:
                return
            area_manager = self._area_managers[self._current_area]

        if self._current_area != area_manager.area:
            return

        if area_manager.output_stream is None:
            return

        if area_manager.output_stream is not None and area_manager.output_stream.active:
            # Save the current playback position
            pos = self._get_playback_position2(area_manager)
            area_manager.position = pos
            area_manager.curr_time = pos
            area_manager.is_paused = True
            area_manager.pause_start_time = time.time()

            # Stop the fill thread
            area_manager.q.stop_fill = True
            area_manager.q.clear_queue()
            area_manager.finished_naturally = False
            area_manager.output_stream.abort()
            if area_manager.output_stream is not None:
                area_manager.output_stream.close()
            area_manager.output_stream = None

            if area_manager.sound_file is not None:
                area_manager.sound_file.close()
                area_manager.sound_file = None
            self._update_timer.stop()

    def toggle_play_pause2(self, audio_file, area_manager: AreaManager):
        if area_manager.output_stream is not None and area_manager.output_stream.active:
            self._pause2(area_manager)
        elif area_manager.output_stream is None:
            self._play2(audio_file, area_manager)

    def stop2(self, area: AreaManager) -> None:
        if isinstance(area, AreaManager):
            area_manager = area
            area = area_manager.area
        else:
            area_manager = self._area_managers[area]

        area_manager.q.stop_fill = True
        if area_manager.output_stream is not None:
            self._update_timer.stop()
        if self._current_area == area:
            self._current_area = None
            self._current_audio = None
        self._session_offset_sec = 0.0
        area_manager.reset()
        area_manager.q.clear_queue()
        self.playback_finished.emit(area)

    def stop_all2(self) -> None:
        self.stop2(self.input_area)
        self.stop2(self.ir_area)
        self.stop2(self.output_area)

    def is_playing2(self, area) -> bool:
        if isinstance(area, PlaybackArea):
            area_manager = self._area_managers.get(area)
        else:
            area_manager = area
        return area_manager.output_stream is not None and area_manager.output_stream.active

    def _get_playback_position2(self, area_manager: AreaManager) -> float:
        if self._current_area is None or self._current_area != area_manager.area:
            return 0.0

        if area_manager.is_paused:
            # Return saved position when paused
            return area_manager.position

        curr_pos = time.time() - area_manager.start_time
        if area_manager.duration:
            curr_pos = min(curr_pos, area_manager.duration)
        return curr_pos

    def _resume2(self, area_manager: AreaManager):
        audio = area_manager.audio_file
        if audio is None:
            return

        try:
            # Reopen the sound file and seek to saved position
            area_manager.sound_file = sf.SoundFile(audio.file_path)
            f = area_manager.sound_file

            seek_frame = int(area_manager.position * f.samplerate)
            f.seek(seek_frame)

            self._session_offset_sec = area_manager.position

            area_manager.q.clear_queue()
            for _ in range(area_manager.q.buffersize):
                data = f.read(area_manager.q.blocksize, always_2d=True)
                if not len(data):
                    break
                area_manager.q.queue.put_nowait(data)

            area_manager.output_stream = sd.OutputStream(
                samplerate=f.samplerate,
                blocksize=area_manager.q.blocksize,
                channels=f.channels,
                callback=area_manager.callback,
                finished_callback=lambda: self._stream_finished(area_manager)
            )
            area_manager.output_stream.start()

            area_manager.q.stop_fill = False
            area_manager.fill_thread = threading.Thread(
                target=area_manager.q.fill_queue, daemon=True)
            area_manager.fill_thread.start()

            area_manager.is_paused = False
            area_manager.is_stopped = False
            self._curr_area_manager = area_manager
            self._current_area = area_manager.area
            self._current_audio = audio
            area_manager.start_time = time.time() - area_manager.position
            self._start_updates()
        except Exception as e:
            print(f"Error resuming playback: {e}")

    def _stop_and_save_position2(self, area_manager: AreaManager = None):
        if self._current_area is None:
            return

        if area_manager is None:
            area_manager = self._area_managers[self._current_area]

        if area_manager.output_stream is not None and area_manager.output_stream.active:
            # Save position before stopping
            pos = self._get_playback_position2(area_manager)
            area_manager.position = pos
            area_manager.curr_time = pos
            area_manager.is_paused = True

            # Stop fill thread
            area_manager.q.stop_fill = True
            if area_manager.fill_thread is not None:
                area_manager.fill_thread.join(timeout=1.0)

            # Stop stream
            area_manager.q.clear_queue()
            area_manager.output_stream.abort()
            area_manager.output_stream.close()
            area_manager.output_stream = None

            # Close file
            if area_manager.sound_file is not None:
                area_manager.sound_file.close()
                area_manager.sound_file = None
            self._update_timer.stop()

    def _start_updates(self):
        if not self._update_timer.isActive():
            self._update_timer.start()

    def _update_position2(self):
        if self._current_area is None:
            self._update_timer.stop()
            return
        area_manager = self._area_managers[self._current_area]
        if area_manager.output_stream is not None and area_manager.output_stream.active:
            position = self._get_playback_position2(area_manager)
            area_manager.curr_time = position
            self.position_updated.emit(self._current_area, position)
        else:
            self._update_timer.stop()

    def cleanup(self):
        self.stop_all2()
