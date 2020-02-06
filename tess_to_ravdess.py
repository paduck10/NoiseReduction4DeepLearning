import os, sys
import argparse
import glob, pickle
import re
from pathlib import Path
from shutil import copyfile

def tess_to_ravdess(emotions, chosed_emotions):
	for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/tess_data/tess_wav/*/*.wav'):
		file_name = os.path.basename(file)
		file_name_split= re.split('_', file_name)
		print(file_name_split)
		speaker = file_name_split[0]
		word = file_name_split[1]
		emotion = file_name_split[2].split('.')[0]
		parent_path = Path(file).parent
		parent_folder = re.split('/', str(parent_path))[-1]
		#print(parent_folder)
		ravdess_folder = '/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/ravdess_data/Actor_TESS/'
		ravdess_format = speaker + '-' + word + '-' + emotions[emotion] + '-' + speaker + '-' + word + '-' + emotions[emotion] + '-' + word + '.wav'
		copyfile(str(file), ravdess_folder+ravdess_format)


def main():
    emotions = {
        'neutral' : '01', #neutral
        'happy' : '03', #happy
        'sad' : '04', #sad
        'angry' : '05', #angry
        'fear' : '06', #fearful
        'disgust' : '07', #disgust
        'ps' : '08', #surprised
    }
    
    chosed_emotions = ['neutral' 'angry', 'sad']

    tess_to_ravdess(emotions, chosed_emotions)


if __name__ == "__main__":
    main()
