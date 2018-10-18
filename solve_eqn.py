import numpy as np
import sys

def get_data(path):
	d=np.load(path).item()
	print 123
	print d
	files=[]
	qa,qw,y=[],[],[]
	for i in d:
		if i.split('/')[-1]=='B_4NO2_5NO2.out':
			continue
		files.append(i.split('/')[-1])
		qa.append((d[i][0][2]+d[i][1][2])/2)
		qw.append(d[i][2][2])
		y.append(d[i][3])

	return [files,qa,qw,y]

def solve(path,inde):
	lis=get_data(path)
	X,Y=[],[]
	for i in range (inde,inde+6):
		qa=lis[1][i]
		qw=lis[2][i]
		x1,x2,x3,x4,x5,x6=qa**2,qw**2,qa*qw,qa,qw,1
		X.append([x1,x2,x3,x4,x5,x6])
		Y.append([lis[3][i]])
	
	x = np.array(X)
	y = np.array(Y)
	c = np.linalg.solve(x, y)		
	return c

def predict(path,inde):
	print path,inde
	coeff=solve(path,inde)
	lis=get_data(path)
	avg_err=0
	for i in range (len(lis[0])):
		name=lis[0][i]
		qa,qw=lis[1][i],lis[2][i]
		y=lis[3][i]
		temp=[qa**2,qw**2,qa*qw,qa,qw,1] 
		res=0
		for j in range (len(coeff)):
			#print temp[j],coeff[j][0]
			res+=(temp[j]*coeff[j][0])
		avg_err+=((res-y)/y)*100
		print name,'predicted,actual',res,y,'; error is',int(((res-y)/y)*100),'%',float(res-y)
	print 'Overall average error : ',int(avg_err/len(lis[0]))
	return int(avg_err/len(lis[0]))

predict(sys.argv[1],0)

'''
maxi,ind=99999,0
for i in range (2,27):
	p=predict(sys.argv[1],i)
	if maxi<p:
		maxi=p
		ind=i 
print maxi,ind
'''








