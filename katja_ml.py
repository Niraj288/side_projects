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
mat = scipy.io.loadmat(sys.argv[1])

atoms=mat['Z']
coord=mat['R']
energy=mat['T']

li=[]

for i in range (len(atoms)):
	li.append([])
	for j in range (len(atoms[i])):
		if atoms[i][j]==0.0:
			break
		#print atoms[i][j],coord[i][j]
		li[-1].append([atoms[i][j]]+list(coord[i][j]))

def prin(X,y,file):
	t=100
	clf = MLPRegressor(solver='lbfgs',activation='relu')#,hidden_layer_sizes=(3,))
	#clf = LinearRegression()
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.001)
	clf.fit(X_train, y_train)

	accuracy = clf.score(X_train,y_train)
	#MSE=clf.mean_squared_error(X_train,y_train)
	print 'accuracy',accuracy,'\n'
	print 'RMSE',math.sqrt(metrics.mean_squared_error(y,clf.predict(X)))
	print 'MAE',metrics.mean_absolute_error(y,clf.predict(X))
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
	print 'processing....'
	t=time.time()
	a,b=size
	X_new=[]
	for i in range (len(X)):
		X_new.append(preprocessing.process(X[i],[a,b]))
		#preprocessing.make_image(preprocessing.process(X[i],[12,12]),str(i))
	print 'processing done in',time.time()-t,'seconds'
	return np.array(X_new)

def flat_X(X):
	X_new=[]
	for i in X:
		X_new.append(i.flatten())
	return np.array(X_new)


def add_valance(d,atomNumber):
	st=d[atomNumber]['electronicConfiguration']
	d_v={'s':2,'p':6,'d':10,'f':18}
	res=0
	for i in range (len(st)-1):

		if st[i] in d_v:
			
			st0=''
			j=i+1 
			while j<len(st):
				#print 'hola',st[j],i
				try:
					int(st[j])
					st0+=st[j]
				except ValueError:
					break
				j+=1
			if d_v[st[i]]>int(st0):
				res+=int(st0)
	#print atomNumber,st,res 
	return res 

def add_electron(X):
	d=atom_data.data(sys.argv[0])
	for i in range (len(X)):
		#print X[i]#d[X[i][0]]#['electronegativity']
		for j in range (len(X[i])):
			X[i][j].append(d[int(X[i][j][0])]['electronegativity'])
			X[i][j].append(float(d[int(X[i][j][0])]['atomicMass'][:3]))
			X[i][j].append(d[int(X[i][j][0])]['electronAffinity'])
			X[i][j].append(d[int(X[i][j][0])]['ionizationEnergy'])
			#X[i][j].append(d[int(X[i][j][0])]['vanDelWaalsRadius'])
			#X[i][j].append(d[int(X[i][j][0])]['atomicRadius'])
			#X[i][j].append(add_valance(d,int(X[i][j][0])))
	
	return X

X=li
X=add_electron(X)
y=energy[0]
#y=map(lambda x : x*627.51, y)
X=process(X,[30,30])
#d['X_processed']=X 
#np.save('rubb_data.npy',d)

print len(X)
X=ps.scale(X)


file=['']*len(X)
print 'Training ...'
t=time.time()
prin(X,y,file)
print 'Training done in',time.time()-t,'seconds'