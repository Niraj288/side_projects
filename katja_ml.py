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

def D_coord(index):
	d=np.load('/Users/47510753/Downloads/katja_data.npy').item()
	#d=np.load('/users/nirajv/data/katja_data.npy').item()
	dic=read_inp()
	print dic 
	#X,y=get_Xy()
	#d['X']=X 
	#np.save('katja_data.npy',d)
	X,y=d['X'],d['y']
	X,y=get_rand(X,y,int(dic['size']))
	X=add_electron(X,dic)
	X=process(X,[10,10],1)
	X_new=[]
	ma,mi=-99999,99999
	coords=[]
	for i in range (len(X)):
		for j in range (len(X[i])):
			for k in range (len(X[i][j])):
				for l in range (len(X[i][j][k])):
					coords.append([X[i][j][k][l],j,k,l]) 
					if ma<X[i][j][k][l]:
						ma=X[i][j][k][l]
					if mi>X[i][j][k][l]:
						mi=X[i][j][k][l]
	M=1+ma-mi
	f=open('3D.xyz','w')
	for i in range (len(coords)):
		coords[i][0]=((-mi+0.1+coords[i][0])/M)*0.5+0.01
		f.write(' '.join(map(str,coords[i]))+'\n')
	f.close()
	return coords
	


def get_Xy():
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
	return li,energy[0]

def prin2(X_train, y_train, X_test, y_test,dic):
	t=100
	clf = MLPRegressor(solver=dic['solver'],activation=dic['activation'],hidden_layer_sizes=eval(dic['hls']), batch_size = dic['batch_size'], max_iter=dic['max_iter'])
	#clf = LinearRegression()
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
	print 'Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y_test)):
		if y_test[i]==0.0:
			y_test[i]=0.0000001
		predi=str(round(((pr[i]-y_test[i])/y_test[i])*100,2))+' %'
		print ' '*(20-len(predi))+ predi, ' '*(20-len(str(y_test[i])))+str(y_test[i]) , ' '*(20-len(str(round(pr[i],2))))+str(round(pr[i],2)),' '*(20-len(str(round((y_test[i]-pr[i]),4))))+str(round((y_test[i]-pr[i]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	return MAE

def validate(X,y,dic):
        kf = KFold(n_splits=5, random_state=True, shuffle=True )
        ref=0
        for train,test in kf.split(y):
                a=np.array([X[i] for i in train])
                b=np.array([y[i] for i in train])
                c=np.array([X[i] for i in test])
                d=np.array([y[i] for i in test])
                ref+=prin2(a,b,c,d,dic)
        print 'cross validation MAE',ref/5
        return ref/5

def prin(X,y,file,dic):
	t=100
	clf = MLPRegressor(solver=dic['solver'],activation=dic['activation'],hidden_layer_sizes=eval(dic['hls']), batch_size = dic['batch_size'], max_iter=dic['max_iter'])
	#clf = LinearRegression()
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=float(dic['test_size']))
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
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y_test)):
		if y_test[i]==0.0:
			y_test[i]=0.0000001
		predi=str(round(((pr[i]-y_test[i])/y_test[i])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y_test[i])))+str(y_test[i]) , ' '*(20-len(str(round(pr[i],2))))+str(round(pr[i],2)),' '*(20-len(str(round((y_test[i]-pr[i]),4))))+str(round((y_test[i]-pr[i]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])
	return MAE


def process(X,size,d3=0):
	print 'processing....'
	t=time.time()
	a,b=size
	X_new=[]
	for i in range (len(X)):
		X_new.append(preprocessing.process(X[i],[a,b],d3))
		#preprocessing.make_image(preprocessing.process(X[i],[12,12]),str(i))
	print 'processing done in',time.time()-t,'seconds'
	if d3:
		return X_new
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
				if int(st0)>0.5*d_v[st[i]]:
					res+=-(d_v[st[i]]-int(st0))
				else:
					res+=int(st0)
	#print atomNumber,st,res 
	return res 

def read_inp():
	f=open(sys.argv[1],'r')
	lines=f.readlines()
	f.close()
	dic={'3D':[]}
	for line in lines:
		if '#' in line or len(line.strip().split())==0:
			continue
		a,b=line.strip().split()
		if '3D'==a:
			dic['3D'].append(b)
		else:
			dic[a]=b 
	return dic

def add_electron(X,dic):
	if len(dic['3D'])==0:
		return X 
	d=atom_data.data(sys.argv[0])
	for i in range (len(X)):
		#print X[i]#d[X[i][0]]#['electronegativity']
		for j in range (len(X[i])):
			for k in dic['3D']:
				if k=='add_valance':
					X[i][j].append(add_valance(d,int(X[i][j][0])))
				elif k=='atomicMass':
					X[i][j].append(float(d[int(X[i][j][0])][k][:4]))
				else:
					X[i][j].append(float(d[int(X[i][j][0])][k]))
			
	
	return X

def get_rand(X,y,t):
	if t==-1:
		return X,y
	random.seed(1286)
	inde= random.sample(range(len(X)),t)
	x1,y1=[],[]
	for i in inde:
		x1.append(X[i])
		y1.append(y[i])
	return x1,y1

def run():
	#d={'X_processed':X,'y':y}
	d=np.load('katja_data.npy').item()
	#d=np.load('/users/nirajv/data/katja_data.npy').item()
	dic=read_inp()
	print dic 
	#X,y=get_Xy()
	#d['X']=X 
	#np.save('katja_data.npy',d)
	X,y=d['X'],d['y']
	X,y=get_rand(X,y,int(dic['size']))
	X=add_electron(X,dic)
	#y=map(lambda x : x*627.51, y)
	X=process(X,[25,25])

	print len(X)
	#X=ps.scale(X)
	#min_max_scaler = MinMaxScaler()
	#X = min_max_scaler.fit_transform(X)

	file=['']*len(X)
	print 'Training ...'
	t=time.time()
	prin(X,y,file,dic)
	#validate(X,y,dic)
	print 'Training done in',time.time()-t,'seconds'

run()
#D_coord(1)














