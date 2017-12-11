#pymol code

from pymol import cmd
import os
import sys

def get_ids(path,suffix):
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	ref=0
	st=[]
	for line in lines:
		if ref==5:
			break
		if 'File format' in line:
			ref=1
		if len(line.strip().split())==0 and ref>0:
			ref+=1
		if ref==2 or ref==3:
			ref+=1
		if ref==4:
			if suffix=='_dh':
				
				if '[' in line:
					l=line.strip().split()
					st+=[[line.strip().split()[0],l[6],l[8]]]
				else:
					l=line.strip().split()
					st+=[[line.strip().split()[0],l[2],l[4]]]
			else:
				#for acceptor-hydrogen calculation
				s,e=line.index('('),line.index(')')
				l=line[s+1:e].split(',')
				st+=[[line.strip().split()[0],l[0],l[1]]]
			
	return st

#send .txt path
def selection_(path):
	ids=get_ids(path,'_ah')
	for [h,i,j] in ids:
		print h,'id '+i.strip()+','+j.strip()
		cmd.select(h,'id '+i.strip()+','+j.strip())

selection_('/Users/47510753/Desktop/To-Niraj/test2/1k43-qm3.txt')
if __name__=='__main__':
	selection_('/Users/47510753/Desktop/To-Niraj/test2/1r4g-qm5.txt')
	#selection_(sys.argv[1])
