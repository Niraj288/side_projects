import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import copy

def get_torsion(s,y):
	lis=[]
	for i in range (len(y[0])):
		#print len(y[:,i]),len(s)
		g1=np.gradient(y[:,i],s)
		g2=np.gradient(g1,s)
		lis.append(g2)
		'''
		break
		lis.append([])
		x1=np.gradient(y[i][:,0],x)
		x2=np.gradient(x1)
		x3=np.gradient(x2)
		#print len(x1)
		y1=np.gradient(y[i][:,1],x)
		y2=np.gradient(y1)
		y3=np.gradient(y2)

		z1=np.gradient(y[i][:,2],x)
		z2=np.gradient(z1)
		z3=np.gradient(z2)

		for j in range (len(x)):
			t=x3[j]*(y1[j]*z2[j]-y2[j]*z1[j])+y3[j]*(x2[j]*z1[j]-x1[j]*z2[j])+z3[j]*(x1[j]*y2[j]-x2[j]*y1[j])/((y1[j]*z2[j]-y2[j]*z1[j])**2+(x2[j]*z1[j]-x1[j]*z2[j])**2+(x1[j]*y2[j]-x2[j]*y1[j])**2)
			lis[-1].append(t)
	
		#lis.append(np.linalg.norm(np.inner(np.cross(g1,g2),g3)/np.linalg.norm(np.cross(g1,g2))))
		'''
	bt_vec=[]
	for i in range (len(y)):
		t_vec=[]
		for j in range (len(y[0])):
			t_vec.append(lis[j][i])
		mag=np.linalg.norm(t_vec)
		#mag=np.linalg.norm(t_vec/mag)
		bt_vec.append(mag)
	#print mag
	return np.array(bt_vec)

def fit_points(x,y):
	lis=[]
	for i in range (len(y[0])):
		#plt.plot(x,y[:,i],'ro')
		#y_temp=filter(x,y[:,i],2)
		lis.append(y[:,i])
		#plt.plot(x,y_temp)
		#plt.show()
	lis2=[]
	x_new = np.linspace(x[0], x[-1], len(x)*5)
	for i in lis:
		z=np.polyfit(x,i,3)
		f=np.poly1d(z)
		y_new = f(x_new)
		lis2.append(y_new)
	lis3=[]
	for i in range (0,len(lis2),3):
		lis3.append([])
		for j in range (len(lis2[0])):
			lis3[-1].append([lis2[i][j],lis2[i+1][j],lis2[i+2][j]])
	
	return np.array(x_new),np.array(lis3)

def extract_coord(line):
        lis=[]
        st=''
        ref=0
        count=0
        line=line.replace('D','E')
        for i in line:
                if i==' ':
                        if len(st)!=0:
                                lis.append(st)
                        st=''
                elif i=='-' and line[count-1]!='E':
                        if len(st)!=0:
                                lis.append(st)
                        st='-'
                else:
                        st+=i
                count+=1
        if len(lis)<3:
                lis.append(st)
        lis=map(float,lis)
        return lis

def filter(x,y,h):
	print 'printing'
	plt.plot(x,y,'ro')
	lis=copy.copy(y)
	for i in range (len(x)-h-1):
		ym=max(y[i+1:i+h+1])
		jump,jump2=ym-y[i],ym-y[i+h+1]
		delta_y=y[i+h+1]-y[i]
		if  ((jump>0 and jump2>0) or (jump<0 and jump2<0)) :#and 1 or ym<100*delta_y:
			#print delta_y,x[i],i,ym,jump,jump2
			ref=1
			for j in range (i+1,i+h+1):
				lis[j]=y[i]+ref*delta_y/(h+1) 
				ref+=1
	plt.plot(x,lis)
	plt.show()
	return lis 
		

def data(path):
	f=open(path,'r')
	lines=f.readlines()
	f.close()

	ref=0
	atoms,coord,E=[],[],[]
	x=[]
	for line in lines:
		if 'BL,Alpha,Beta' in line or 'FX_ZMat_Orientation' in line or 'END' in line:
			ref=2
		if ref==3:
			st=line.strip()
			coord[-1]+=extract_coord(st)
		if ref==1 and 'BL,Alpha,Beta' not in line:
			atoms.append(line.strip().split()[0])
		if ref==4:
			line=line.replace('D','E')
			kl=line.strip().split()
			x.append(float(kl[-1]))
			E.append(float(kl[1]))
		if 'CC'==line.strip().split()[0]:
			ref=3
			coord.append([])
		if 'XXIRC' in line:
			ref=4
		if 'IAnZ' in line and ref==0:
			ref=1
	M=0
	for i in atoms:
		M+=int(i)
	M=math.sqrt(M)
	for i in range (len(coord)):
		for j in range (len(coord[i])):
			coord[i][j]=M*coord[i][j]
	return np.array(x),np.array(coord),np.array(E)


s,y,E=data(sys.argv[1])
t=get_torsion(s,y)
plt.plot(s,t,'r-')
#plt.plot(s,E,'g-')
plt.show()

#s=range(1,6)
#y=np.array([[1,2,3],[2,3,4],[3,4,5],[10,4,5],[4,50,6]])
'''
y1=y[:,1]
plt.plot(s,y1,'o')



x1,y1=fit_points(x,y)
Y=get_torsion(x1,y1)
a,b,c=Y 
print len(y[:,1])
col=['r-','b-','g-','v-']
ref=0	
for i in Y:
	plt.plot(x1,i,col[ref])
	ref+=1

#plt.plot(x1,y1[0][:,2],'g-',x,y[:,2],'ro')
plt.show()
'''

