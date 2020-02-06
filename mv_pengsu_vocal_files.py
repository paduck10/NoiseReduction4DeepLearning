import os, sys
import re
import argparse
import shutil

def mv_vocal_files(media_path, out_path):
	for dir in os.listdir(media_path):
		for file in os.listdir(media_path + str(dir) + '/'):
			if str(file).startswith('vocal'):
				os.rename(media_path + str(dir) + '/' + str(file), out_path + str(dir) + '.mp3')
				print('Moved vocal.mp3 in ' + str(dir) + ' folder to ' + out_path + str(dir) + '.mp3')


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_dir', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/separate_vocal_and_accompaniment/', help='If the separation is over, then the output files are stored in a separate folder, e.g. 9, 82, 81, ... -> This input should be the parent directory of those separate folders, which moves each vocal and accompaniment files to the output directory')
	parser.add_argument('-o', '--output_dir', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/collect_vocalfile/', help='Type the directory where all vocal/music fils will be stored.')

	args = parser.parse_args()

	mv_vocal_files(args.input_dir, args.output_dir)

