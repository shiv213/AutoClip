from moviepy.editor import *
# from beat_analysis import get_onsets
from video_analysis import make_cuts
import glob
from beat_tracker import beat_track

input_audio = "music/japan88.wav"
audio = AudioFileClip(input_audio)
beats = beat_track(input_audio)
timestamps = []

for x in range(len(beats)):
    if x % 2 == 0:
        timestamps.append(beats[x])

print(timestamps)

videos_dir = "clips/identical/"
# videos_dir = "output/"
videos = []
for x in glob.glob(videos_dir + "*"):
    videos.append(x.replace('\\', '/'))
print(videos)

cut_videos = []
output_path = "output"
for x in videos:
    cut_videos += make_cuts(x, output_path, buff_size=40)
print(cut_videos)

count = 0
clips = []
while count < len(videos) - 1:
    clips.append(VideoFileClip(cut_videos[count]).subclip(0, timestamps[count + 1] - timestamps[count]))
    count += 1

output_clip = concatenate_videoclips(clips).set_audio(audio)
output_clip.write_videofile("output.mp4")

# TODO Clean temp files left behind
