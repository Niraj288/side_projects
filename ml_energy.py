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

def get_Xy(path1,path2):
	f=open(path1,'r')
	line=f.readlines()
	f.close()
	g=open(path2,'r')
	line2=g.readlines()
	g.close()

	X,y=[],[]
	ref=0
	for i in line:
		if len(i.strip().split())==0:
			X.append([])
			y.append(float(line2[ref].strip().split()[0]))
			ref+=1
		elif len(i.strip().split())==5:
			x,y1,z,a=i.strip().split()[1:]
			X[-1].append(map(float,[a,x,y1,z]))
	return X,np.array(y)


def prin(X,y,file):
	t=100
	clf = MLPRegressor(solver='lbfgs',activation='relu',hidden_layer_sizes=(1,))
	#clf = LinearRegression()
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.01)
	clf.fit(X_train, y_train)

	accuracy = clf.score(X_train,y_train)
	print 'accuracy',accuracy,'\n'
	#X_test,y_test=X[-t:],y[-t:]
	#file=file[-t:]
	pr=clf.predict(X_test)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y_test)):
		predi=str(round(((pr[i]-y_test[i])/y_test[i])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y_test[i])))+str(y_test[i]) , ' '*(20-len(str(round(pr[i],2))))+str(round(pr[i],2)),' '*(20-len(str(round((y_test[i]-pr[i]),4))))+str(round((y_test[i]-pr[i]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	return pr

def process(X,size):
	a,b=size
	X_new=[]
	for i in range (len(X)):
		X_new.append(preprocessing.process(X[i],[a,b]))
		#preprocessing.make_image(preprocessing.process(X[i],[12,12]),str(i))
	return np.array(X_new)

def flat_X(X):
	X_new=[]
	for i in X:
		X_new.append(i.flatten())
	return np.array(X_new)


X,y=get_Xy(sys.argv[1],sys.argv[2])
X=process(X,[12,12])
X=flat_X(X)
X=ps.scale(X)

print len(X)
file=['']*2000
prin(X,y,file)










