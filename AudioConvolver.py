import soundfile as sf
import numpy as np
from scipy.signal import fftconvolve, resample
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
from pygame.locals import *




### Main application window
class MainWindow:
    def __init__(self, master):
        self.master = master
        master.minsize(400, 200)
        master.maxsize(1800, 900)
        master.title("Audio Convolver")

        # Maintain copy of signals
        audio_input_original = AudioInput()
        ir_input_original = AudioInput()
        audio_input = AudioInput()
        ir_input = AudioInput()
        self.output_audio = AudioInput()


        def process(audio_in, ir_in):
            if audio_in.file_path is None or ir_in.file_path is None:
                mbox.showerror("Error", "Please select both input audio and impulse response files")
                return
            try:
                convolver = AudioConvolver(audio_in, ir_in)
                output_audio = convolver.convolve(audio_in, ir_in)
                # convolver.save_output(output_audio)
                return output_audio
            except AssertionError as e:
                mbox.showerror("Error", str(e))
                return

        self.label = tk.Label(master, text="Select input audio and impulse response files:")
        self.label.pack()
        self.input_button = tk.Button(master, text="Select Input Audio", command = lambda: audio_input.load_file(audio_input_original))
        self.input_button.pack()
        self.input_gain_slider = tk.Scale(master, from_ = 100, to = 0, resolution = 1, orient = "vertical", 
                                    command = lambda val: audio_input.adjust_gain(audio_input_original, float(val)))
        self.input_gain_slider.set(50)
        self.input_gain_slider.pack()

        self.ir_button = tk.Button(master, text="Select Impulse Response", command = lambda: ir_input.load_file(ir_input_original))
        self.ir_button.pack()
        self.ir_gain_slider = tk.Scale(master, from_ = 100, to = 0, resolution= 1, orient = "vertical", 
                                    command = lambda val: ir_input.adjust_gain(ir_input_original, float(val)))
        self.ir_gain_slider.set(50)
        self.ir_gain_slider.pack()

        def on_process():
            self.output_audio = process(audio_input, ir_input)
            self.export_button.config(state="normal")
            return
        
        self.process_button = tk.Button(master, text="Process", command=on_process)
        self.process_button.pack()

        def on_export():
            convolver = AudioConvolver(audio_input, ir_input)
            convolver.save_output(self.output_audio)
            return

        self.export_button = tk.Button(master, text="Export Audio File", state="disabled", command=on_export)
        self.export_button.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()


class AudioInput:
    def __init__(self):
        self.file_path = ""
        self.data = np.empty(2)
        self.samplerate = 0
        self.channels = 0

    def load_file(self, audio_copy):
        self.file_path = askopenfilename(title="Select an audio file",
                                         filetypes=[("WAV Files", "*.wav"), ("MP3 Files", "*.mp3"),
                                                    ("FLAC Files", "*.flac"), ("AIFF Files", "*.aiff"), ("AU Files", "*.au"), ("CAF Files", "*.caf")])
        if self.file_path is None or self.file_path == "":
            mbox.showerror("Error", "No file selected")
            return
        try:
            self.data, self.samplerate = sf.read(self.file_path, always_2d=True)
        except Exception as e:
            mbox.showerror("Error", f"Failed to read file: {str(e)}")
            return
        if self.data.size == 0:
            mbox.showerror("Error", "Failed to load audio file")
            return
        self.channels = self.data.shape[1]
        self.copy_data(audio_copy)
        mbox.showinfo("Success", f"Loaded file: {self.file_path}")

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
        

### This is where we will handle audio processing
class AudioConvolver:
    def __init__(self, input_audio, impulse_response):
        self.input_audio_path = input_audio.file_path
        self.impulse_response_path = impulse_response.file_path
        self.output_audio_path = "output.wav"

    @staticmethod
    def convolve(input_audio, impulse_response):
        output_audio = AudioInput()

        if input_audio.samplerate != impulse_response.samplerate:
            num_samples_new = int(impulse_response.data.shape[0] * input_audio.samplerate / impulse_response.samplerate)
            impulse_response.data = resample(impulse_response.data, num_samples_new, axis=0)
            impulse_response.samplerate = input_audio.samplerate

        # Fill in data fields for audio
        output_audio.data = fftconvolve(input_audio.data, impulse_response.data, mode='full', axes=0)
        output_audio.samplerate = input_audio.samplerate

        # Calling shape() on 2nd element finds number of channels
        output_audio.channels = output_audio.data.shape[1]

        if output_audio.channels > 2:
            output_audio.data = output_audio.data[:, :2]  # Keep only first two channels if more than 2 channels

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
