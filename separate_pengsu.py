#!/bin/bash

"""

Should be run in the directory where "pretrained_model" folder lives
Otherwise, it cannot found "pretrained_model" which return error.

"""



import os
import sys
import argparse
import subprocess

def get_files_from_path(media_path):
	original_files = []
	for file in os.listdir(media_path):
		if str(file).endswith('.mp3'):
			file_name = media_path + str(file)
			original_files.append(file_name)
	#print(original_files)
	return original_files

if __name__ == "__main__":
	os.environ["CUDA_VISIBLE_DIVICES"]="1"
	parser = argparse.ArgumentParser()
#       parser.add_argument('-i', '--input_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media/', help='Type the directory whe    re     original youtube files are')
#       parser.add_argument('-o', '--output_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/voice_separation/spleeter/pengsu_yt_output/', help='Type the out    put     directory. Separated vocal and music files will be stored')
	parser.add_argument('-i', '--input_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/dataset/originalfile/indexed/', help='Type the directory where original youtube files are')
	parser.add_argument('-o', '--output_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/dataset/separate_vocal_and_accompaniment/', help='Type the output directory. Separated vocal and music files will be stored')
	parser.add_argument('-c', '--codec', default = 'mp3', help='Choose which codec to use : mp3, wav, ogg, m4a, wma, flac')
	args = parser.parse_args()

	file_list = get_files_from_path(args.input_dir)
	file_names = ''
	for item in file_list:
		#file_names += ' ' + item + ' '
		spleeter_cmd = 'spleeter separate -i %s -o %s -c %s' % (item, args.output_dir, args.codec)
		print('Separating ' + str(item) + ' started!')
		os.system(spleeter_cmd)
		print('Separating ' + str(item) + ' done!')

	#spleeter_cmd = 'spleeter separate -i %s -o %s ' % (file_names, args.output_dir)
	#os.system(spleeter_cmd)
