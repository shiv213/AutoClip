import librosa
from librosa import display
import matplotlib.pyplot as plt

# To load the file, and get the amplitude measured with the sampling rate amplitude,
y, sr = librosa.load("music/depressed.wav")

# To plot the pressure-time plot
librosa.display.waveplot(y, sr=sr)

# Build the Fourier transform
X = librosa.stft(y)
# Apply a conversion from raw amplitude to decibel
Xdb = librosa.amplitude_to_db(abs(X))
# Build a spectrogram
librosa.display.specshow(Xdb, sr=sr, x_axis="time", y_axis="hz")
