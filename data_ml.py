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

def save_coord(file,index):
	li=[]
	ref=0
	for i in range (index,len(file)):
		#print file[i]
		if ref==3:
			break
		if '-------------' in file[i]:
			ref+=1
		elif ref==2:
			#print file[i]

			an=file[i].strip().split()[1]
			c=map(float,file[i].strip().split()[3:])
			li.append([float(an)]+c)
	
	return li


def coord(path):
	file_o = open(path,'r')
	file=file_o.readlines()
	file_o.close()
	energy=[]
	lowest_energy=99999
	bl=[]
	ref=0
	last=0.0
	key="Normal "
	index=0
	for line in file:
		#print line
		if key in line:
			energy.append(last)
			
		if 'Standard orientation:' in line:
			last=save_coord(file,index)
			#print last
		index+=1
	#extract_data(energy)
	return energy[0] 


#move(extract_data(path))

#print coord(sys.argv[1])

def get_coord(path):
	data = subprocess.check_output('gcartesian '+path, shell=True).split('\n')[1:]
	lis=[]
	for i in data[:-1]:
		lis.append(map(float,i.split()))
	return lis 

def get_Xy(path):
	X,y,file=[],[],[]
	d=np.load('/'.join(sys.argv[0].split('/')[:-1])+'/acid_data/pka.npy').item()
	for i in os.listdir(path):
		if i[-8:]=='.g16.out':
			X.append(preprocessing.process(coord(i),[100,100]))
			#preprocessing.make_image(preprocessing.process(coord(i),[100,100]),i.split('.')[0])
		 	y.append([float(d[i.split('.')[0]])])
		 	file.append(i.strip().split()[0])
	return np.array(X),np.array(y),file


def prin(X,y,file):
	t=100
	clf = MLPRegressor(solver='lbfgs',activation='relu',hidden_layer_sizes=(100,100,))
	#clf = LinearRegression()
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.1)
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

def flat_X(X):
	X_new=[]
	for i in X:
		X_new.append(i.flatten())
	return np.array(X_new)


X,y,file=get_Xy(sys.argv[1])
X=flat_X(X)
X=ps.scale(X)

#print len(file)

prin(X,y,file)










