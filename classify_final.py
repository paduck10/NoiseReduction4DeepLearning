import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from joblib import dump, load

import random
import argparse
import sys
import re
from pathlib import Path
from shutil import copyfile

#from duck_emotion import extract_feature
# Extract features (mfcc, chroma, mel) from a sound file
# Core part, VVIP function for emotional detector
def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype='float32')
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfcc = np.mean(librosa.feature.mfcc(y = X, sr = sample_rate, n_mfcc = 40).T, axis = 0)
            result = np.hstack((result, mfcc)) # stacks arrays in sequence horizontally(in a columnar fashion)
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr = sample_rate).T, axis = 0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr = sample_rate).T, axis = 0)
            result = np.hstack((result, mel))
        # For datatype checking
        #print('Datatype of extracted feature : %s \n' % str(result.shape))
        #print(result)
        return result



# Load the data and extract features for each sound file
def load_test_data(emotions, observed_emotions):
	x, y = [], []
	files = []
	for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/custom_dataset/Actor_*/*.wav'):
		file_name = os.path.basename(file)
		emotion = emotions[file_name.split("-")[2]]
		if emotion not in observed_emotions:
			continue
		feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
		x.append(feature)
		y.append(emotion)
		files.append(file)
	x = np.array(x)
	#np.reshape(x, (-1, 1))
	#y = np.array(y)
	#return train_test_split(np.array(x), y, test_size=test_size, random_state=9)
	return (x, y, files)

def load_data_files(args, emotions, observed_emotions):
	x, files, file_names = [], [], []
	for file in glob.glob(args.input_dir + '*.wav'):
		file_name = os.path.basename(file)
		feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
		x.append(feature)
		#y.append()
		files.append(file)
		file_names.append(file_name)
	x = np.array(x)
	#np.reshape(x, (-1, 1))
	#y = np.array(y)
	#return train_test_split(np.array(x), y, test_size=test_size, random_state=9)
	return (x, files, file_names)



def main(args, emotions, observed_emotions):

	# Testset test -> Not for actual clustering!
	#testset_feature, testset_label, files = load_test_data(emotions, observed_emotions)

	testset_feature, files, file_names = load_data_files(args, emotions, observed_emotions)

	print('Load data files and directory done!')

	model = MLPClassifier(alpha = 0.01, batch_size = 256, epsilon= 1e-08,
	hidden_layer_sizes = (500000, ), learning_rate = 'adaptive', max_iter=500, warm_start=True, verbose=True, tol=1e-7)

	# Load the checkpoint
	path = args.checkpoint
	model = load(os.path.abspath(path))
	print('Checkpoint loaded at ' + path)

	# Predict for the test set
	print('Tested dataset : total %s.' % testset_feature.shape[0])
	# Angry vs not Angy 
	y_pred = model.predict(testset_feature)
	# 확률값 뽑아주기
	#y_pred_proba = model.predict_proba(testset_feature)

	# Print the tested version accuracy
	#accuracy = accuracy_score(y_true=testset_label, y_pred=y_pred)
	#print("Tested Accuracy with pretrained model: {:.2f}%".format(accuracy*100))

	# Add custom folder to add clustering
	neutral_dir = Path(args.output_dir + 'neutral').mkdir(parents=True, exist_ok=True)
	calm_dir = Path(args.output_dir + 'calm').mkdir(parents=True, exist_ok=True)
	happy_dir = Path(args.output_dir + 'happy').mkdir(parents=True, exist_ok=True)
	sad_dir = Path(args.output_dir + 'sad').mkdir(parents=True, exist_ok=True)
	angry_dir = Path(args.output_dir + 'angry').mkdir(parents=True, exist_ok=True)
	fearful_dir = Path(args.output_dir + 'fearful').mkdir(parents=True, exist_ok=True)
	disgust_dir = Path(args.output_dir + 'disgust').mkdir(parents=True, exist_ok=True)
	surprised_dir = Path(args.output_dir + 'surprised').mkdir(parents=True, exist_ok=True)
	boredom_dir = Path(args.output_dir + 'boredom').mkdir(parents=True, exist_ok=True)

	emotion_dir = {
		'neutral' : str(args.output_dir + 'neutral/'),
		'calm' : str(args.output_dir + 'calm/'),
		'happy' : str(args.output_dir + 'happy/'),
		'sad' : str(args.output_dir + 'sad/'),
		'angry' : str(args.output_dir + 'angry/'),
		'fearful' : str(args.output_dir + 'fearful/'),
		'disgust' : str(args.output_dir + 'disgust/'),
		'surprised' : str(args.output_dir + 'surprised/'),
		'boredom' : str(args.output_dir + 'boredom/'),
	}
	
	#clustering files. Ex) clus-angry-05-FILENAME
	for emotion, file, file_name in zip(y_pred, files, file_names):
		#print(emotion_dir[emotion] + 'clus' + '-' + emotion + '-' + emotions[str(emotion)]  + '-' + file_name)
		file_to_cluster =  emotion_dir[emotion] + 'clus' + '-' + emotion + '-' + emotions[emotion] + '-' + file_name
		copyfile(str(file), file_to_cluster)
		
		print('Clustered %s into %s' % (str(file_name), file_to_cluster))
	
	"""
	# This line is for clustering files to the following : angry-95-05-FILENAME
	for line, file, file_name in y_pred_proba, files, file_names:
		maxProba = int(np.amax(line) * 100)
		maxIndex = int(np.where(line == np.amax(line))[0])
		cluster_emotion = ''
		if maxIndex == 0:
			copyfile(str(file), neutral_dir + 'clus' + '-' + 'neutral' + '-' + maxProba + '-' file_name)
		else:
			copyfile(str(file), angry_dir + 'clus' + '-' + 'angry' + '-' + maxProba + '-' + file_name)
	"""



if __name__== "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--checkpoint', help='Load the trained model for classification', default = '/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/chkpt/pretrained_model.joblib')
	parser.add_argument('-i', '--input_dir', help='Input directory which dataset you want to test lives', default='/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/custom_dataset/')
	parser.add_argument('-o', '--output_dir', help='Output directory to store your clustered files, based on the emotion dectection', default='/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/custom_dataset/clustered/')
	args = parser.parse_args()

	# Emotions in the RAVDESS dataset
	# Use this for clustering
	emotions_rev = {
		'neutral' : '01',
		'calm' : '02',
		'happy' : '03',
		'sad' : '04',
		'angry' : '05',
		'fearful' : '06',
		'disgust' : '07',
		'surprised' : '08',
		'boredom' : '09'
	}

	# Use this for testing
	emotions = {
		'01' : 'neutral',
		'02' : 'calm',
		'03' : 'happy',
		'04' : 'sad',
		'05' : 'angry',
		'06' : 'fearful',
		'07' : 'disgust',
		'08' : 'surprised',
		'09' : 'boredom'
	}



	# To add more emotion for clustering, add emotion in "observed_emotions"
	observed_emotions = ['neutral', 'angry']
	main(args, emotions_rev, observed_emotions)
