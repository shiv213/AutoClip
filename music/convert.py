from os import path
from pydub import AudioSegment

# files
src = "full_depressed.mp3"
dst = "full_depressed.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")