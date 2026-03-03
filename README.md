# AudioConvolver — FFT-Based Audio Convolution Tool

AudioConvolver is a small desktop app for loading any two audio files (a **source** and an **impulse response (IR)**) generating 
a **convolved** output, useful for IR-style reverb effects, acoustic simulation, and more experimental sound design applications.

![Image of an AudioConvolver demo](/resources/demo.png)

## Features
- Load common formats like `.wav`, `.mp3`, or `.flac` file as the input audio or IR
- Automatic resampling when input and IR sample rates differ
- Real-time waveform display for input, IR, and output signals
- Playback controls (play, pause, stop, restart) for all three signals
- Playback position cursor on each waveform
- Adjustable gain (±10 dB) for input, IR, and output
- Export the convolved output to a file

## How it works
This project uses audio [convolution](https://en.wikipedia.org/wiki/Convolution) to combine two signals into a new signal: 
the source audio is effectively “filtered” through the impulse response (similar to [gaussian blur](https://en.wikipedia.org/wiki/Gaussian_blur)
in image processing). A typical use case is applying an impulse response recorded inside a room to produce a reverb-like 
effect. Using arbitrary signals can also produce more surreal, hybrid textures.

For increased performance, the following convolution methods are used:
* A standard convolution using the SciPy 
[fftconvolve](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.fftconvolve.html#scipy.signal.fftconvolve) 
method for shorter signals or similar-length inputs.
* Convolving with the [overlap-add method](https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method) 
using the scipy [oaconvolve](https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method) method for longer signals or 
highly mistmatched lengths.

## Requirements files
This repo uses two dependency lists:
* `requirements.txt` — **runtime dependencies** needed to run the app
* `requirements-gui.txt` — **developer tooling** used to build an executable

## Getting Started (running from source) 
### 1. Clone the repository
```aiignore
bash git clone https://github.com/BaileyLoso/AudioConvolver.git

```
### 2. Create your local environment:

**Windows**
```aiignore
bash python -m venv .venv
bash .venv\Scripts\activate
```

**macOS / Linux (bash/zsh)**
```aiignore
bash python -m venv .venv
bash source .venv/bin/activate
```

### 3. Install runtime dependencies
```
bash pip install -r requirements.txt
```

### 4. Run the app
```aiignore
bash python AudioConvolver.py
```

## Development (optional)
### Installing dev/build tools

```aiignore
bash pip install -r requirements-gui.txt
```
 ### Building the app
```aiignore
bash pyinstaller --clean -noconfirm AudioConvolver.spec
```


## Requirements
- [Python 3.12](https://www.python.org/): Due to package dependencies, this project will not work with Python versions
after 3.12.

### NOTE: 
- AudioConvolver is currently only tested on Windows 11, but future versions may support macOS and Linux.

## Setup 
```
bash git clone https://github.com/BaileyLoso/AudioConvolver.git
pip install PySide6 pyqtgraph scipy soundfile numpy
```

## Tech Stack
- [Python](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython-6/) (GUI)
- [pyqtgraph](https://www.pyqtgraph.org/) (waveform visualization)
- [SciPy](https://scipy.org/) (FFT-based convolution)
- [soundfile](https://python-soundfile.readthedocs.io/) (audio I/O)
- [sounddevice](https://python-sounddevice.readthedocs.io/) (audio playback)


## Limitations
- Gain adjustment is capped at ±10 dB
- Convolution of very large files may cause a brief UI freeze while processing
- Only the first two channels are kept if the convolved output exceeds stereo

## Roadmap
- Add a progress indicator for long convolution operations.
- Support drag-and-drop file loading.
- Add a wet/dry mix control for blending the original and convolved signals.

## References
- Convolution: https://en.wikipedia.org/wiki/Convolution
- SciPy `fftconvolve`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.fftconvolve.html
- SciPy `oaconvolve`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.oaconvolve.html
- Overlap-add method: https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method



