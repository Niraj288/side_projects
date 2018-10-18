import mdtraj as md
import sys
import numpy as np
import math

def distance(a,b):	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_coord(file,topo,frame=None):
	t=md.load(file,top=topo)
	refe=0
	alld={}
	for frame in range (0,len(t.xyz),10):
		lis=t.xyz[frame]

		d={}
		
		ref=1
		for i in range (0,len(lis),4):
			for j in range (4):
				if j==0:
					d[ref]=['O']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1
				elif j==1 or j==2:
					d[ref]=['H']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1

		alld[refe]=d
		refe+=1 
	return alld

if __name__=='__main__':
	a=sys.argv[1]
	b=sys.argv[2]
	frame=1000

	dic=get_coord(file,topo)[frame]



