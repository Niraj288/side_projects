import os
import sys

def make_xyz(path):
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
'''
if len(sys.argv)>1:
	l=[sys.argv[1]]
else:
	l=os.listdir('.')

for i in l:
	if i[-4:]=='.com':
		make_xyz(i)
'''