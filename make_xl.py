import xlrd
import os
import xlwt
import sys

#give the txt file
def xl(path):
	d={}
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	ref=0
	for line in lines:
		if 'Additional' in line:
			break
		if len(line.strip().split())==0:
			continue
		if 'File format' in line:
			ref+=1
		if ref==1 or ref==2 or ref==3:
			ref+=1
		if ref==4:
			b,bl,ka1,ka2=line.strip().split()[-4:]
			if b in d:
				d[b].append([bl,ka1,ka2])
			else:
				d[b]=[[bl,ka1,ka2]]
	return d 

if __name__ == "__main__":
	print xl(sys.argv[1])

