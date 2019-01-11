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

def conv(data, bonds):

	size = 529
	big_li = []
	for i in range (len(data)):
		fli = []
		ch = [int(ij[0]) for ij in data[i]]
		ch.sort()
		for j in range (len(data[i])):
			for k in range (j+1, len(data[i])):
				lis = [0]*len(bonds)
				li = [str(data[i][j][0]), str(data[i][k][0])]
				li.sort()
				st = '-'.join(li)
				ind = bonds.index(st)
				r = distance(data[i][j][1:], data[i][k][1:])
				if r == 0:
					lis[ind] = -0.5 * data[i][j][0]**2
				else:
					lis[ind] = -(data[i][j][0] * data[i][k][0])/r 
				fli.append(lis)
		if len(fli) < size:
			lis = [0]*len(bonds)
			for _ in range (size - len(fli)):				
				fli.append(lis)

		big_li.append(fli)

	return np.array(big_li) 





def process(data_all):

	atoms = ['1.0', '3.0', '4.0', '5.0', '6.0', '7.0', '8.0', '9.0', '16.0']
	bonds = []
	for i in range (len(atoms)):
		for j in range (i,len(atoms)):
			li = [atoms[i], atoms[j]]
			li.sort()
			bonds.append('-'.join(li))

	print len(bonds)

	k=len(data_all[0])
	indexes=[0]#[0]
	#if k>3:
	#	indexes+=range(4,k)

	for inde in indexes:
		data=map(lambda x : [x[inde],x[1],x[2],x[3]],data_all)

		con = conv(data, bonds)

	return con


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
	data=[[[1,-1,1,0],[1,1,1,0],[3,0,2,0],[4,1,1,1]],[[1,-1,1,0],[1,1,1,0],[3,0,2,0],[4,1,1,1]]]
	print process(data)
	#make_image(process(data,[12,12]),'0_3.png')



















