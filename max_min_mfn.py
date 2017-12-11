import os
import sys

def max_min(path):
	max,min=[],[]
	_x,_n=[],[]
	f=open(path,'r')
	lines=f.readlines()
	f.close()

	ref=0
	for line in lines:
		if ref==1 or ref==2:
			ref+=1
		if ref==3:
			l=line.strip().split()
			if len(l)==0:
				ref=0
				continue
			if '*' in line:
				l=l[1:]
				_n.append([l[2],l[4:7]])
			min.append([l[2],l[4:7]])
		if ref==5 or ref==6:
			ref+=1
		if ref==7:
			l=line.strip().split()
			if len(l)==0:
				break
			if '*' in line:
				l=l[1:]
				_x.append([l[2],l[4:7]])
			max.append([l[2],l[4:7]])
		if 'The number of surface minima' in line:
			ref=1
		if 'The number of surface maxima' in line:
			ref=5
	return max,min,_x,_n

print max_min(sys.argv[1])
