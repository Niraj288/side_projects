import sys
import numpy as np 
import math
import atom_data

def save_coord(file,index,refe=1):
	d=atom_data.symbol_dict(sys.argv[0])
	li=[]
	ref=0
	for i in range (index,len(file)):
		#print file[i]
		if ref==3:
			break
		if '-------------' in file[i]:
			ref+=1
		elif ref==2:
			#print file[i]
			try:
				an=file[i].strip().split()[1]
				int(an)
			except ValueError:
				an=d[an]

			if refe==2:
				
				c=map(float,file[i].strip().split()[2:])
				li.append([int(an)]+[c])
			else:
				c=map(float,file[i].strip().split()[3:])
				li.append([int(an)]+[c])

	return li

def distance(a,b):
	res=0
	for i in range (3):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def sort_distance(data,ref):
	lis=[]

	for i in  range (len(data)):
		r=distance(data[i][1:],ref[1:])
		if r==0.0:
			lis.append(0.5*data[i][0]**2.4)#data[i][0])
		else:
			#lis.append(r)
			lis.append((data[i][0]*ref[0])/r)
	lis.sort() 
	return lis

def convert_xy(coord,forces):
	X,y=[],[]
	for i in range (len(coord)):
		for j in range (len(coord[i])):
			X.append(sort_distance(map(lambda x : [x[0]]+x[1],coord[i]),[coord[i][j][0]]+coord[i][j][1]))
			y.append(forces[i][j][1])
	print len(X),len(y)
	return np.array(X),np.array(y)



def coord(path):
	file_o = open(path,'r')
	file=file_o.readlines()
	file_o.close()
	energy,forces=[],[]
	lowest_energy=99999
	bl=[]
	ref=0
	last=0.0
	key="***** Axes restored to original set *****"
	index=0
	for line in file:
		#print line
		if key in line:
			forces.append(save_coord(file,index,2))
			energy.append(last)
			
		if 'Input orientation:' in line:
			last=save_coord(file,index)
			#print last
		index+=1
	return convert_xy(energy,forces)

def add_data(path):
	d=np.load('force_data.npy').item()
	#print d
	k=coord(path)
	d['X']+=k[0]
	d['y']+=k[1]
	np.save('force_data.npy',d)

if __name__=='__main__':
	add_data(sys.argv[1])















