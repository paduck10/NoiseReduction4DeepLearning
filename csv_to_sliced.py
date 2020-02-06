import csv
from collections import OrderedDict
import argparse
import os, sys
import shutil
from pydub import AudioSegment
import re

# Slice mp3 files, (format : 1.mp3, 2.mp3, 3.mp3, ...) according to the csv file
# csv file stores starting/ending point of each speech, music, or Noenergy part
# csv file contains information made by inaSpeechSegment library

def csv2sliced(minsec, in_path, out_path, csv_path):
	# Should match .mp3 and .csv file (corresponding files)
	for file in os.listdir(csv_path):
		cur_file = str(file) 
		print('Slicing .mp3 file with ' + cur_file + '!') # For debugging
		with open(csv_path + cur_file) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter='\t')
			line_count = 0
			st_fn = []
			for row in csv_reader:
				if row[0] == 'male': # Change this to female if you want female voice
					if float(row[2]) - float(row[1]) > minsec:
						st_fn.append((row[1], row[2]))
			print(st_fn) #For debugging
			# Pydub slice : 1000 means 1 sec
			name = re.search("\d+", cur_file).group()
			# Indexing work is needed
			song = AudioSegment.from_mp3(in_path + name + '.mp3')
			for i in range(len(st_fn)):
				st = int(float(st_fn[i][0]) * 1000)
				fn = int(float(st_fn[i][1]) * 1000)
				print(st, fn)
				sliced = song[st:fn]
				sliced.export(out_path + "%s-%s-slice.mp3" % (name, i), format="mp3")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--minsec', default="1.5", help='Minial second in terms of slicing the speech, used for training. It is float type value, but you can just type integer, e.g. "-m 1" ', type=float, required=False)
    parser.add_argument('-i', '--in_path', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/collect_vocalfile/', help='Default : media folder! Path where the original mp3 files are!')
    parser.add_argument('-o', '--out_path', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/sliced_vocalfile/', help='Default : data_sliced folder. If you want to customize your output directory file, go ahead.')
    parser.add_argument('-c', '--csv_path', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/collect_vocalfile/output_csv/', help='Directory where csv files are in!')
    args = parser.parse_args()
    csv2sliced(args.minsec, args.in_path, args.out_path, args.csv_path)

if __name__ == "__main__":
	main()

