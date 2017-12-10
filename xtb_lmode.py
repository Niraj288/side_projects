#xtb_lmode
import os
import sys
import atom_data

def make_dat(path):
	filename=path[:-4]+'.xyz'
	amass,za,xyz=[],[],[]
	f=open(filename,'r')
	lines=f.readlines()
	f.close()
	data=atom_data.data()
	sym=symbol_dict()
	for line in lines[2:]:
		if len(line.strip().split())==0:
			continue

		s,x,y,z=line.strip().spit()
		atm=data[]





