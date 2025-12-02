import soundfile as sf
import numpy as np
from scipy.signal import fftconvolve
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename, asksaveasfilename


### Main application window
class MainWindow:
    def __init__(self, master):
        self.master = master
        master.minsize(400, 200)
        master.maxsize(1200, 600)
        master.title("Audio Convolver")

        audio_input = AudioInput()
        ir_input = AudioInput()

        def process(audio_in, ir_in):
            if audio_in.file_path is None or ir_in.file_path is None:
                mbox.showerror("Error", "Please select both input audio and impulse response files")
                return
            try:
                convolver = AudioConvolver(audio_in, ir_in)
                output_audio = convolver.convolve(audio_in, ir_in)
                convolver.save_output(output_audio)
            except AssertionError as e:
                mbox.showerror("Error", str(e))
                return

        self.label = tk.Label(master, text="Select input audio and impulse response files:")
        self.label.pack()
        self.input_button = tk.Button(master, text="Select Input Audio", command=audio_input.load_file)
        self.input_button.pack()
        self.ir_button = tk.Button(master, text="Select Impulse Response", command=ir_input.load_file)
        self.ir_button.pack()
        self.process_button = tk.Button(master, text="Process", command=lambda: process(audio_input, ir_input))
        self.process_button.pack()
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()


class AudioInput:
    def __init__(self):
        self.file_path = None
        self.data = None
        self.samplerate = None
        self.channels = None

    def load_file(self):
        self.file_path = askopenfilename(title="Select an audio file",
                                         filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3"),
                                                    ("FLAC Files", "*.flac")])
        if self.file_path is None or self.file_path == "":
            mbox.showerror("Error", "No file selected")
            return
        self.data, self.samplerate = sf.read(self.file_path, always_2d=True)
        if self.data is None:
            mbox.showerror("Error", "Failed to load audio file")
            return

        mbox.showinfo("Success", f"Loaded file: {self.file_path}")


#TODO : Link process button to AudioConvolver class
#TODO : Add gain control to convolved output before saving

### This is where we will handle audio processing
class AudioConvolver:
    def __init__(self, input_audio, impulse_response):
        self.input_audio_path = input_audio.file_path
        self.impulse_response_path = impulse_response.file_path
        self.output_audio_path = "output.wav"

    @staticmethod
    def convolve(input_audio, impulse_response):
        output_audio = AudioInput()
        assert input_audio.samplerate == impulse_response.samplerate, "Sample rates do not match"

        # Fill in data fields for audio
        output_audio.data = fftconvolve(input_audio.data, impulse_response.data, mode='full', axes=0)
        output_audio.samplerate = input_audio.samplerate

        # Calling shape() on 2nd element finds number of channels
        output_audio.channels = output_audio.data.shape[1]

        if output_audio.channels > 2:
            output_audio = output_audio[:, :2]  # Keep only first two channels if more than 2 channels

        # 1.0 is max amplitude for audio files
        if np.max(np.abs(output_audio.data)) > 1.0:
            output_audio.data = output_audio.data / np.max(np.abs(output_audio.data))  # Normalize to prevent clipping
        return output_audio

    def save_output(self, output_audio):
        self.output_audio_path = asksaveasfilename(title="Save output audio file", defaultextension=".wav",
                                                   filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3"),
                                                              ("FLAC Files", "*.flac")])
        if self.output_audio_path is None or self.output_audio_path == "":
            mbox.showerror("Error", "No file selected for saving")
            return
        sf.write(self.output_audio_path, output_audio.data, output_audio.samplerate)
        mbox.showinfo("Success", f"Saved output file: {self.output_audio_path}")


root = tk.Tk()
MainWindow(root)
root.mainloop()
