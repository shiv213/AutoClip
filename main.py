from moviepy.editor import *
from beat_analysis import get_onsets
# from video_analysis import get_cuts

input_audio = "music/short_loop.wav"
audio = AudioFileClip(input_audio)
timestamps = get_onsets(input_audio)
input_clip = VideoFileClip("clips/manual.mp4")
timestamps.append(timestamps[-1]+2)
print(timestamps)
clips = []
count = 0
while count < len(timestamps)-1:
    clips.append(input_clip.subclip(timestamps[count], timestamps[count+1]+0.1))
    count += 1

# temp = []
# for i in reversed(clips):
#     temp.append(i)

output_clip = concatenate_videoclips(clips).set_audio(audio)
output_clip.ipython_display(width=1080, height=1920)
