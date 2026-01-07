import enum

import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
import pyqtgraph as pg
from ui_form import Ui_MainWindow
from audio_processing import AudioFile, AudioConvolver
from AudioPlayback import AudioPlaybackManager, PlaybackArea
from enum import Enum, auto


class ButtonIcons:
    PLAY = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart)
    PAUSE = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause)


def process(audio_in, ir_in):
    if audio_in.file_path is None or ir_in.file_path is None:
        return None  # No input files loaded
    try:
        convolver = AudioConvolver(audio_in, ir_in)
        output_audio = convolver.convolve(audio_in, ir_in)
        return output_audio
    except AssertionError as e:
        QErrorMessage(parent=None).showMessage(str(e))
        return None


def _setup_plot_widget(plot_widget):
    plot_widget.showGrid(x=False, y=False)
    plot_widget.hideAxis('left')
    plot_widget.hideAxis('bottom')


### Main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up UI from QT Creator and mixer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.playback_manager = AudioPlaybackManager()

        # Connect playback signals
        self.playback_manager.position_updated.connect(self._on_position_updated)
        self.playback_manager.playback_finished.connect(self._on_playback_finished)

        # Maintain copy of signals
        self._audio_input_original = AudioFile()
        self._ir_input_original = AudioFile()
        self.audio_input = AudioFile()
        self.ir_input = AudioFile()
        self._output_audio = AudioFile()

        # Set up plot widgets
        _setup_plot_widget(self.ui.InputPeekWidget)
        _setup_plot_widget(self.ui.IRPeekWidget)
        _setup_plot_widget(self.ui.graphicsView)

        # Initialize plot curves and cursors for each area
        self.input_curve = self.ui.InputPeekWidget.plot(pen='b')
        self.input_curve.setClipToView(True)
        self.input_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))


        self.ir_curve = self.ui.IRPeekWidget.plot(pen='b')
        self.ir_curve.setClipToView(True)
        self.ir_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))


        self.output_curve = self.ui.graphicsView.plot(pen='b')
        self.output_curve.setClipToView(True)
        self.output_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))


        # Map areas to their cursors
        self._cursors = {
            PlaybackArea.INPUT: self.input_cursor,
            PlaybackArea.IR: self.ir_cursor,
            PlaybackArea.OUTPUT: self.output_cursor,
        }

        # Connect signals to UI widgets
        self.ui.inputFileButton.clicked.connect(self.load_input_audio)
        self.ui.IRFileButton.clicked.connect(self.load_ir_audio)
        self.ui.outputPlayButton.clicked.connect(self._toggle_output_playback)
        self.ui.inputPlayButton.clicked.connect(self._toggle_input_playback)
        self.ui.IRPlayButton.clicked.connect(self._toggle_ir_playback)
        self.ui.clearButton.clicked.connect(self.clear_inputs)


    def _toggle_icon(self, playback_area, button):
        if self.playback_manager.is_playing(playback_area):
            button.setIcon(ButtonIcons.PAUSE)
        else:
            button.setIcon(ButtonIcons.PLAY)
        return


    def _toggle_input_playback(self):
        if self.audio_input.file_path == "":
            return
        self.playback_manager.toggle_play_pause(self.audio_input, PlaybackArea.INPUT, self)
        self._toggle_icon(PlaybackArea.INPUT, self.ui.inputPlayButton)

    def _toggle_ir_playback(self):
        if self.ir_input.file_path == "":
            return
        self.playback_manager.toggle_play_pause(self.ir_input, PlaybackArea.IR, self)
        self._toggle_icon(PlaybackArea.IR, self.ui.IRPlayButton)

    def _toggle_output_playback(self):
        if self.audio_input.file_path == "" or self.ir_input.file_path == "":
            return
        self.playback_manager.toggle_play_pause(self._output_audio, PlaybackArea.OUTPUT, self)
        if self.playback_manager.is_playing(PlaybackArea.OUTPUT):
            self.ui.outputPlayButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        else:
            self.ui.outputPlayButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))


    def _on_position_updated(self, area: PlaybackArea, position: float):
        cursor = self._cursors.get(area)
        audio_map = {PlaybackArea.INPUT: self.audio_input,
                     PlaybackArea.IR: self.ir_input,
                     PlaybackArea.OUTPUT: self._output_audio}
        audio = audio_map.get(area)
        if not cursor or not audio or audio.data.size == 0:
            return
        duration = len(audio.data) / audio.samplerate
        position = max(0.0, min(position, duration))

        cursor.setValue(position)

    def _on_playback_finished(self, area: PlaybackArea):
        cursor = self._cursors.get(area)
        if cursor:
            cursor.setValue(0)

    def clear_inputs(self):
        self.playback_manager.stop_all()
        self._audio_input_original.clear()
        self._ir_input_original.clear()
        self.audio_input.clear()
        self.ir_input.clear()
        self._output_audio.clear()
        # Reset all cursors
        for cursor in self._cursors.values():
            cursor.setValue(0)

    def load_input_audio(self):
        self.audio_input.load_file(self._audio_input_original)
        self.display_waveform(self.input_curve, self.audio_input.data,
                              self.audio_input.samplerate)
        self.ui.InputPeekWidget.addItem(self.input_cursor)
        # if getattr(self, "ir_input", None) is not None:
        #     self.convolve()

    def load_ir_audio(self):
        self.ir_input.load_file(self._ir_input_original)
        self.display_waveform(self.ir_curve, self.ir_input.data, self.ir_input.samplerate)
        self.ui.IRPeekWidget.addItem(self.ir_cursor)
        if getattr(self, "audio_input", None) is not None:
            self.convolve()

    def convolve(self):
        self._output_audio = process(self.audio_input, self.ir_input)
        self.display_waveform(self.output_curve, self._output_audio.data,
                              self._output_audio.samplerate)
        self.ui.graphicsView.addItem(self.output_cursor)

    # def start_audio_playback(self):
    #     self.playback_manager.play_output_audio(self._output_audio, self)

    def display_waveform(self, curve, audio_data, samplerate):
        if audio_data.size == 0:
            return
        data = audio_data[:, 0]
        duration = len(data) / samplerate

        # Normalize to -1 to 1
        max_val = np.max(np.abs(data))
        if max_val > 1:
            data = data / max_val

        time_axis = np.linspace(0, duration, len(data))
        curve.setData(time_axis, data)
        curve.setDownsampling(ds=30, method='mean')
        curve.updateItems()

    def closeEvent(self, event):
        self.playback_manager.cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()