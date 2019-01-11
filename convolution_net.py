import preprocessing_bob as ps
import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn import metrics as mt
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Reshape
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
from keras.layers import average 
from keras.models import Input, Model
from keras.layers import average, concatenate
from keras.models import Input, Model
from keras.callbacks import EarlyStopping
from keras.regularizers import l2 
from sklearn.metrics import accuracy_score

def test_arch1():
    NUM_CLASSES = 1
    cnn2 = Sequential()
    #cnn2.add(input_shape=(40,40,1))
    cnn2.add(Conv2D(filters=16, kernel_size= (3, 3), 
                    padding='same', input_shape=(24,7776,1),
                    data_format="channels_last"))
    cnn2.add(Activation('relu'))
    cnn2.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
    # add one layer on flattened output
    cnn2.add(Flatten())
    cnn2.add(Dense(NUM_CLASSES, activation='sigmoid'))

    # Let's train the model 
    cnn2.compile(loss='mean_squared_error',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # we need to exapnd the dimensions here to give the 
    #   "channels" dimension expected by Keras

    return cnn2

def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(13, input_dim=13, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

seed = 7
np.random.seed(seed)
# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=test_arch1, epochs=10, batch_size=50, verbose=1)


'''
d=np.load('/Users/47510753/Downloads/katja_data.npy').item()

X,y=d['X'],d['y']

X = np.array([ps.get_2D(i) for i in X]).reshape(-1,24,7776,1)
y = np.array(y)

np.save('bob_katja_data.npy',{'X':X,'y':y})
'''
d=np.load('/Users/47510753/Downloads/bob_katja_data.npy').item()

X,y=d['X'],d['y']


estimator.fit(X,y)

