import os
import sys
import numpy as np 
import math
from PIL import Image
from sklearn.linear_model import LinearRegression


def distance(a,b):
	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def distance_M(lis,a,b):
	z1,z2=lis[a][0],lis[b][0]
	r=distance(lis[a][1:4],lis[b][1:4])

	return z1*z2*math.exp(abs(z1-z2)*-r) 

def distance_M2(lis,a,b):
	z1,z2=lis[a][0],lis[b][0]
	r=distance(lis[a][1:4],lis[b][1:4])
	if r==0:
		return 0.5*z1**2.4
	return z1*z2/r

def sort_distance(data,ref):
	lis=[]

	for i in  range (len(data)):
		r=distance(data[i][1:4],ref[1:4])
		if r==0.0:
			lis.append(0.5*data[i][0]**2.4)#data[i][0])
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

def align(data):
	mi=99999999
	for i in data:
		if i[0]<mi:
			mi=i[0]
	if mi<0:
		for i in range (len(data)):
			data[i][0]+=(-mi)+1
	return data 

def flat_X(X):
	X_new=[]
	for j in X:
		X_new.append(j.flatten())
	return np.array(X_new).flatten()
	#return np.array(X_new)

def get_fit(lis,fi):
	z=[]
	c,i=fi
	l=len(c)
	for i in range (len(lis)):
		res=0
		for j in range (len(c)):
			res+=(lis[i][0]**(l-j))*c[j]
		res+=i 
		z.append(res) 
	return z

def process(data_all,size):
	k=len(data_all[0])
	indexes=[0]#[0]
	if k>3:
		indexes+=range(4,k)
	big_li=[]
	#print indexes
	for inde in indexes:
		data=map(lambda x : [x[inde],x[1],x[2],x[3]],data_all)
		data=align(data)
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

		
		for i in range (len(pre_list)):
			pre_list[i][-1]=sum(sort_distance(data,pre_list[i]))
		pre_list=sorted(data,key = lambda x : x[-1])

		distance_matrix=[]
		for i in range (len(pre_list)):
			distance_matrix.append([])
			for j in range (len(pre_list)):
				distance_matrix[-1].append(distance_M2(pre_list,i,j))
		
		eigens=np.linalg.eig(distance_matrix)[0]
		
		#eigens=get_fit(pre_list,fi)
		for i in range (len(eigens)):
			distance_matrix[i][i]=eigens[i]
		
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
	data=[[1,-1,1,0,1.5,0.8],[1,1,1,0,1.6,9],[3,0,2,0,-0.8,8],[4,1,1,1,0.9,7]]
	print process(data,[5,5])
	#make_image(process(data,[12,12]),'0_3.png')



















