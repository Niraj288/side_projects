import sys
import scipy.spatial as spatial
import numpy as np
import math


def dict_bonds():
	l = map(str,range (1,19))
	d = {} 
	count = 0
	for i in l:
		for j in l:
			li = map(int,[i,j])
			li.sort()
			if str(li[0])+'-'+str(li[1]) not in d:
				d[str(li[0])+'-'+str(li[1])] = count
				count += 1
	return d 

def distance(a,b):
	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_2D(coord):
	l_d = 18 * 18
	d = dict_bonds()
	dist_dict = {}
	mat = []
	for i in coord:
		lis = []
		mat.append([])
		for j in coord:
			r = distance(i[1:],j[1:])
			if r!=0:
				e = i[0]*j[0]/r
			else:
				e = 0.5 * i[0]**2
			li =map(int,[i[0],j[0]])
			li.sort()
			lis.append([r,e,d[str(li[0])+'-'+str(li[1])]])
		lis.sort()
		
		for i in lis:
			li_ohe = [0]*l_d
			li_ohe[i[-1]] = i[-2]
			mat[-1]+=li_ohe

		for i in range (24-len(lis)):
			li_ohe = [0]*l_d
			mat[-1]+=li_ohe

	for i in range (24-len(coord)):
		li_pad = [0]*24*l_d
		mat.append(li_pad)


	return np.array(mat) 






if __name__ =='__main__':

	coord = [[1,0,0,0],[8,1,0,0],[1,0,1,0]]
	coord = np.array(coord)

	print get_2D(coord).shape

