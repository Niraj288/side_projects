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

def coord(path,index,d):
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	y1=float(lines[1].strip().split()[index])
	y2=lines[1].strip().split()
	l=int(lines[0])
	X=[]
	for i in range (l):
		a,x,y,z,ml=lines[2+i].strip().split()
		a=int(d[a])
		#print a,x,y,z
		x=x.replace('*^','e')
		y=y.replace('*^','e')
		z=z.replace('*^','e')
		X.append(map(float,[a,x,y,z]))
	return X,y1,y2


def get_Xy(path,index):
	X,y,Y=[],[],[]
	a_d=atom_data.symbol_dict(sys.argv[0])
	for i in os.listdir('.'):
		if i[-4:]=='.xyz':
			x,y1,y2=coord(i,index,a_d)
			X.append(x)
			y.append(y1)
			Y.append(y2)
	return X,np.array(y),Y


def prin(X,y,file):
	t=100
	clf = MLPRegressor(solver='lbfgs',activation='relu')#,hidden_layer_sizes=(3,))
	#clf = LinearRegression()
	X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.001)
	clf.fit(X_train, y_train)

	accuracy = clf.score(X_train,y_train)
	#MSE=clf.mean_squared_error(X_train,y_train)
	print 'accuracy',accuracy,'\n'
	print 'MSE',metrics.mean_squared_error(y,clf.predict(X))
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


#X,y,Y=get_Xy(sys.argv[1],14)
#d={}
#d['X']=X 
#d['y']=Y 
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
			X[i][j].append(d[int(X[i][j][0])]['vanDelWaalsRadius'])
			X[i][j].append(d[int(X[i][j][0])]['atomicRadius'])
			X[i][j].append(add_valance(d,int(X[i][j][0])))
	
	return X


d=np.load('rubb_data.npy').item()
#X,y=d['X'],[float(xi[16]) for xi in d['y'] ]
for i in range (1):
	print i
	t=1000
	#X,y=d['X'][:-2000],[float(xi[i])*627.51 for xi in d['y'][:-2000] ]
	X,y=d['X'][:t],[float(xi[5])*627.51 for xi in d['y'][:t] ]
	X=add_electron(X)
	'''
	train=X
	clf = IsolationForest(max_samples = 100, random_state = 42)
	clf.fit(train)
	y_noano = clf.predict(train)
	y_noano = pd.DataFrame(y_noano, columns = ['Top'])
	y_noano[y_noano['Top'] == 1].index.values

	train = train.iloc[y_noano[y_noano['Top'] == 1].index.values]
	train.reset_index(drop = True, inplace = True)
	print("Number of Outliers:", y_noano[y_noano['Top'] == -1].shape[0])
	print("Number of rows without outliers:", train.shape[0])
	
	for j in range (len(y)):
		if y[j] > 30000:
			print y[j],j
	'''
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
	









