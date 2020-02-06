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
	for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/custom_dataset/*/*.wav'):
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

def clustering_emtions(emotions, observed_emotions):
	x, files = [], []
	for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/custom_dataset/*/*.wav'):
		file_name = os.path.basename(file)
		feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
		x.append(feature)
		#y.append()
		files.append(file)
	x = np.array(x)
	#np.reshape(x, (-1, 1))
	#y = np.array(y)
	#return train_test_split(np.array(x), y, test_size=test_size, random_state=9)
	return (x, files)



def main(args):

	# Emotions in the RAVDESS dataset
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
	#observed_emotions = ['neutral', 'angry', 'sad']

	#testset_feature, testset_label, files = load_test_data(emotions, observed_emotions)
	testset_feature, files = clustering_emotion(emotions, observed_emotions)

	model = MLPClassifier(alpha = 0.01, batch_size = 256, epsilon= 1e-08,
	hidden_layer_sizes = (500000, ), learning_rate = 'adaptive', max_iter=500, warm_start=True, verbose=True, tol=1e-7)

	# Load the checkpoint
	path = args.checkpoint
	model = load(os.path.abspath(path))
	

	# Predict for the test set
	print('Tested dataset : total %s.' % testset_feature.shape[0])
	y_pred = model.predict(testset_feature)
	y_pred_proba = model.predict_proba(testset_feature)
	print(y_pred_proba)
	f = open('predict_proba.txt', 'wb')
	y_p = np.asarray(y_pred_proba, order='C')
	f.write(y_p)
	f.close()
	# Calculate the accuracy of our model
	accuracy = accuracy_score(y_true=testset_label, y_pred=y_pred)

	# Print the accuracy
	print("Tested Accuracy with pretrained model: {:.2f}%".format(accuracy*100))



if __name__== "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--checkpoint', help='Load the trained model for classification', default='/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/chkpt/pretrained_model.joblib')
	args = parser.parse_args()

	main(args)
