"""Audio playback manager."""

import pygame
import soundfile as sf
import tempfile
import os
from PySide6.QtWidgets import QErrorMessage
from PySide6.QtCore import QObject, Signal, QTimer
from enum import Enum, auto


class PlaybackArea(Enum):
    INPUT = auto()
    IR = auto()
    OUTPUT = auto()


class PlaybackState:
    def __init__(self):
        self.position = 0.0
        self.is_paused = False
        self.is_stopped = True
        self.temp_file = None

    def reset(self):
        self.position = 0.0
        self.is_paused = False
        self.temp_file = None

    def cleanup_temp_file(self):
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except Exception as e:
                print(f"Error removing temporary file: {e}")
            self.temp_file = None


class AudioPlaybackManager(QObject):
    position_updated = Signal(PlaybackArea, float)
    playback_finished = Signal(PlaybackArea)

    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        # Track the playback state for each playback area
        self._states = {
            PlaybackArea.INPUT: PlaybackState(),
            PlaybackArea.IR: PlaybackState(),
            PlaybackArea.OUTPUT: PlaybackState()
        }
        self._current_area = None
        self._current_audio = None

        # Timer to update the playback position
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._update_position)
        self._update_timer.setInterval(50)
        self._session_offset_sec = 0.0
        self.duration = 0.0

    def get_current_area(self):
        return self._current_area

    def get_current_audio(self):
        return self._current_audio

    def play(self, audio_file, area: PlaybackArea, parent=None):
        if audio_file is None or audio_file.data.size == 0:
            QErrorMessage(parent).showMessage("No audio to play.")
            return
        state = self._states[area]

        # If this area was paused, resume from saved position
        if state.is_paused and self._current_area == area:
            self._resume(area)
            return

        # Stop any current playback and save its position
        self._stop_and_save_position()

        # Prepare new playback
        try:
            # Create temp file if needed
            if not state.temp_file or not os.path.exists(state.temp_file):
                temp_fd, state.temp_file = tempfile.mkstemp(suffix='.wav')
                os.close(temp_fd)
                sf.write(state.temp_file, audio_file.data, audio_file.samplerate)
            pygame.mixer.music.load(state.temp_file)

            # Start from saved position (convert to milliseconds)
            start_pos = state.position if state.is_paused else 0.0
            pygame.mixer.music.play(start=start_pos)
            self._session_offset_sec = start_pos

            self._current_area = area
            self._current_audio = audio_file
            state.is_paused = False

            # Start position update timer
            QTimer.singleShot(50, self._start_updates)

        except Exception as e:
            QErrorMessage(parent).showMessage(str(e))

    def pause(self, area: PlaybackArea = None):
        if area is None:
            area = self._current_area
        if area is None or self._current_area != area:
            return

        if pygame.mixer.music.get_busy():
            state = self._states[area]
            # Save current position before pausing
            state.position = self._get_playback_position()
            state.is_paused = True
            pygame.mixer.music.pause()
            self._update_timer.stop()

    def toggle_play_pause(self, audio_file, area: PlaybackArea, parent=None):
        if self._current_area == area and pygame.mixer.music.get_busy():
            self.pause(area)
        else:
            self.play(audio_file, area, parent)

    def stop(self, area: PlaybackArea):
        """Stop playback in a playback area and reset position to 0."""
        if area is not None:
            state = self._states[area]
            state.reset()

        if self._current_area == area:
            pygame.mixer.music.stop()
            self._update_timer.stop()
            self._current_area = None
            self._current_audio = None
            self._session_offset_sec = 0.0

    def stop_all(self):
        pygame.mixer.music.stop()
        self._update_timer.stop()
        for state in self._states.values():
            state.reset()
        self._current_area = None
        self._current_audio = None
        self._session_offset_sec = 0.0

    def is_playing(self, area: PlaybackArea = None) -> bool:
        if area is None:
            return pygame.mixer.music.get_busy()
        return self._current_area == area and pygame.mixer.music.get_busy()

    def get_current_area(self) -> PlaybackArea:
        return self._current_area

    def _get_playback_position(self) -> float:
        if self._current_area is None:
            return 0.0
        state = self._states[self._current_area]
        if state.is_paused:
            return state.position
        if pygame.mixer.music.get_busy():
            return self._session_offset_sec + (pygame.mixer.music.get_pos() / 1000.0)
        return state.position

    def _resume(self, area: PlaybackArea):
        pygame.mixer.music.unpause()
        self._states[area].is_paused = False
        self._start_updates()

    def _stop_and_save_position(self):
        if self._current_area is not None and pygame.mixer.music.get_busy():
            state = self._states[self._current_area]
            state.position = self._get_playback_position()
            state.is_paused = True
            pygame.mixer.music.stop()
            self._update_timer.stop()

    def _start_updates(self):
        if not self._update_timer.isActive():
            self._update_timer.start()

    def _update_position(self):
        if self._current_area is None:
            self._update_timer.stop()
            return
        if pygame.mixer.music.get_busy():
            position = self._get_playback_position()
            self.position_updated.emit(self._current_area, position)
        else:
            # Playback finished naturally
            self._update_timer.stop()
            self._states[self._current_area].reset()
            self.playback_finished.emit(self._current_area)
            self._current_area = None
            self._current_audio = None

    def cleanup(self):
        self.stop_all()
        for state in self._states.values():
            state.cleanup_temp_file()
        pygame.mixer.quit()