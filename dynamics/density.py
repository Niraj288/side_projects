import mdtraj as md
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd


def get_density(file,topo,frame=None):
	#print 'smthing'
	t=md.load(file,top=topo)
	refe=0
	pb = list(t.unitcell_lengths)
	dn = md.density(t)
	dens = []

	for frame in range (0,len(t.xyz),100):
		dens.append(dn[refe])

		refe+=1 

	avg_density = sum(dens)/len(dens) 

	return avg_density

def visual(res):

	d = np.load(res).item()
	'''
	d2 = np.load(res[:-4]+'0.npy').item()

	for i in d2:
		d[i] = d2[i]

	#print d
	'''

	lis = [[int(i), float(d[i])] for i in d]
	lis.sort()

	for i in lis:
		print  i[0]
	for i in lis:
		print  i[1]

	x_labels = [i[1] for i in lis if i[0]!= 0]
	frequencies = [i[0] for i in lis if i[0]!=0]

	#print file, x_labels[0], frequencies[0]

	#print lis

	plt.figure(figsize=(12, 8))
	freq_series = pd.Series.from_array(frequencies)
	ax = freq_series.plot(kind='bar')
	ax.set_ylabel('Frequency')
	ax.set_xticklabels(x_labels)

	#plt.savefig('density.png')
	#plt.show()
	

def test():
	den = {}
	for i in os.listdir('.'):
		if i[-6:] =='.mdcrd':
			file = i 
			topo = i[:-6]+'.prmtop'
			den[i[-6:]] = get_density(file, topo)

	np.save('density.npy', den)

if __name__=='__main__':
	#test()
	visual(sys.argv[1])



