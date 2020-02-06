import os
from pydub import AudioSegment
import argparse
import re

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', help='Type mp3 file name to convert!', required=True)
	parser.add_argument('-o', '--output', default='out.wav', help='Type wav file name for output!')
	args = parser.parse_args()

	nameRegex = re.compile(r'.+\.')
	filename = re.match(nameRegex, args.input).group()

	src = args.input
	dst = filename + 'wav'

	sound = AudioSegment.from_mp3(src)
	sound.export(dst, format='wav')
