from moviepy.editor import *
from beat_analysis import get_onsets
from video_analysis import make_cuts
import glob

input_audio = "music/depressed.wav"
audio = AudioFileClip(input_audio)
timestamps = get_onsets(input_audio)
# timestamps.append(timestamps[-1] + 2)
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
