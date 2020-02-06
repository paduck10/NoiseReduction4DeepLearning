import os, sys
import argparse
import glob, pickle
import re
from pathlib import Path
from shutil import copyfile

def emoDB_to_custom(emotions, chosed_emotions):
    for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/emoDB_data/wav/*.wav'):
        file_name = os.path.basename(file)
        emotion = re.findall('[A-Z]', file_name)[0]
        speaker_num = re.findall('\d\d', file_name)[0]
        sentence_num = re.findall('[a-b]\d\d', file_name)[0]
        identifier = re.findall('\w', file_name)[-1]
        parent_path = Path(file).parent
        parent_folder = re.split('/', str(parent_path))[-1]
        #print(parent_folder)
        ravdess_folder = '/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/ravdess_data/Actor_emoDB/'
        ravdess_format = 'emoDB' + '-' + 'emoDB' + '-' + emotions[emotion] + '-' + speaker_num + '-' + sentence_num + '-' + emotions[emotion] + '-' + identifier + '.wav'
        copyfile(str(file), ravdess_folder+ravdess_format)


def main():
    emotions = {
        'W' : '05', #anger
        'E' : '07', #disgust
        'A' : '06', #fear
        'F' : '03', #happiness
        'N' : '01', #neutral
        'T' : '04', #sadness
        'L' : '09', #Boredom
    }
    
    chosed_emotions = ['neutral' 'angry', 'sad']

    emoDB_to_custom(emotions, chosed_emotions)


if __name__ == "__main__":
    main()
