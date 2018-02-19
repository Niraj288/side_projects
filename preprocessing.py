import os
import sys
import numpy as np 
import math
from PIL import Image


def distance(a,b):
	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)


def sort_distance(data,ref):
	lis=[]
	for i in  range (len(data)):
		r=distance(data[i][1:4],ref[1:4])
		if r==0.0:
			lis.append(data[i][0])#data[i][0])
		else:
			#lis.append(r)
			lis.append((data[i][0]*ref[0])/r)
	lis.sort()
	return lis

def make_image(my_list,name):
	pixels=[]
	img = Image.new('L', (len(my_list), len(my_list[0])))
	print (len(my_list), len(my_list[0]))
	ma=-999999
	for i in range (len(my_list)):
		m=max(my_list[i])
		if m>ma:
			ma=m 

	for i in range (len(my_list)):
		for j in range (len(my_list[i])):
			if my_list[i][j] in [-1]:
				my_list[i][j]=255
				img.putpixel((i,j),255)
			elif my_list[i][j]==0.0:
				img.putpixel((i,j),0)
			else:
				img.putpixel((i,j),int((my_list[i][j]/ma)*255))	
				#print int((my_list[i][j]/ma)*255)
	img.save(name+'.png')


def flat_X(X):
	X_new=[]
	for j in X:
		X_new.append(j.flatten())
	return np.array(X_new).flatten()
	#return np.array(X_new)

def process(data_all,size):
	k=len(data_all[0])
	indexes=[0]#[0]
	if k>3:
		indexes+=range(4,k)
	big_li=[]
	#print indexes
	for inde in indexes:
		data=map(lambda x : [x[inde],x[1],x[2],x[3]],data_all)
		#print data
		M=0
		for i in data:
			M+=float(i[0])
		if M==0:
			M=1
		com=[]
		for i in range (1,4):
			com.append(sum([x[0]*x[i] for x in data])/M)
		#print 'com is at',com
		
		for i in range (len(data)):
			data[i].append(distance(data[i][1:4],com))
		pre_list=sorted(data,key = lambda x : x[-1])
		
		distance_matrix=[]
		for i in pre_list:
			distance_matrix.append(sort_distance(data,i))
		distance_matrix=sorted(distance_matrix,key=lambda x : sum(x))  # make sure you need this!!
		
		a,b=size
		a1=len(distance_matrix)
		for i in range (a):
			if i>=a1:
				distance_matrix.append([0.0]*a)
			else:
				for j in range (a1-1,b-1):
					distance_matrix[i].append(0.0)
		big_li.append(distance_matrix)
	#print np.array(big_li)
	big_li=flat_X(np.array(big_li))
	return np.array(big_li)


if __name__=='__main__':
	'''
	f=open(sys.argv[1],'r')
	lines=f.readlines()
	f.close()
	data=[]
	for i in lines:
		if len(i.strip().split())==4:
			data.append(map(float,i.strip().split()))
	print data
	'''
	data=[[1,-1,1,0,1.5,0],[1,1,1,0,1.6,9],[3,0,2,0,-0.8,8],[4,1,1,1,0.9,7]]
	print len(process(data,[5,5]))
	#make_image(process(data,[12,12]),'0_3.png')



















