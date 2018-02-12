import os
import sys
import numpy as np 
import math

data=[[1,-1,1,0,2],[1,1,1,0,1],[3,0,2,0,1],[4,1,1,1,1]]

def distance(a,b):
	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)


def sort_distance(data,ref):
	lis=[]
	for i in  range (len(data)):
		r=distance(data[i][1:],ref[1:])
		if r==0:
			lis.append(r)
		else:
			lis.append(r)
			#lis.append((data[i][0]*ref[0])/r**2)
	lis.sort()
	
	return lis



def process(data,size):
	M=0
	for i in data:
		M+=float(i[0])
	com=[]
	for i in range (1,len(data[0])):
		com.append(sum([x[0]*x[i] for x in data])/M)
	print 'com is at',com
	
	for i in range (len(data)):
		data[i].append(distance(data[i][1:],com))
	pre_list=sorted(data,key = lambda x : x[-1])
	
	distance_matrix=[]
	for i in pre_list:
		distance_matrix.append(sort_distance(data,i))
	a,b=size
	a1=len(distance_matrix)
	for i in range (a):
		if i>=a1:
			distance_matrix.append([-1]*a)
		else:
			for j in range (a1-1,b-1):
				distance_matrix[i].append(-1)
	return np.array(distance_matrix)


if __name__=='__main__':
	print process(data,[6,6])
