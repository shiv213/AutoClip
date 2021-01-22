from moviepy.editor import *
from video_analysis import make_cuts
import glob
from librosa_beat_track import beat_track
import numpy as np
from itertools import permutations

input_audio = "music/robbery.mp3"
# videos_dir = "clips/identical/"
videos_dir = "output/test/"

beats, onsets = beat_track(input_audio, plot=True)
onsets = [float(i)/max(onsets) for i in onsets]
videos = []
for x in glob.glob(videos_dir + "*"):
    videos.append(x.replace('\\', '/'))

output_name = "output"
cut_videos = videos
# cut_videos = []
# for x in videos:
#     cut_videos += make_cuts(x, output_path, buff_size=40)
# print(cut_videos)

count = 0
clips = []
beat_length = np.diff(np.array(beats)).mean()
rounded_beats = []
original_clips = []

for clip in cut_videos:
    vfc = VideoFileClip(clip)
    rounded_beats.append(int(vfc.duration / beat_length))
    original_clips.append(vfc)

perms = permutations(rounded_beats, len(rounded_beats))

weights = []
orders = []
for permutation in list(perms):
    order = list(permutation)
    total_weight = 0
    running_beats = 0
    for element in order:
        running_beats += element
        total_weight += onsets[running_beats]
    weights.append(total_weight)
    orders.append(order)

best_order = orders[weights.index(max(weights))]
print(max(weights))
print(best_order)
for x in range(len(best_order)-1):
    adjusted_clip = original_clips[rounded_beats.index(best_order[x])].fx(vfx.speedx, final_duration=best_order[x]*beat_length)
    clips.append(adjusted_clip)

all_clips = concatenate_videoclips(clips)
audio = AudioFileClip(input_audio)
output_clip = all_clips.set_audio(audio.subclip(0, all_clips.duration))
output_clip.write_videofile("output.mp4", fps=30)

# Clean temp files left behind
# for x in glob.glob(output_path + "*"):
#     try:
#         x.unlink()
#     except OSError as e:
#         print("Error: %s : %s" % (x, e.strerror))
