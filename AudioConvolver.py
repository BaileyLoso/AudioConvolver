import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QErrorMessage
from PySide6.QtGui import QIcon
import pyqtgraph as pg
from ui_form import Ui_MainWindow
from audio_processing import AudioFile, AudioConvolver
from AudioPlayback import AudioPlaybackManager, PlaybackArea


class ButtonIcons:
    PLAY = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart)
    PAUSE = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause)


def process(audio_in, ir_in):
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
        self.output_audio_copy = AudioFile()

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

        self._curves = {
            self.ui.InputPeekWidget: self.input_curve,
            self.ui.IRPeekWidget: self.ir_curve,
            self.ui.graphicsView: self.output_curve
        }

        # Map areas to their cursors
        self._cursors = {
            PlaybackArea.INPUT: self.input_cursor,
            PlaybackArea.IR: self.ir_cursor,
            PlaybackArea.OUTPUT: self.output_cursor,
        }

        self._buttons = {
            PlaybackArea.INPUT: self.ui.inputPlayButton,
            PlaybackArea.IR: self.ui.IRPlayButton,
            PlaybackArea.OUTPUT: self.ui.outputPlayButton
        }

        self._input_audio_files = {
            self.audio_input: self._audio_input_original,
            self.ir_input: self._ir_input_original
        }


        # Connect signals to UI widgets
        self.ui.inputFileButton.clicked.connect(self.load_input_audio)
        self.ui.IRFileButton.clicked.connect(self.load_ir_audio)
        self.ui.outputPlayButton.clicked.connect(self._toggle_output_playback)
        self.ui.inputPlayButton.clicked.connect(self._toggle_input_playback)
        self.ui.IRPlayButton.clicked.connect(self._toggle_ir_playback)
        self.ui.clearButton.clicked.connect(self.clear_fields)
        self.ui.saveButton.clicked.connect(self.save_output)
        self.ui.inputStopButton.clicked.connect(self.stop_playback)
        self.ui.IRStopButton.clicked.connect(self.stop_playback)
        self.ui.outputStopButton.clicked.connect(self.stop_playback)
        self.ui.inputRestartButton.clicked.connect(self.restart_playback)
        self.ui.IRRestartButton.clicked.connect(self.restart_playback)
        self.ui.outputRestartButton.clicked.connect(self.restart_playback)
        self.ui.inputDial.valueChanged.connect(lambda x: self.change_input_gain(self.audio_input, x))
        self.ui.IRDial.valueChanged.connect(lambda x: self.change_input_gain(self.ir_input, x))
        self.ui.OutputDial.valueChanged.connect(self.change_output_gain)


    def save_output(self):
        if self.audio_input.file_path == "" or self.ir_input.file_path == "":
            return
        AudioConvolver.save_output(self._output_audio)

    def _toggle_input_playback(self):
        if self.audio_input.file_path == "":
            return
        self._reset_play_icon()
        self.playback_manager.toggle_play_pause(self.audio_input, PlaybackArea.INPUT, self)
        self._toggle_icon(PlaybackArea.INPUT, self.ui.inputPlayButton)


    def _toggle_ir_playback(self):
        if self.ir_input.file_path == "":
            return
        self._reset_play_icon()
        self.playback_manager.toggle_play_pause(self.ir_input, PlaybackArea.IR, self)
        self._toggle_icon(PlaybackArea.IR, self.ui.IRPlayButton)


    def _toggle_output_playback(self):
        if self.audio_input.file_path == "" or self.ir_input.file_path == "":
            return
        self._reset_play_icon()
        self.playback_manager.toggle_play_pause(self._output_audio, PlaybackArea.OUTPUT, self)
        if self.playback_manager.is_playing(PlaybackArea.OUTPUT):
            self.ui.outputPlayButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        else:
            self.ui.outputPlayButton.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))


    def _toggle_icon(self, playback_area, button):
        if self.playback_manager.is_playing(playback_area):
            button.setIcon(ButtonIcons.PAUSE)
        else:
            button.setIcon(ButtonIcons.PLAY)
        return


    def _reset_play_icon(self):
        """Reset play icons to default the default icon before a new playback starts."""
        self.ui.outputPlayButton.setIcon(ButtonIcons.PLAY)
        self.ui.IRPlayButton.setIcon(ButtonIcons.PLAY)
        self.ui.inputPlayButton.setIcon(ButtonIcons.PLAY)


    def stop_playback(self):
        if not self.playback_manager.is_playing():
            return
        curr_area = self.playback_manager.get_current_area()
        cursor = self._cursors.get(curr_area)
        self._reset_play_icon()
        self.playback_manager.stop(curr_area)
        cursor.setValue(0)

    def restart_playback(self):
        curr_file = self.playback_manager.get_current_audio()
        curr_area = self.playback_manager.get_current_area()
        self.stop_playback()
        self.playback_manager.toggle_play_pause(curr_file, curr_area, self)
        self._toggle_icon(curr_area, self._buttons.get(curr_area))


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


    def clear_fields(self):
        self.playback_manager.stop_all()
        self._audio_input_original.clear()
        self._ir_input_original.clear()
        self.audio_input.clear()
        self.ir_input.clear()
        self._output_audio.clear()
        self.ui.inputFileDisplay.setPlainText("")
        self.ui.IRFileDisplay.setPlainText("")
        self._reset_play_icon()

        # Delete all waveforms and cursors
        for (widget, curve), (area, cursor) in zip(self._curves.items(), self._cursors.items()):
            widget.removeItem(cursor)
            if curve.getData() is not None:
                curve.setData([])


    def load_input_audio(self):
        self.audio_input.load_file(self._audio_input_original)
        self.display_waveform(self.input_curve, self.audio_input.data,
                              self.audio_input.samplerate)
        self.ui.InputPeekWidget.addItem(self.input_cursor)
        if self.audio_input.samplerate > 0 and self.ir_input.samplerate > 0:
            self.convolve()
        file_path = self.audio_input.file_path
        if file_path != "":
            file_path = file_path.split("/")[-1]
        self.ui.inputFileDisplay.setPlainText(file_path)


    def load_ir_audio(self):
        self.ir_input.load_file(self._ir_input_original)
        self.display_waveform(self.ir_curve, self.ir_input.data, self.ir_input.samplerate)
        self.ui.IRPeekWidget.addItem(self.ir_cursor)
        if self.audio_input.samplerate > 0 and self.ir_input.samplerate > 0:
            self.convolve()
        file_path = self.ir_input.file_path
        if file_path != "":
            file_path = file_path.split("/")[-1]
        self.ui.IRFileDisplay.setPlainText(file_path)


    def change_input_gain(self, audio_file: AudioFile, db_val: int = 0):
        if db_val == 0:
            self._input_audio_files[audio_file].copy_data(audio_file)
        else:
            audio_file.adjust_gain(self._input_audio_files[audio_file], db_val)
        if audio_file is self.audio_input:
            self.display_waveform(self.input_curve, self.audio_input.data, self.audio_input.samplerate)
        else:
            self.display_waveform(self.ir_curve, self.ir_input.data, self.ir_input.samplerate)
        if self.audio_input.samplerate > 0 and self.ir_input.samplerate > 0:
            self.convolve()


    def change_output_gain(self, db_val: int = 0):
        if db_val == 0:
            self._output_audio.copy_data(self.output_audio_copy)
        else:
            self._output_audio.adjust_gain(self.output_audio_copy, db_val)
        self.display_waveform(self.output_curve, self._output_audio.data, self._output_audio.samplerate)


    def convolve(self):
        self._output_audio = process(self.audio_input, self.ir_input)
        if self._output_audio is not None:
            self._output_audio.copy_data(self.output_audio_copy)
        self.display_waveform(self.output_curve, self._output_audio.data,
                              self._output_audio.samplerate)
        self.ui.graphicsView.addItem(self.output_cursor)


    def display_waveform(self, curve, audio_data, samplerate):
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
        self.playback_manager.cleanup()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()