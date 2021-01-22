from moviepy.editor import *
from video_analysis import make_cuts
import glob
from librosa_beat_track import beat_track
import numpy as np
from itertools import permutations
import progressbar

audio_file = "music/blueberry_faygo.mp3"
# videos_dir = "clips/identical/"
videos_dir = "csgo/"

beats, onsets = beat_track(audio_file, plot=False)
onsets = [float(i) / max(onsets) for i in onsets]
videos = []
for x in glob.glob(videos_dir + "*"):
    videos.append(x.replace('\\', '/'))

output_name = "output"
cut_videos = videos

# Do video analysis
# cut_videos = []
# for x in progressbar.progressbar(videos):
#     cut_videos += make_cuts(x, output_path, buff_size=40)
# print(cut_videos)


def permutation_generator(a):
    a.sort()
    yield list(a)
    if len(a) <= 1:
        return
    first = 0
    last = len(a)
    while 1:
        i = last - 1
        while 1:
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
                break
            if i == first:
                a.reverse()
                return


count = 0
clips = []
beat_length = np.diff(np.array(beats)).mean()
rounded_beats = []
original_clips = []
best_order = []
max_weight = 0

for clip in cut_videos:
    vfc = VideoFileClip(clip)
    rounded_beats.append(int(vfc.duration / beat_length))
    original_clips.append(vfc)

# TODO Check if audio file is longer than video clips

print("Total Clips: ", len(original_clips))
print("Calculating best order of clips")
widgets = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar()
]

bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength, widgets=widgets)

# Unoptimized original loop
# for permutation in list(permutations(rounded_beats, len(rounded_beats))):

for permutation in permutation_generator(rounded_beats):
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
for x in range(len(best_order) - 1):
    adjusted_clip = original_clips[rounded_beats.index(best_order[x])].fx(vfx.speedx,
                                                                          final_duration=best_order[x] * beat_length)
    original_clips[rounded_beats.index(best_order[x])] = 0
    rounded_beats[rounded_beats.index(best_order[x])] = 0
    # original_clips.pop(rounded_beats.index(best_order[x]))
    clips.append(adjusted_clip)

# Crossfade transitions
# clips = [CompositeVideoClip([clip.fx(transfx.crossfadein, 0.5)]) for clip in clips]
all_clips = concatenate_videoclips(clips)
audio = AudioFileClip(audio_file)
output_clip = all_clips.set_audio(audio.subclip(0, all_clips.duration))
output_clip.write_videofile("output.mp4", fps=30)

# Clean temp files left behind
# for x in glob.glob(output_path + "*"):
#     try:
#         x.unlink()
#     except OSError as e:
#         print("Error: %s : %s" % (x, e.strerror))
