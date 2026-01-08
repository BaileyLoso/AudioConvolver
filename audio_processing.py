import soundfile as sf
import numpy as np
from scipy.signal import fftconvolve, resample, decimate
from PySide6.QtWidgets import QFileDialog, QMessageBox, QErrorMessage



class AudioFile:
    def __init__(self):
        self.file_path = ""
        self.data = np.empty(2)
        self.samplerate = 0
        self.channels = 0

    def __repr__(self):
        return f"AudioFile(file_path='{self.file_path}', samplerate={self.samplerate}, channels={self.channels})"

    def __eq__(self, other):
        return self.file_path == other.file_path

    def load_file(self, audio_copy):
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Select audio file", "", "Audio Files (*.wav *.mp3 *.flac)")

        # Check if file path is valid
        if self.file_path:
            try:
                self.data, self.samplerate = sf.read(self.file_path, always_2d=True)
                self.channels = self.data.shape[1]
                self.copy_data(audio_copy)
            except Exception as e:
                QErrorMessage(parent=None).showMessage(str(e))
                return

        # If file path is invalid, return
        else:
            return
        QMessageBox.information(None, "Success", f"Loaded file: {self.file_path}")

    def copy_data(self, dst):
        dst.file_path = self.file_path
        dst.data = self.data
        dst.samplerate = self.samplerate
        dst.channels = self.channels

    def adjust_gain(self, original, gain_val):
        if self.data.size == 0 or original.data.size == 0:
            return
        gain_val = gain_val * 2
        self.data = original.data * gain_val
        self.data = np.clip(self.data, -1, 1)
        return

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
        output_audio = AudioFile()

        if audio_in.samplerate != ir.samplerate:
            num_samples_new = int(ir.data.shape[0] * audio_in.samplerate / ir.samplerate)
            ir.data = resample(ir.data, num_samples_new, axis=0)
            ir.samplerate = audio_in.samplerate

        # Fill in data fields for audio
        output_audio.data = fftconvolve(audio_in.data, ir.data, mode='full', axes=0)
        output_audio.samplerate = audio_in.samplerate

        # Calling shape() on 2nd element finds number of channels
        output_audio.channels = output_audio.data.shape[1]

        if output_audio.channels > 2:
            output_audio.data = output_audio.data[:, :2]  # Keep only first two channels if more than 2 channels

        # 1.0 is max amplitude for audio files
        if np.max(np.abs(output_audio.data)) > 1.0:
            output_audio.data = output_audio.data / np.max(np.abs(output_audio.data))  # Normalize to prevent clipping
        return output_audio

    def save_output(self, output_audio):
        self.output_audio_path = QFileDialog.getSaveFileName(None, "Save output audio file", "", "Audio Files (*.wav *.mp3 *.flac)")[0]
        if self.output_audio_path is None or self.output_audio_path == "":
            QErrorMessage(parent=None).showMessage("No output file path selected")
            return
        sf.write(self.output_audio_path, output_audio.data, output_audio.samplerate)
        QMessageBox.information(None, "Success", f"Saved output to: {self.output_audio_path}")
        return