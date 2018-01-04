import os
import numpy as np
import sys
from sklearn.linear_model import LinearRegression

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

	clf.fit(X, y)

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

	#test(X,y,file,clf.coef_[0],clf.intercept_[0])



def make_fit(data):
	X,y=[],[]
	file=[]
	data['./Se_3OMe.out']=[['Se-O', 1.6732, 5.279, 825.270], ['Se-O', 1.6727, 5.301, 813.594], ['Se-OOC', 24.4578, 7.353, 361.250 ], 4.65]
	for i in data:
		file.append(i.split('/')[-1])
		a,b,c,d=data[i]
		a1=(float(a[-1])+float(b[-1]))/2
		b1=float(c[-1]) 
		X+=[[a1**2,b1**2,a1*b1,a1,b1]]
		y+=[[float(d)]]
	prin(X,y,file)
	
def test(X,y,file,coef,c):
	print '\nTesting validity ...\n'
	print 'Coefficients are',coef
	print 'Intercept is',c 
	pr=[]
	for li in X:
		res=0
		for j in range (len(li)):
			res+=float(li[j])*coef[j]
		res+=c 
		pr.append([res])
	print 'Filename                 Percentage Error         Actual Value      Predicted Value           Difference\n'
	for i in range (len(y)):
		predi=str(round(((pr[i][0]-y[i][0])/y[i][0])*100,2))+' %'
		print file[i]+' '*(20-len(file[i])),' '*(20-len(predi))+ predi, ' '*(20-len(str(y[i][0])))+str(y[i][0]) , ' '*(20-len(str(round(pr[i][0],2))))+str(round(pr[i][0],2)),' '*(20-len(str(round((y[i][0]-pr[i][0]),4))))+str(round((y[i][0]-pr[i][0]),4))
	print 'Done!!'

def amide_fit(data):
	X,y=[],[]
	file=[]
	for i in data:
		if i in ['./mol1H.out','./mol2H.out','./mol3H.out','./mol4H.out','./mol15H.out','./mol16H.out','./mol17H.out','./mol18H.out','./mol19H.out']:
			continue
		file.append(i.split('/')[-1])
		a,b,c,d,e,f=data[i]
		X+=[[a[-1],b[-1],c[-1],d[-1],e[-1]]]
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

calc(sys.argv[1])
#add_data(sys.argv[1])








