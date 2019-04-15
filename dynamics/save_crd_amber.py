import mdtraj as md
import sys
import numpy as np
import math

def distance(a,b):	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_coord_tip4p(file,topo,frames=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	pbc = {}
	pb = list(t.unitcell_lengths)
	for frame in range (0,len(t.xyz),100):
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
				#print list(lis[i+j])

		alld[refe]=d
		pbc[refe] = map(lambda x : x*10, pb[frame])

		refe+=1 
	return alld, pbc

def get_coord_opc(file,topo,frames=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	pbc = {}
	pb = list(t.unitcell_lengths)
	for frame in range (0,len(t.xyz),100):
		lis=t.xyz[frame]
		#print len(lis)
		#break
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
				#print list(lis[i+j])

		alld[refe]=d
		pbc[refe] = map(lambda x : x*10, pb[frame])

		refe+=1 
	return alld, pbc

def get_coord_fb_4p(file,topo,frames=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	pbc = {}
	pb = list(t.unitcell_lengths)
	for frame in range (0,len(t.xyz),100):
		lis=t.xyz[frame]
		#print len(lis)
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
				#print list(lis[i+j])

		alld[refe]=d
		pbc[refe] = map(lambda x : x*10, pb[frame])

		refe+=1 
	return alld, pbc

def get_coord_fb_3p(file,topo,frames=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	pbc = {}
	pb = list(t.unitcell_lengths)
	for frame in range (0,len(t.xyz),100):
		lis=t.xyz[frame]
		#print len(lis)
		#break
		d={}
		
		ref=1
		
		for i in range (0,len(lis),3):
			for j in range (3):
				if j==0:
					d[ref]=['O']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1
				elif j==1 or j==2:
					d[ref]=['H']+map(lambda x: x*10, list(lis[i+j]))
					ref+=1
				#print list(lis[i+j])

		alld[refe]=d
		pbc[refe] = map(lambda x : x*10, pb[frame])

		refe+=1 
	return alld, pbc

def save_data(file,topo):
	name = file.strip().split('.')[0]
	dic = get_coord_tip5p(file,topo)

	np.save(name+'.npy',dic)

	print file, 'saved as', name+'.npy'



def get_coord_tip5p(file,topo,frame=None): # tip5p
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	alld={}
	pbc = {}
	pb = list(t.unitcell_lengths)
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
		pbc[refe] = map(lambda x : x*10, pb[frame])

		refe+=1 
	return alld, pbc

def get_coord(file, topo, frame = None):
	return get_coord_fb_3p(file, topo, frame)

if __name__=='__main__':
	a=sys.argv[1]
	b=sys.argv[2]
	frame=1000

	dic, pbc =get_coord(a,b)




