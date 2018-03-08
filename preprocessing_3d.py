import os
import sys
import numpy as np 
import math

def distance(a,b):
	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_val(data,i,j,d):
	lis=[]
	li=map(float,[data[i][0],data[j][0]])
	li.sort()
	r=distance(data[i][1:4],data[j][1:4])
	if r==0.0:
		lis.append(0.5*data[i][0]**2.4)#data[i][0])
	else:
		#lis.append(r)
		lis.append((data[i][0]*data[j][0])/r)
	d[tuple(li)]+=[lis[-1]]

def align(d,size):
	t=60
	ma=-99999
	for i in d:
		k=d[i] 
		k.sort(reverse=1)
		d[i]=k
		if len(d[i])>ma:
			ma=len(d[i])
	if ma>t:
		print 'Warning : Data loss ',ma,t  
	lis=[]
	a,b=size

	for i in range (1,a):
		for j in range (1,b):
			for k in range (t):
				li=[float(i),float(j)]
				li.sort()
				if k>=len(d[tuple(li)]):
					lis.append(0.0)
				else:
					lis.append(d[tuple(li)][k])
	return np.array(lis)


def process(data,size,d3):
	a,b=size
	d={}
	vs=[]
	for i in range (1,a):
		for j in range (1,b):
			li=[float(i),float(j)]
			li.sort()
			d[tuple(li)]=[]
	for i in range (len(data)):
		for j in range (i+1):
			li=[data[i],data[j]]
			li.sort()
			if li in vs:
				continue
			vs.append(li)
			val=get_val(data,i,j,d)
	return align(d,size)

if __name__=='__main__':
	print process([[1,0,0,0],[2,1,0,0],[1,0,1,0]],[4,4])
