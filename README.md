# AudioConvolver — an FFT-Based Audio Convolution Tool
Load any two audio files and convolve them together in real time — ideal for applying **impulse responses** to audio signals for reverb, acoustic simulation, and sound design.

## Tech Stack
- [Python](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [pyqtgraph](https://www.pyqtgraph.org/)
- [SciPy](https://scipy.org/)
- [soundfile](https://python-soundfile.readthedocs.io/)
- [pygame](https://www.pygame.org/)

## Description
This is a personal project where my goal was to explore digital signal processing and desktop GUI development. I used SciPy's FFT-based convolution routines for audio processing and PySide6 with pyqtgraph for building an interactive waveform display and playback interface.

## Features
- Load any `.wav`, `.mp3`, or `.flac` file as the input audio or impulse response.
- Automatic resampling when input and IR sample rates differ.
- Real-time waveform display for input, IR, and output signals.
- Playback controls (play, pause, stop, restart) for all three audio areas.
- Playback position cursor displayed on each waveform.
- Adjustable gain (±10 dB) for input, IR, and output via dial or spin box.
- Save the convolved output to a file.

## Getting Started

Requirements: [Python 3.12+](https://www.python.org/)
```
git clone https://github.com/BaileyLoso/AudioConvolver.git
pip install PySide6 pyqtgraph scipy soundfile pygame numpy
python AudioConvolver.py
```

## Limitations
- Gain adjustment is capped at ±10 dB.
- Convolution of very large files may cause a brief UI freeze.
- Only the first two channels are kept if the convolved output exceeds stereo.

## Roadmap
- Add a progress indicator for long convolution operations.
- Support drag-and-drop file loading.
- Add a wet/dry mix control for blending the original and convolved signals.
- Extend gain range or replace dial with a more precise fader control.
