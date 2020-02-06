import os
import shutil
from os import path
import glob
import re
import argparse
from pathlib import Path

def indexing(media_path):
	i = 1
	Path(media_path + 'indexed/').mkdir(parents=True, exist_ok=True)
	for file in os.listdir(media_path):
	# Ignore alreay changed one
		if file.endswith(".mp3"):
			filename = str(file)
			print('Changing %s th file!' % i)
			os.rename(media_path + filename, media_path + 'indexed/'  + '%s.mp3' % i)
			i += 1

if __name__ == "__main__":
	print('working!')
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_dir', default="/home/deokgyu.ahn/practice/Resource/Code/dataset/originalfile/", help='Type directory where media files live, waiting for indexing, -> 1.mp3, 2.mp3, ...')
	args = parser.parse_args()
	indexing(args.input_dir)
