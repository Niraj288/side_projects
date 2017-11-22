import os
import sys

def make_fchk(path):
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	s,cord=[],[]
	ref=0
	sym={'14':'Si','1':'H','7':'N','8':'O','6':'C','53':'I','36':'Kr','9':'F'}
	for line in lines:
		if 'Number of symbols in /Mol/' in line:
			break
		if len(line.strip().split())==0:
			continue
		if 'Nuclear charges' in line:
			ref=1
		if ref==1 or ref==2:
			ref+=1
		if ref==3:
			lis=[i.split('.')[0] for i in line.strip().split()]
			s+=lis 
		if 'Current cartesian coordinates' in line:
			ref+=1
		if ref==4 or ref==5:
			ref+=1
		if ref==6:
			lis=[str(float(i[:10])*0.529177) for i in line.strip().split()]
			cord+=lis
		
	cords=[]
	i,ref=0,0
	g=open(path[:-5]+'.xyz','w')
	while i < (len(cord)):
		g.write(sym[s[ref]]+' '+' '.join(cord[i:i+3])+'\n')
		print ' '.join(cord[i:i+3])
		i+=3
		ref+=1
	g.close()

def make_xyz(path):
	if path.split('.')[-1]=='fchk':
		make_fchk(path)
		return 2
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	lis=''
	ref=0
	for line in lines:
		if '#p ' in line:
			ref+=1
		if len(line.strip().split())==0:
			ref+=1
		if ref==6:
			break
		if ref==3 or ref==4:
			ref+=1
		if ref==5:
			lis+=line
	g=open(path[:-4]+'.xyz','w')
	g.write(lis)
	g.close()
	return 1

#make_xyz(sys.argv[1])

'''
if len(sys.argv)>1:
	l=[sys.argv[1]]
else:
	l=os.listdir('.')

for i in l:
	if i[-4:]=='.com':
		make_xyz(i)
'''