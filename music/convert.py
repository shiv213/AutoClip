from os import path
from pydub import AudioSegment

# files
src = "depressed.mp3"
dst = "depressed.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")