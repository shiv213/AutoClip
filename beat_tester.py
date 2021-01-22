from moviepy.editor import *
# from demo_pitch import get_onsets
# from beat_analysis import get_onsets
from librosa_beat_track import beat_track
import matplotlib.pyplot as plt

input_audio = "music/robbery.mp3"
audio = AudioFileClip(input_audio)
beats, onset_env = beat_track(input_audio, plot=True)
clips = []

# timestamps = []
# for x in range(len(beats)):
#     if x % 2 == 0:
#         timestamps.append(beats[x])
#
# print(timestamps)

i = 0

# switching from one to other
while i < len(beats) - 1:
    if (i % 2) == 0:
        clips.append(ColorClip((100, 50), (0, 0, 0), duration=beats[i + 1] - beats[i]))
    else:
        clips.append(ColorClip((100, 50), (255, 255, 255), duration=beats[i + 1] - beats[i]))
    i += 1

# output_clip = concatenate_videoclips(clips).set_audio(audio)
# output_clip.write_videofile("beat_test.mp4", fps=30)
