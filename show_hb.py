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
	typ=set()
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
					st+=[[line.strip().split()[0],l[6],l[8],l[-1]]]
					typ.add(l[-1])
				else:
					l=line.strip().split()
					st+=[[line.strip().split()[0],l[2],l[4],l[-1]]]
					typ.add(l[-1])
			else:
				#for acceptor-hydrogen calculation
				s,e=line.index('('),line.index(')')
				l=line[s+1:e].split(',')
				st+=[[line.strip().split()[0],l[0],l[1],line.strip().split()[-1]]]
				#print st[-1]
				typ.add(line.strip().split()[-1])
			
	return st,typ

#send .txt path
def selection_(path):
	ids,typs=get_ids(path,'_ah')
	sel=[]
	for [h,i,j,t] in ids:
		t=t.replace('(','_')
		t=t.replace(')','_')
		if i not in sel:
			sel.append(i.strip())
			cmd.select(i.strip(),'id '+i.strip())
		if j not in sel:
			sel.append(j.strip())
			cmd.select(j.strip(),'id '+j.strip())
		cmd.distance(t,i.strip(),j.strip())
	col=['red','green','blue','yellow','cyan','white','orange','grey']
	typs=list(typs)
	print typs
	for i in range (len(typs)):
		t=typs[i]
		t=t.replace('(','_')
		t=t.replace(')','_')
		cmd.set('dash_color',col[i],t)
	for i in sel:
		cmd.delete(i)
		

selection_('/Users/47510753/Downloads/6gn4.txt')
if __name__=='__main__':
	selection_('/Users/47510753/Desktop/To-Niraj/test2/1r4g-qm5.txt')
	#selection_(sys.argv[1])
