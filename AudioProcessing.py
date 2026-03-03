import soundfile as sf
import numpy as np
from scipy.signal import fftconvolve, resample, oaconvolve
from PySide6.QtWidgets import QFileDialog, QMessageBox, QErrorMessage
from PySide6.QtCore import QStandardPaths


class AudioFile:
    def __init__(self):
        self.file_path = ""
        self.data = np.empty(2)
        self.samplerate = 0
        self.channels = 0
        self.length = 0

    def __repr__(self):
        return f"AudioFile(file_path='{self.file_path}', samplerate={self.samplerate}, channels={self.channels})"

    def load_file(self, audio_copy):
        self.file_path, _ = QFileDialog.getOpenFileName(None,
                                                        "Select audio file",
                                                        "",
                                                        "Audio Files (*.wav *.mp3 *.flac *.aiff)")
        if self.file_path:
            try:
                self.data, self.samplerate = sf.read(self.file_path, always_2d=True)
                self.channels = self.data.shape[1]
                self.length = self.data.shape[0]
                self.copy_data(audio_copy)
            except Exception as e:
                QErrorMessage(parent=None).showMessage(str(e))
                return

        # If the file path is invalid, return
        else:
            return

    def copy_data(self, dst):
        dst.file_path = self.file_path
        dst.data = np.copy(self.data)
        dst.samplerate = self.samplerate
        dst.channels = self.channels
        dst.length = self.length

    def adjust_soundfile_gain(self, original_audio, db_val):
        if self.length == 0 or original_audio.length == 0:
            return 0
        if db_val == 0:
            return 0
        linear_gain = 10 ** (db_val / 20.0)
        self.data = original_audio.data * linear_gain
        self.data = np.clip(self.data, -1, 1)
        return linear_gain

    def get_duration(self):
        return self.data.shape[0] / self.samplerate

    def clear(self):
        self.file_path = ""
        self.data = np.empty(2)
        self.samplerate = 0
        self.channels = 0

### This is where we will handle audio processing
class AudioConvolver:
    def __init__(self, input_audio, impulse_response):
        self.input_audio_path = input_audio.file_path
        self.impulse_response_path = impulse_response.file_path
        self.output_audio_path = "output.wav"

    @staticmethod
    def convolve(audio_in, ir):
        """
        Convolve the input AudioFile with the impulse response (IR) AudioFile.

        Convert the input and IR audio data to float32 to encourage faster processing, then the IR is resampled to match
        the samplerate of the input audio if necessary.

        If the IR is shorter than 20% of the length of the input audio, uses oaconvolve for faster convolution.
        Otherwise, fftconvolve is used since it is more efficient with similar-sized audio files.

        The output AudioFile will have the same samplerate and number of channels as the input audio, and it
        will be normalized to prevent clipping.
        """
        output_audio = AudioFile()
        audio_data = audio_in.data.astype(np.float32)
        ir_data = ir.data.astype(np.float32)

        if audio_in.samplerate != ir.samplerate:
            num_samples_new = int(ir_data.shape[0] * audio_in.samplerate / ir.samplerate)
            ir.data = resample(ir_data, num_samples_new, axis=0)

        if ir.length < audio_in.length // 20:
            output_audio.data = oaconvolve(audio_data, ir_data, mode='full', axes=0)
        else:
            output_audio.data = fftconvolve(audio_data, ir_data, mode='full', axes=0)

        output_audio.samplerate = audio_in.samplerate

        # Calling shape() on 2nd element finds number of channels
        output_audio.channels = output_audio.data.shape[1]

        if output_audio.channels > 2:
            output_audio.data = output_audio.data[:, :2]  # Keep only the first two channels if more than 2 channels
        output_audio.length = output_audio.data.shape[0]

        max_val = np.max(np.abs(output_audio.data))
        # 1.0 is the max amplitude for audio files
        if max_val > 1.0:
            output_audio.data /= max_val  # Normalize to prevent clipping
        return output_audio

    def save_output(self, output_audio):
        self.output_audio_path = QFileDialog.getSaveFileName(None, "Save output audio file",
                                                             QStandardPaths.writableLocation(
                                                                 QStandardPaths.StandardLocation.DownloadLocation),
                                                             "Audio Files (*.wav *.mp3 *.flac *.aiff)")[0]
        if self.output_audio_path is None or self.output_audio_path == "":
            QErrorMessage(parent=None).showMessage("No output file path selected")
            return
        sf.write(self.output_audio_path, output_audio.data, output_audio.samplerate)
        QMessageBox.information(None, "Success", f"Saved output to: {self.output_audio_path}")
