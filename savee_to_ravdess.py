import os, sys
import argparse
import glob, pickle
import re
from pathlib import Path
from shutil import copyfile

def savee_to_custom(emotions, chosed_emotions):
    for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/savee_data/AudioData/*/*.wav'):
        file_name = os.path.basename(file)
        emotion = re.findall('[a-zA-Z]+', file_name)[0]
        sentence_num = re.findall('\d+', file_name)[0]
        parent_path = Path(file).parent
        parent_folder = re.split('/', str(parent_path))[-1]
        #print(parent_folder)
        ravdess_folder = '/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/ravdess_data/Actor_Savee/'
        ravdess_format = parent_folder + '-' + sentence_num + '-' + emotions[emotion] + '-' + parent_folder + '-' + parent_folder + '-' + parent_folder + '-' + parent_folder + '.wav'
        copyfile(str(file), ravdess_folder+ravdess_format)


def main():
    emotions = {
        'a' : '05', #anger
        'd' : '07', #disgust
        'f' : '06', #fear
        'h' : '03', #happiness
        'n' : '01', #neutral
        'sa' : '04', #sadness
        'su' : '08', #surprise
    }
    
    chosed_emotions = ['neutral' 'angry', 'sad']

    savee_to_custom(emotions, chosed_emotions)


if __name__ == "__main__":
    main()
