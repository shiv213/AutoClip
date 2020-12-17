from moviepy.editor import *
from beat_analysis import get_onsets

input_audio = "music/wave.wav"
audio = AudioFileClip(input_audio)
timestamps = get_onsets(input_audio)
# timestamps.append(timestamps[-1] + 2)
print(timestamps)

# TODO add beat tester (using white pulses on black background)
total = []
i = 0
while i < len(timestamps) - 2:
    if (i % 2) == 0:
        total.append(ColorClip((100, 50), (0, 0, 0), duration=timestamps[i + 1] - timestamps[i]))
    else:
        total.append(ColorClip((100, 50), (255, 255, 255), duration=timestamps[i + 1] - timestamps[i]))
    i += 1

output_clip = concatenate_videoclips(total).set_audio(audio)
output_clip.write_videofile("beat_test.mp4", fps=30)
