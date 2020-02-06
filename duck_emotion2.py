from __future__ import print_function, absolute_import, division, print_function, unicode_literals
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

import argparse

# Tensorflow version import
import tensorflow as tf
import matplotlib.pyplot as plt
import random
from tensorflow import keras

# For keras RNN model implementation
# https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

# For Test data set
#from classify import load_test_data


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
def load_data(emotions, observed_emotions, test_size = 0.5):
    x, y = [], []
    for file in glob.glob('/home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/ravdess_data/Actor_*/*.wav'):
        file_name = os.path.basename(file)
        emotion = emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)



#def tf_train(x_train, x_test, y_train, y_test, emotions, observed_emotions):
		

def keras_train(x_train, x_test, y_train, y_test):
    # Keras RNN model is used
    print('Keras RNN model is used')
    
    # Convert array type into numpy array, for keras usage
    # Set Neutral to 0, Angry to 1
    for i in range(len(y_train)):
        if y_train[i] == 'neutral':
            y_train[i] = 0
        elif y_train[i] == 'angry':
            y_train[i] = 1

    for i in range(len(y_test)):
        if y_test[i] == 'neutral':
            y_test[i] = 0
        elif y_test[i] == 'angry':
            y_test[i] = 1

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    # fix random seed for reproducibility
    np.random.seed(7)
    max_length = 180 # length of extracted feature's length
    # Create the model
    embedding_vector_length = 16
    model = Sequential()
    model.add(Embedding(max_length, embedding_vector_length, input_length=max_length))
    model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(100))
    model.add(Dense(1, activation='sigmoid')) # Use sigmoid or ReLU or ArcTangent
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    print(model.summary())
    
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs = 1000, batch_size = 64)

    # Final evaluation of the model
    scores = model.evaluate(x_test, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1]*100))


def scikit_train(x_train, x_test, y_train, y_test, emotions, observed_emotions):
	print('MLPC : Training the model...')

# Scale the data -> feature scaling, for stability
	scaler = StandardScaler()
	scaler.fit(x_train)
	x_train = scaler.transform(x_train)
	x_test = scaler.transform(x_test)

#initialize the Multi Layer Perceptron Classifier

	model = MLPClassifier(alpha = 0.01, batch_size = 256, epsilon= 1e-08,
	hidden_layer_sizes = (500000, ), learning_rate = 'adaptive', max_iter=1, warm_start=True, verbose=True, tol=1e-8)
# layer_size : 500000 -> acc : 65%
# layer_size : 500 -> acc : 47%

# Load the checkpoint
	if args.checkpoint is not None:
		path = os.path.join(os.getcwd(), args.checkpoint)
		#f = open(path, 'wb')
		model = load(path)

# Train the model
	max_iter = 501
	checkpoint_num = 10
	for i in range(max_iter):
		model.fit(x_train, y_train)
		#y_predict_proba = model.predict_proba(x_test)
		#print(y_predict_proba)
		
	dump(model, './chkpt/checkpoint_layer500000_testsize25_{}.joblib'.format(i))

	# Predict for the test set
	y_pred=model.predict(x_test)

	# Calculate the accuracy of our model
	accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

	# Print the accuracy
	print("Final Accuracy: {:.2f}%".format(accuracy*100))

	'''
	# For new test
	x_newtest, x_newtest_label, files = load_test_data(emotions, observed_emotions)
	y_pred = model.predict(x_newtest)

	# Calculate the accuracy of our model
	accuracy = accuracy_score(y_true=x_newtest_label, y_pred=y_pred)

	# Print the accuracy
	print("Custom data's final Accuracy: {:.2f}%".format(accuracy*100))
	'''


def main(args):
    # GPU Number set
    os.environ["CUDA_VISIBLE_DEVICES"]="0"

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

    x_train, x_test, y_train, y_test = load_data(emotions, observed_emotions, test_size = 0.25)

    # Tested emotions :
    print('Observed emotions : ')
    print(observed_emotions)

    # Get the shape of the training and testing datasets
    print('Get the shape of the training and testing datasets :')
    print((x_train.shape[0], x_test.shape[0]))

    print('Dimension of the feature vector')
    print(f'Features extracted: {x_train.shape[1]}')

    if args.keras is True:
        keras_train(x_train, x_test, y_train, y_test)
    else:
        scikit_train(x_train, x_test, y_train, y_test, emotions, observed_emotions)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keras', type=bool, help='Type "-t True" to use RNN model, implemented by keras module. WARNING : It can be only used for binary classification(Neutral VS Anger).', default=False)
    parser.add_argument('-c', '--checkpoint', help='Train your model from the last checkpoint. Pretrained model, with layer-300, iteration-500 on ravdess, savee, emoDB data is ./chkpt/pretrained_model.joblib', required=False)
    args = parser.parse_args()
    main(args)
