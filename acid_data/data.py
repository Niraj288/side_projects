import os
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def add_data(data):
	pka=np.load('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy').item()
	ne=np.load(data).item()
	lis=[]
	for i in ne:
		pk=float(raw_input("Enter pka for "+i+' : '))
		pka[i.split('/')[-1].split('.')[0]]=pk
		lis.append([pka[i.split('/')[-1].split('.')[0]],pk])
	for k in lis:
		print ' '.join(map(str,k)) 
	if raw_input('save : ')=='y':
		np.save('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy',pka)


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

def prin(X,y,file):
	clf = LinearRegression() #(n_jobs=processors)

	clf.fit(X[:-2], y[:-2])

	accuracy = clf.score(X,y)
	print 'accuracy',accuracy,'\n'
	eqn='pka = '
	for i in range (len(X[0])):
		eqn+=str(clf.coef_[0][i])+'*Q'+str(i+1)+' + '
	eqn+=str(clf.intercept_[0])
	print eqn,'\n'
	pr=clf.predict(X)
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y)):
		predi=str(round(((pr[i][0]-y[i][0])/y[i][0])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y[i][0])))+str(y[i][0]) , ' '*(20-len(str(round(pr[i][0],2))))+str(round(pr[i][0],2)),' '*(20-len(str(round((y[i][0]-pr[i][0]),4))))+str(round((y[i][0]-pr[i][0]),4))
	#print 'Mean square Error',mean_squared_error(X,pr)
	#print 'R2 score',r2_score(X,pr)
	#test(X,y,file,clf.coef_[0],clf.intercept_[0])



def make_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		a1=(float(a[-1])+float(b[-1]))/2
		b1=float(c[-1]) 
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(d)]]
	prin(X,y,file)
	
def test(data):
	X,y,x=[],[],[]
	file=[]
	for i in data:
		if len(data[i])==5:
			a,b,c,d,e=data[i]
			x+=[[a[-1],b[-1],c[-1],d[-1],e[-1]]]
			file.append(i.split('/')[-1])
			continue
		a,b,c,d,e,f=data[i]
		X+=[[a[-1],b[-1],c[-1],d[-1],e[-1]]]
		y+=[[float(f)]] 
	clf = LinearRegression() #(n_jobs=processors)

	clf.fit(X, y)

	accuracy = clf.score(X,y)
	print 'accuracy',accuracy,'\n'
	pr=clf.predict(x)
	for i in range (len(pr)):
		print file[i]+' '*(20-len(file[i])),pr[i][0]

def amide_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		if 0 and i in ['./mol1H.out','./mol2H.out','./mol3H.out','./mol4H.out','./mol15H.out','./mol16H.out','./mol17H.out','./mol18H.out','./mol19H.out']:
			continue
		file.append(i.split('/')[-1])
		a,b,c,d,e,f=data[i]
		a1,b1=b[-1],e[-1]
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(f)]]
	prin(X,y,file)

def phenol_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		file.append(i.split('/')[-1])
		a,b,f=data[i]
		a1,b1=a[-1],b[-1]
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(f)]]
	prin(X,y,file)

def calc(data):
	pka=np.load('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy').item()
	d=np.load(data).item()
	
	
	ref=0
	for i in d:
		if len(d[i])==4:
			break
		name=i.split('/')[-1].split('.')[0]
		try:
			d[i]=d[i]+[pka[name]]
		except KeyError:
			ref=1
			pka[name]=float(raw_input('Enter pka for '+i+' : '))
			d[i]=d[i]+[pka[name]]

	if ref:
		if raw_input('Save data : ')=='y':
			np.save('/'.join(sys.argv[0].split('/')[:-1])+'/pka.npy',pka)
	#amide_fit(d)
	make_fit(d)
	#phenol_fit(d)
	#test(d)

calc(sys.argv[1])
#add_data(sys.argv[1])








