#!/usr/bin/env python
'''
CREATED:2014-06-04 11:43:30 by Colin Raffel <craffel@gmail.com>

Detect onsets in an audio file

Usage:   ./onset_detector.py [-h] input_file.mp3    output_onsets.csv
'''
from __future__ import print_function

import argparse
import sys
import numpy as np
import librosa
import matplotlib.pyplot as plt

def onset_detect(input_file):
    '''Onset detection function

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save onset timestamps as a CSV file
    '''

    # 1. load the wav file and resample to 22.050 KHz
    print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)

    # Use a default hop size of 512 frames @ 22KHz ~= 23ms
    hop_length = 512

    # 2. run onset detection
    print('Detecting onsets...')
    o_env = librosa.onset.onset_strength(y, sr=sr)
    times = librosa.times_like(o_env, sr=sr)
    plt.plot(times, 2 + o_env / o_env.max(), alpha=0.8, label='Mean (mel)')
    plt.show()
    onsets = librosa.onset.onset_detect(onset_envelope=o_env, y=y,
                                        sr=sr,
                                        hop_length=hop_length)
    print("Found {:d} onsets.".format(onsets.shape[0]))

    # 3. save output
    # 'beats' will contain the frame numbers of beat events.

    onset_times = librosa.frames_to_time(onsets,
                                         sr=sr,
                                         hop_length=hop_length)

    print('done!')
    return onset_times


if __name__ == '__main__':
    # Run the beat tracker
    print(onset_detect("music/wave.wav"))
