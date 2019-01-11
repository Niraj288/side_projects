from sklearn.neural_network import MLPRegressor
import os
import numpy as np
import math
import sys
import preprocessing
import subprocess
import module
import sklearn.preprocessing as ps 
from sklearn import cross_validation, neighbors
import atom_data
import time
from sklearn import metrics
from sklearn.ensemble import IsolationForest
import scipy.io
from sklearn.preprocessing import MinMaxScaler
import random
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import preprocessing_cm
from sklearn.kernel_ridge import KernelRidge

def flat_X(X):
	X_new=[]
	for j in X:
		X_new.append(j.flatten())
	return np.array(X_new)

def get_Xy():
	mat = scipy.io.loadmat('/Users/47510753/Downloads/qm7.mat')
	coord=mat['X']
	print coord.shape
	coord=flat_X(coord)
	energy=mat['T']
	return coord,energy[0]

def prin(X,y):
	t=100
	#clf = MLPRegressor(solver=dic['solver'],activation=dic['activation'],hidden_layer_sizes=eval(dic['hls']), batch_size = dic['batch_size'], max_iter=dic['max_iter'])
	#clf = LinearRegression()
	clf=KernelRidge(kernel ='laplacian', alpha=0.01)
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.01)
	clf.fit(X_train, y_train)
	
	print 'Training size',len(X_train)
	print 'Testing size',len(X_test)
	#scores = cross_val_score(clf, X, y, cv=5)
	#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

	accuracy = clf.score(X_train,y_train)
	print 'accuracy',accuracy,'\n'
	print 'RMSE',math.sqrt(metrics.mean_squared_error(y_test,clf.predict(X_test)))
	MAE=metrics.mean_absolute_error(y_test,clf.predict(X_test))
	print 'MAE',MAE 
	#X_test,y_test=X[-t:],y[-t:]
	#file=file[-t:]
	pr=clf.predict(X_test)
	print '             Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y_test)):
		if y_test[i]==0.0:
			y_test[i]=0.0000001
		predi=str(round(((pr[i]-y_test[i])/y_test[i])*100,2))+' %'
		print ' '*(20-len(predi))+ predi, ' '*(20-len(str(y_test[i])))+str(y_test[i]) , ' '*(20-len(str(round(pr[i],2))))+str(round(pr[i],2)),' '*(20-len(str(round((y_test[i]-pr[i]),4))))+str(round((y_test[i]-pr[i]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	return MAE

X,y=get_Xy()

#prin(X,y)

