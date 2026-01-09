import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage
from PySide6.QtGui import QIcon
import pyqtgraph as pg
from ui_form import Ui_MainWindow
from AudioProcessing import AudioFile, AudioConvolver
from AudioPlayback import AudioPlaybackManager, PlaybackArea


def _process(audio_in, ir_in):
    """
    Convolve two audio files and return the resulting output.

    Parameters
    ----------
    audio_in : AudioFile
        The input audio file to be convolved.
    ir_in : AudioFile
        The impulse response audio file used for convolution. Although
        impulse responses are usually short, longer files are permitted.

    Returns
    -------
    AudioFile or None
        The convolved audio file if successful, None otherwise.
    """
    if audio_in.file_path is None or ir_in.file_path is None:
        return None  # No input files loaded
    if audio_in.samplerate == 0 or ir_in.samplerate == 0:
        return None
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


class MainWindow(QMainWindow):
    """
    The main application window for AudioConvolver and its GUI logic.

    This class is responsible for setting up the UI, connecting signals to
    UI widgets, and managing the application's main functionality.

    Attributes
    ----------
    ui: Ui_MainWindow
        UI form object defined in ui_form.py.
    """

    def __init__(self):
        super().__init__()

        # Set up UI from QT Creator and mixer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._playback_manager = AudioPlaybackManager()

        # Connect playback signals
        self._playback_manager.position_updated.connect(self._on_position_updated)
        self._playback_manager.playback_finished.connect(self._on_playback_finished)

        # Maintain copy of signals
        self._audio_input_original = AudioFile()
        self._ir_input_original = AudioFile()
        self._audio_input = AudioFile()
        self._ir_input = AudioFile()
        self._output_audio_original = AudioFile()
        self._output_audio = AudioFile()

        # Set up plot widgets
        _setup_plot_widget(self.ui.InputPeekWidget)
        _setup_plot_widget(self.ui.IRPeekWidget)
        _setup_plot_widget(self.ui.graphicsView)

        # Initialize plot curves and cursors for each area
        self._input_curve = self.ui.InputPeekWidget.plot(pen='b')
        self._input_curve.setClipToView(True)
        self._input_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))

        self._ir_curve = self.ui.IRPeekWidget.plot(pen='b')
        self._ir_curve.setClipToView(True)
        self._ir_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))

        self._output_curve = self.ui.graphicsView.plot(pen='b')
        self._output_curve.setClipToView(True)
        self._output_cursor = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(color='r', width=2))

        self._curves = {
            self.ui.InputPeekWidget: self._input_curve,
            self.ui.IRPeekWidget: self._ir_curve,
            self.ui.graphicsView: self._output_curve
        }

        self._cursors = {
            PlaybackArea.INPUT: self._input_cursor,
            PlaybackArea.IR: self._ir_cursor,
            PlaybackArea.OUTPUT: self._output_cursor,
        }

        self._buttons = {
            PlaybackArea.INPUT: self.ui.inputPlayButton,
            PlaybackArea.IR: self.ui.IRPlayButton,
            PlaybackArea.OUTPUT: self.ui.outputPlayButton
        }

        self._input_audio_files = {
            self._audio_input: self._audio_input_original,
            self._ir_input: self._ir_input_original
        }

        self._icons = {
            "PLAY" : QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart),
            "PAUSE": QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause)
        }

        self._audio_areas = {
            PlaybackArea.INPUT: self._audio_input,
            PlaybackArea.IR: self._ir_input,
            PlaybackArea.OUTPUT: self._output_audio_original
        }

        # Connect signals to UI widgets
        self.ui.inputFileButton.clicked.connect(self._load_input_audio)
        self.ui.inputPlayButton.clicked.connect(self._toggle_input_playback)
        self.ui.inputRestartButton.clicked.connect(self._restart_playback)
        self.ui.inputStopButton.clicked.connect(self._stop_playback)

        self.ui.IRFileButton.clicked.connect(self._load_ir_audio)
        self.ui.IRPlayButton.clicked.connect(self._toggle_ir_playback)
        self.ui.IRRestartButton.clicked.connect(self._restart_playback)
        self.ui.IRStopButton.clicked.connect(self._stop_playback)

        self.ui.outputPlayButton.clicked.connect(self._toggle_output_playback)
        self.ui.outputRestartButton.clicked.connect(self._restart_playback)
        self.ui.outputStopButton.clicked.connect(self._stop_playback)

        self.ui.inputDial.valueChanged.connect(
            lambda x: self._change_inputs_gain(self._audio_input, x))
        self.ui.IRDial.valueChanged.connect(
            lambda x: self._change_inputs_gain(self._ir_input, x))
        self.ui.OutputDial.valueChanged.connect(self._change_output_gain)

        self.ui.clearButton.clicked.connect(self._clear_fields)
        self.ui.saveButton.clicked.connect(self._save_output)

    def _get_audio_for_area(self, area: PlaybackArea):
        if area == PlaybackArea.INPUT:
            return self._audio_input
        elif area == PlaybackArea.IR:
            return self._ir_input
        else:
            return self._output_audio_original

    def _save_output(self):
        if self._audio_input.file_path == "" or self._ir_input.file_path == "":
            return
        AudioConvolver.save_output(self, self._output_audio_original)

    def _toggle_input_playback(self):
        if self._audio_input.file_path == "":
            return
        self._reset_play_icon()
        self._playback_manager.toggle_play_pause(self._audio_input, PlaybackArea.INPUT, self)
        self._toggle_icon(PlaybackArea.INPUT, self.ui.inputPlayButton)

    def _toggle_ir_playback(self):
        if self._ir_input.file_path == "":
            return
        self._reset_play_icon()
        self._playback_manager.toggle_play_pause(self._ir_input, PlaybackArea.IR, self)
        self._toggle_icon(PlaybackArea.IR, self.ui.IRPlayButton)

    def _toggle_output_playback(self):
        if self._audio_input.file_path == "" or self._ir_input.file_path == "":
            return
        self._reset_play_icon()
        self._playback_manager.toggle_play_pause(self._output_audio_original, PlaybackArea.OUTPUT)
        if self._playback_manager.is_playing(PlaybackArea.OUTPUT):
            self.ui.outputPlayButton.setIcon(self._icons.get("PAUSE"))
        else:
            self.ui.outputPlayButton.setIcon(self._icons.get("PLAY"))

    def _toggle_icon(self, playback_area, button):
        if self._playback_manager.is_playing(playback_area):
            button.setIcon(self._icons.get("PAUSE"))
        else:
            button.setIcon(self._icons.get("PLAY"))

    def _reset_play_icon(self):
        self.ui.outputPlayButton.setIcon(self._icons.get("PLAY"))
        self.ui.IRPlayButton.setIcon(self._icons.get("PLAY"))
        self.ui.inputPlayButton.setIcon(self._icons.get("PLAY"))

    def _stop_playback(self):
        curr_area = self._playback_manager.get_current_area()
        if curr_area is None:
            return
        cursor = self._cursors.get(curr_area)
        self._reset_play_icon()
        self._playback_manager.stop(curr_area)
        cursor.setValue(0)

    def _restart_playback(self):
        curr_file = self._playback_manager.get_current_audio()
        curr_area = self._playback_manager.get_current_area()
        self._stop_playback()
        self._playback_manager.toggle_play_pause(curr_file, curr_area, self)
        self._toggle_icon(curr_area, self._buttons.get(curr_area))

    def _on_position_updated(self, area: PlaybackArea, position: float):
        cursor = self._cursors.get(area)
        audio = self._get_audio_for_area(area)
        if not cursor or not audio or audio.data.size == 0:
            return
        duration = len(audio.data) / audio.samplerate
        position = max(0.0, min(position, duration))
        cursor.setValue(position)

    def _on_playback_finished(self, area: PlaybackArea):
        cursor = self._cursors.get(area)
        if cursor:
            cursor.setValue(0)

    def _clear_fields(self):
        self._playback_manager.stop_all()
        self._audio_input_original.clear()
        self._ir_input_original.clear()
        self._audio_input.clear()
        self._ir_input.clear()
        self._output_audio_original.clear()
        self.ui.inputFileDisplay.setPlainText("")
        self.ui.IRFileDisplay.setPlainText("")
        self._reset_play_icon()

        # Delete all waveforms and cursors
        for (widget, curve), (_, cursor) in zip(self._curves.items(), self._cursors.items()):
            widget.removeItem(cursor)
            if curve.getData() is not None:
                curve.setData([])

    def _load_input_audio(self):
        self._audio_input.load_file(self._audio_input_original)
        self._display_waveform(self._input_curve, self._audio_input.data,
                               self._audio_input.samplerate)
        self.ui.InputPeekWidget.addItem(self._input_cursor)

        """Temp area to test uninterrupted output playback"""
        curr_area = self._playback_manager.get_current_area()
        if curr_area is PlaybackArea.INPUT or curr_area is PlaybackArea.IR:
            self._playback_manager.stop(curr_area)

        # self._playback_manager.stop_all()
        if self._audio_input.samplerate > 0 and self._ir_input.samplerate > 0:
            self._convolve()
        file_path = self._audio_input.file_path
        if file_path != "":
            file_path = file_path.split("/")[-1]
        self.ui.inputFileDisplay.setPlainText(file_path)

    def _load_ir_audio(self):
        self._ir_input.load_file(self._ir_input_original)
        self._display_waveform(self._ir_curve, self._ir_input.data, self._ir_input.samplerate)
        self.ui.IRPeekWidget.addItem(self._ir_cursor)
        self._playback_manager.stop_all()
        if self._audio_input.samplerate > 0 and self._ir_input.samplerate > 0:
            self._convolve()
        file_path = self._ir_input.file_path
        if file_path != "":
            file_path = file_path.split("/")[-1]
        self.ui.IRFileDisplay.setPlainText(file_path)

    def _change_inputs_gain(self, audio_file: AudioFile, db_val: int = 0):
        """
        Adjust the input gain and update the input waveform.

        If both inputs are loaded, re-convolve the output.
        """

        if db_val == 0:
            self._input_audio_files[audio_file].copy_data(audio_file)
        else:
            audio_file.adjust_gain(self._input_audio_files[audio_file], db_val)
        if audio_file is self._audio_input:
            self._display_waveform(self._input_curve, self._audio_input.data,
                                   self._audio_input.samplerate)
            if self._playback_manager.is_playing(PlaybackArea.INPUT):
                self._playback_manager.update_audio(self._audio_input, PlaybackArea.INPUT)
        else:
            self._display_waveform(self._ir_curve, self._ir_input.data, self._ir_input.samplerate)
            if self._playback_manager.is_playing(PlaybackArea.IR):
                self._playback_manager.update_audio(self._ir_input, PlaybackArea.IR)

        if self._audio_input.samplerate > 0 and self._ir_input.samplerate > 0:
            self._convolve()

    def _change_output_gain(self, db_val: int = 0):
        """Adjust the output gain and update the output waveform."""

        if db_val == 0:
            self._output_audio_original.copy_data(self._output_audio)
        else:
            self._output_audio.adjust_gain(self._output_audio_original, db_val)

            if self._playback_manager.is_playing(PlaybackArea.OUTPUT):
                curr_area = self._playback_manager.get_current_area()
                curr_audio = self._get_audio_for_area(curr_area)
                self._playback_manager.update_audio(curr_audio, curr_area)
        self._display_waveform(self._output_curve, self._output_audio.data,
                               self._output_audio.samplerate)

    def _convolve(self):
        """Trigger convolution, save the output, and display its waveform."""

        self._output_audio_original = _process(self._audio_input, self._ir_input)
        if self._output_audio_original is not None:
            self._output_audio_original.copy_data(self._output_audio)
        self._display_waveform(self._output_curve, self._output_audio_original.data,
                               self._output_audio_original.samplerate)
        self.ui.graphicsView.addItem(self._output_cursor)

        if self._playback_manager.is_playing(PlaybackArea.OUTPUT):
            self._playback_manager.update_audio(self._output_audio_original, PlaybackArea.OUTPUT)

    @staticmethod
    def _display_waveform(curve, audio_data, samplerate):
        """
        Display a waveform in a plot widget.

        The waveform is downsampled by a factor of 30 to improve
        performance, and the amplitude is normalized to -1 to 1.
        """

        if audio_data.size == 0:
            return
        if audio_data.ndim == 1:
            data = audio_data
        else:
            data = audio_data[:, 0]
        duration = len(data) / samplerate

        # Normalize to -1 to 1
        max_val = np.max(np.abs(data))
        if max_val > 1:
            data = data / max_val

        time_axis = np.linspace(0, duration, len(data))
        curve.setData(time_axis, data)
        curve.setDownsampling(ds=30, method='mean')
        plot_widget = curve.getViewBox()
        plot_widget.setYRange(-1, 1, padding=0)
        curve.updateItems()

    def closeEvent(self, event):
        """
        Cleanup resources when the window is closed.

        Overrides QMainWindow.closeEvent() to additionally clean up the
        playback manager and pygame mixer.
        """

        self._playback_manager.cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
