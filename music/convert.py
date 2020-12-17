from os import path
from pydub import AudioSegment

# files
src = "japan88.mp3"
dst = "japan88.wav"

# convert wav to mp3
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")