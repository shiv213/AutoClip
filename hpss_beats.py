#!/usr/bin/env python
"""
CREATED:2013-02-12 16:33:40 by Brian McFee <brm2132@columbia.edu>

Beat tracking with HPSS filtering

Usage: ./hpss_beats.py [-h] input_audio.mp3 output_beats.csv
"""
from __future__ import print_function

import argparse
import sys
import numpy as np
import librosa

# Some magic number defaults, FFT window and hop length
N_FFT = 2048

# We use a hop of 512 here so that the HPSS spectrogram input
# matches the default beat tracker parameters
HOP_LENGTH = 512


def beat_track(input_file):
    """HPSS beat tracking

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save beat event timestamps as a CSV file
    """

    # Load the file
    print('Loading  ', input_file)
    y, sr = librosa.load(input_file)

    # Do HPSS
    print('Harmonic-percussive separation ... ')
    y = librosa.effects.percussive(y)

    # Construct onset envelope from percussive component
    print('Tracking beats on percussive component')
    onset_env = librosa.onset.onset_strength(y=y,
                                             sr=sr,
                                             hop_length=HOP_LENGTH,
                                             n_fft=N_FFT,
                                             aggregate=np.median)

    # Track the beats
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
                                           sr=sr,
                                           hop_length=HOP_LENGTH)

    beat_times = librosa.frames_to_time(beats,
                                        sr=sr,
                                        hop_length=HOP_LENGTH)

    print(beat_times)
    return beat_times


if __name__ == '__main__':
    # Run the beat tracker
    beat_track("music/depressed.wav")
