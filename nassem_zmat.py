
import numpy as np
import math
import atom_data
import sys

def save_coord(file,index,e):
	li=[]
	ref=0
	for i in range (index,len(file)):
		#print file[i]
		if ref==3:
			break
		if '-------------' in file[i]:
			ref+=1
		elif ref==2:
			#print file[i]

			an=file[i].strip().split()[1]
			c=map(float,file[i].strip().split()[3:])
			li.append([e[an]]+[c])
	
	return li


def coord(path):
	file_o = open(path,'r')
	file=file_o.readlines()
	file_o.close()
	energy=[]
	lowest_energy=99999
	bl=[]
	ref=0
	last=0.0
	key="Normal termination of Gaussian"
	index=0
	e0=atom_data.data(sys.argv[0])
	e={}
	for i in e0:
		#print i
		e[str(i)]=e0[i]['symbol']

	for line in file:
		#print line
		if key in line:
			energy.append(last)
			
		if 'Z-Matrix orientation:' in line:
			last=save_coord(file,index,e)
		index+=1
	return energy

def job():
	p=sys.argv[1]
	for i in coord(p)[0]:
		print "{:>3} {:>10} {:>10} {:>10}".format(*[i[0]]+map(str,i[1]))

job()


