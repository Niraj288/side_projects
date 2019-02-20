import mdtraj as md
import sys
import numpy as np
import math
import os

def get_density(file,topo,frame=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	pb = list(t.unitcell_lengths)
	dn = md.density(t)
	dens = []

	for frame in range (0,len(t.xyz),100):
		dens.append(dn[refe])
		print file, frame, dens

		refe+=1 

	avg_density = sum(dens)/len(dens) 

	return avg_density

def test():
	den = {}
	for i in os.listdir('.'):
		if i[-6:] =='.mdcrd':
			file = i 
			topo = i[:-6]+'.prmtop'
			den[i[:-6]] = get_density(file, topo)

	np.save('density.npy', den)

if __name__=='__main__':
	test()




