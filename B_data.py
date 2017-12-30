import numpy as np 
import matplotlib.pyplot as plt
import xlwt
import sys
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

data=np.load(sys.argv[1]).item()

#data2=np.load('/Users/47510753/Documents/side_projects/B_final.npy').item()
#data['./B_4NH2_5NO2.out']=[['C-O',1.2451,9.976,1571.474],['C-O',1.2419,10.183,1587.718],['O-C-O',130.3039,1.874,906.507],4.19]
#data['./B_4NO2.out']=[['C-O',1.2426,10.12,1582.785],['C-O',1.2426,10.12,1582.785],['O-C-O',130.5321,1.862,904.86],3.43]
#data['./B_4OMe.out']=[['C-O',1.2454,9.986,1572.314],['C-O',1.2454,9.999,1573.321],['O-C-O',129.6075,1.904,910.652],4.5]
np.save(sys.argv[1],data)
def add_pka(data,name):
	data2=np.load(sys.argv[2]).item()
	ne={}
	for i in data:
		a,b=data[i]
		d=data2[i.split('/')[-1].split('.')[0]][-1]
		data[i].append(d)
		ne[i]=data[i]
	print ne,len(ne)
	if raw_input('Save : ')=='y':
		np.save(name,ne)

def make_excel(data,name):
	wb=xlwt.Workbook() 
	sheet = wb.add_sheet('Version1')
	sheet.write(0,0,'Filename')
	sheet.write(0,1,'Qa1')
	sheet.write(0,2,'Qa2')
	sheet.write(0,3,'Qw')
	sheet.write(0,4,'pKa')
	row=1
	for i in data:
		col=0
		a,b,c,d=data[i]
		sheet.write(row,col,i.split('/')[-1])
		sheet.write(row,col+1,str(a[-1]))
		sheet.write(row,col+2,str(b[-1]))
		sheet.write(row,col+3,str(c[-1]))
		sheet.write(row,col+4,str(d))
		row+=1
	wb.save(name)

def plot(data):
	for i in data:
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		avg=(a[-1]+b[-1])/2
		plt.plot(avg,d,'ro')
	plt.show()

def make_fit1(data):

	X,y=[],[]
	file=[]
	#ne={}
	for i in data:
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		#d=data2[i][-1]
		#data[i].append(d)
		#ne[i]=data[i]
		a1=(a[-1]+b[-1])/2
		b1=c[-1] 
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[d]]
		#avg=(a[-1]+b[-1])/2
		#plt.plot(avg,d,'ro')
	'''
	print ne,len(ne)
	if raw_input('Save : ')=='y':
		np.save('B_final.npy',ne)

	plt.show()

	wb.save('Benzoic_acid.xls')
	'''
	#X_train, X_test, y_train, y_test= cross_validation.train_test_split(X,y,test_size=0.0)

	clf = LinearRegression() #(n_jobs=processors)

	clf.fit(X, y)

	accuracy = clf.score(X,y)
	print 'accuracy',accuracy,'\n'
	pr=clf.predict(X)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y)):
		predi=str(round(((pr[i][0]-y[i][0])/y[i][0])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y[i][0])))+str(y[i][0]) , ' '*(20-len(str(round(pr[i][0],2))))+str(round(pr[i][0],2)),' '*(20-len(str(round((y[i][0]-pr[i][0]),4))))+str(round((y[i][0]-pr[i][0]),4))

def make_fit2(data):

	X,y=[],[]
	file=[]
	#ne={}
	for i in data:
		file.append(i.split('/')[-1])
		a,b,d=data[i]
		#d=data2[i][-1]
		#data[i].append(d)
		#ne[i]=data[i]
		a1=float(a[-1])
		b1=float(b[-1])
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(d)]]

	clf = LinearRegression() #(n_jobs=processors)

	clf.fit(X, y)

	accuracy = clf.score(X,y)
	print 'accuracy',accuracy,'\n'
	pr=clf.predict(X)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y)):
		predi=str(round(((pr[i][0]-y[i][0])/y[i][0])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y[i][0])))+str(y[i][0]) , ' '*(20-len(str(round(pr[i][0],2))))+str(round(pr[i][0],2)),' '*(20-len(str(round((y[i][0]-pr[i][0]),4))))+str(round((y[i][0]-pr[i][0]),4))


make_fit1(data)