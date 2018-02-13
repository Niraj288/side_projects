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
		r=distance(data[i][1:],ref[1:])
		if r==0:
			lis.append(r)
		else:
			#lis.append(r)
			lis.append((data[i][0]*ref[0])/r**2)
	lis.sort()
	return lis

def make_image(my_list,name):
	pixels=[]
	img = Image.new('L', (len(my_list), len(my_list[0])))
	print (len(my_list), len(my_list[0]))
	for i in range (len(my_list)):
		for j in range (len(my_list[i])):
			if my_list[i][j] in [-1]:
				my_list[i][j]=255
				img.putpixel((i,j),255)
			elif my_list[i][j]==0.0:
				img.putpixel((i,j),0)
			else:
				img.putpixel((i,j),int((my_list[i][j]*1000)%255))	
	img.save(name+'.png')

def process(data,size):
	M=0
	for i in data:
		M+=float(i[0])
	com=[]
	for i in range (1,len(data[0])):
		com.append(sum([x[0]*x[i] for x in data])/M)
	#print 'com is at',com
	
	for i in range (len(data)):
		data[i].append(distance(data[i][1:],com))
	pre_list=sorted(data,key = lambda x : x[-1])
	
	distance_matrix=[]
	for i in pre_list:
		distance_matrix.append(sort_distance(data,i))
	distance_matrix=sorted(distance_matrix,key=lambda x : sum(x))  # make sure you need this!!
	
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
	data=[[1,-1,1,0,2],[1,1,1,0,1],[3,0,2,0,1],[4,1,1,1,1]]
	process(data,[6,6])

