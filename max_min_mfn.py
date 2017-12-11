import os
import sys
from pymol import cmd

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

def job(path):
	max,min,_x,_n=max_min(path)
	print 'yes'
	for a,[x,y,z] in max:
		if 0 and a==_x[0][0]:
			cmd.pseudoatom(color='tv_magenta',pos=[x,y,z])
		else:
			cmd.pseudoatom(color='tv_red',pos=[x,y,z])
	for b,[x,y,z] in min:
		if 0 and a==_n[0][0]:
			cmd.pseudoatom(color='tv_cyan',pos=[x,y,z])
		else:
			cmd.pseudoatom(color='tv_blue',pos=[x,y,z])

job('/Users/47510753/Documents/outputs/nohup/CF3_Pt_nohup.out')

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


