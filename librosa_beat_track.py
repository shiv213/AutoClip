import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def beat_track(input_file, plot=False):
    y, sr = librosa.load(input_file)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    librosa.frames_to_time(beats, sr=sr)
    onset_env = librosa.onset.onset_strength(y, sr=sr,
                                             aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,
                                           sr=sr)
    hop_length = 512
    times = librosa.times_like(onset_env, sr=sr, hop_length=hop_length)

    if plot:
        fig, ax = plt.subplots(nrows=2, sharex='all')
        m = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
        librosa.display.specshow(librosa.power_to_db(m, ref=np.max),
                                 y_axis='mel', x_axis='time', hop_length=hop_length,
                                 ax=ax[0])
        ax[0].label_outer()
        ax[0].set(title='Mel spectrogram')
        ax[1].plot(times, librosa.util.normalize(onset_env),
                   label='Onset strength')
        ax[1].vlines(times[beats], 0, 1, alpha=0.5, color='r',
                     linestyle='--', label='Beats')
        ax[1].legend()
        plt.show()

    return times[beats].tolist(), onset_env[beats]
