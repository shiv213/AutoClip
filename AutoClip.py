from typing import List
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import moviepy
from moviepy.editor import *
import glob
import progressbar
import numpy
import math


def permutation_generator(a: List[int], limit: None):
    if limit is not None:
        max_perms = limit
    else:
        max_perms = -1
    a.sort()
    yield list(a)
    if len(a) <= 1:
        return
    first = 0
    last = len(a)
    while 1:
        i = last - 1
        while max_perms != 0:
            i = i - 1
            if a[i] < a[i + 1]:
                j = last - 1
                while not (a[i] < a[j]):
                    j = j - 1
                a[i], a[j] = a[j], a[i]
                r = a[i + 1:last]
                r.reverse()
                a[i + 1:last] = r
                yield list(a)
                max_perms -= 1
                break
            if i == first:
                a.reverse()
                return
        return


def analyze_audio(input_audio: str, plot: bool = False) -> object:
    """
    Returns time in seconds of beats and normalized onset strengths

    :param input_audio:
    :param plot:
    :return:
    """
    y, sr = librosa.load(input_audio)
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

    onsets = onset_env[beats]
    beats = times[beats].tolist()
    onsets = [float(i) / max(onsets) for i in onsets]
    return beats, onsets


def load_videos(videos_dir: str):
    """
    Return video file paths from provided directory

    :param videos_dir:
    :return:
    """
    videos = []
    for x in glob.glob(videos_dir + "*"):
        videos.append(x.replace('\\', '/'))
    return videos


# Do video analysis
# def analyze_videos(videos):
#     cut_videos = []
#     for x in progressbar.progressbar(videos):
#         cut_videos += make_cuts(x, output_path, buff_size=40)
#     print(cut_videos)

def fit_video(videos: List[str], beats: List[float], onsets: List[numpy.float64], maximum_perms=None) -> List[
    moviepy.video.io.VideoFileClip.VideoFileClip]:
    """
    Find most optimal ordering of clips based on provided beat and onsets (music) and return adjusted clips

    :param videos: list of all video paths
    :param beats: beats returned from analyze_audio function
    :param onsets: onsets returned from analyze_audio function
    :param maximum_perms: maximum amount of permutations to be used in finding the most optimal order of videos (None for no limit)
    """
    beat_length = np.diff(np.array(beats)).mean()
    rounded_beats = []
    original_clips = []
    best_order = []
    max_weight = 0
    for clip in videos:
        vfc = VideoFileClip(clip)
        rounded_beats.append(int(vfc.duration / beat_length))
        original_clips.append(vfc)

    print("Total Clips: ", len(original_clips))
    widgets = [
        'Calculating best order of clips: ', progressbar.Timer()
    ]

    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=widgets)

    for permutation in permutation_generator(rounded_beats, maximum_perms):
        order = list(permutation)
        total_weight = 0
        running_beats = 0
        for element in order:
            running_beats += element
            total_weight += onsets[running_beats]
        if total_weight > max_weight:
            max_weight = total_weight
            best_order = order
        bar.update()

    print("\n")
    print("Original order: ", rounded_beats)
    print("Best order: ", best_order)

    clips = []
    for x in range(len(best_order) - 1):
        adjusted_clip = original_clips[rounded_beats.index(best_order[x])].fx(vfx.speedx,
                                                                              final_duration=best_order[
                                                                                                 x] * beat_length)
        original_clips[rounded_beats.index(best_order[x])] = 0
        rounded_beats[rounded_beats.index(best_order[x])] = 0
        clips.append(adjusted_clip)
        # Crossfade transitions
        # clips = [CompositeVideoClip([clip.fx(transfx.crossfadein, 0.5)]) for clip in clips]
    return clips


def write_video(clips: List[moviepy.video.io.VideoFileClip.VideoFileClip], audio_file: str, filename: str,
                fps: int = 30) -> None:
    """
    Write provided video clips and audio file to video

    :param clips:
    :param audio_file:
    :param filename:
    :param fps:
    """
    all_clips = concatenate_videoclips(clips)
    output_clip = all_clips.set_audio(AudioFileClip(audio_file).subclip(0, all_clips.duration))
    output_clip.write_videofile(filename + ".mp4", fps=fps)


def run_autoclip(audio_file: str, videos_dir: str, output_filename: str, maximum_perms=math.factorial(10)):
    """
    Automatically run AutoClip and write output to video file

    :param audio_file:
    :param videos_dir:
    :param output_filename:
    :param maximum_perms:
    """
    beats, onsets = analyze_audio(audio_file, plot=False)
    videos = load_videos(videos_dir)
    clips = fit_video(videos, beats, onsets, maximum_perms)
    write_video(clips, audio_file, output_filename, 30)
