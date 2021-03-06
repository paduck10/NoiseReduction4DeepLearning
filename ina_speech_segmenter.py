#!/usr/bin/env python
# encoding: utf-8

# The MIT License

# Copyright (c) 2018 Ina (David Doukhan - http://www.ina.fr/)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import glob
import os
import distutils.util
import warnings
import indexing_data # Indexing .mp3 files in 'media' folder
import sys


# TODO
# * Allow the selection of a custom ffmpeg binary
# * allow the use a external activity or speech music segmentations
# * describe URL management in help and interference with glob

description = """Do Speech/Music(/Noise) and Male/Female segmentation and store segmentations into CSV files. Segments labelled 'noEnergy' are discarded from music, noise, speech and gender analysis. 'speech', 'male' and 'female' labels include speech over music and speech over noise. 'music' and 'noise' labels are pure segments that are not supposed to contain speech.
"""
epilog="""
Detailled description of this framework is presented in the following study:
Doukhan, D., Carrive, J., Vallet, F., Larcher, A., & Meignier, S. (2018, April). An open-source speaker gender detection framework for monitoring gender equality. In 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 5214-5218). IEEE.
"""


# Configure command line parsing
parser = argparse.ArgumentParser(description=description, epilog=epilog)
parser.add_argument('-i', '--input', nargs='+', help='Input media to analyse. May be a full path to a media (/home/david/test.mp3), a list of full paths (/home/david/test.mp3 /tmp/mymedia.avi), or a regex input pattern ("/home/david/myaudiobooks/*.mp3")', required=False)
parser.add_argument('-r', '--input_dir', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/collect_vocalfile/', help='(Default : /home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media) Input media DIRECTORY where all the media files are in!')
parser.add_argument('-o', '--output_directory', default='/home/deokgyu.ahn/practice/Resource/Code/dataset/collect_vocalfile/output_csv', help='Directory used to store segmentations. Resulting segmentations have same base name as the corresponding input media, with csv extension. Ex: mymedia.MPG will result in mymedia.csv', required=False)
parser.add_argument('-d', '--vad_engine', choices=['sm', 'smn'], default='smn', help="Voice activity detection (VAD) engine to be used (default: 'smn'). 'smn' split signal into 'speech', 'music' and 'noise' (better). 'sm' split signal into 'speech' and 'music' and do not take noise into account, which is either classified as music or speech. Results presented in ICASSP were obtained using 'sm' option")
parser.add_argument('-g', '--detect_gender', choices = ['true', 'false'], default='True', help="(default: 'true'). If set to 'true', segments detected as speech will be splitted into 'male' and 'female' segments. If set to 'false', segments corresponding to speech will be labelled as 'speech' (faster)")


# Duck's : Additional argument to how many files you would deal with : e.g) 100, 300, 1833...
# parser.add_argument('-num', '--num_episodes', choices=['10', '100', '500', '1000', '1500', '1833'], default='1', help="Number of episodes you want to analyze, always starting from the media file '1.mp3'.")


args = parser.parse_args()
# Preprocess arguments and check their consistency
input_files = []
media_path = '/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media'
#indexing_data.indexing(args.input_dir)
# Duck's : put media files(mp3) into media folder! -> automatically add them to input_files
#for i in range(1, int(args.num_episodes)):
#	input_files += media_path + '%s.mp3' % i

for file in os.listdir(args.input_dir):
	if str(file).endswith('.mp3'):
		input_file = args.input_dir + str(file)
		input_files.append(input_file)

# For debugging purposes
#print(input_files)
# sys.exit()

# Uncomment this section if you want to manually add files in command line
#for e in args.input:
#    input_files += glob.glob(e)
assert len(input_files) > 0, 'No existing media selected for analysis! Bad values provided to -i (%s)' % args.input

odir = args.output_directory
assert os.access(odir, os.W_OK), 'Directory %s is not writable!' % odir

# Do processings
from inaSpeechSegmenter import Segmenter, seg2csv

# load neural network into memory, may last few seconds
detect_gender = bool(distutils.util.strtobool(args.detect_gender))
seg = Segmenter(vad_engine=args.vad_engine, detect_gender=detect_gender)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    
    for i, e in enumerate(input_files):
        print('processing file %d/%d: %s' % (i+1, len(input_files), e))
        base, _ = os.path.splitext(os.path.basename(e))
        seg2csv(seg(e), '%s/%s.csv' % (odir, base))
