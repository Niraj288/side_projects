import mdtraj as md
import sys
import numpy as np
import math

def distance(a,b):	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_coord_tip5p(file,topo,frames=None):
	t=md.load(file,top=topo)
	refe=0
	alld={}

	for frame in range (0,len(t.xyz),100):
		lis=t.xyz[frame]
		oxy = lis[range(1,5000,5)]
		h1 = lis[range(4,5000,5)]
		h2 = lis[range(5,5000,5)]

		#print oxy.shape, h1.shape, h2.shape
		d = {}
		for i in range (1000):
			d[i+1] = ['O']+map(lambda x: x*10, list(oxy[i]))

		for i in range (1000):
			d[i+1001] = ['H']+map(lambda x: x*10, list(h1[i]))

		for i in range (1000):
			d[i+2001] = ['H']+map(lambda x: x*10, list(h2[i]))

		alld[frame] = d 

	return alld

def save_data(file,topo):
	name = file.strip().split('.')[0]
	dic = get_coord_tip5p(file,topo)

	np.save(name+'.npy',dic)

	print file, 'saved as', name+'.npy'



def get_coord(file,topo,frame=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	for frame in range (0,len(t.xyz),100):
		lis=t.xyz[frame]

		d={}
		
		ref=1
		for i in range (0,len(lis),5):
			for j in range (5):
				if j==0:
					d[ref]=['O']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1
				elif j==1 or j==2:
					d[ref]=['H']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1
				#print list(lis[i+j])

		alld[refe]=d
		#print d 
		refe+=1 
	return alld

if __name__=='__main__':
	a=sys.argv[1]
	b=sys.argv[2]
	frame=1000

	dic=get_coord_tip5p(a,b)

	print len(dic)



