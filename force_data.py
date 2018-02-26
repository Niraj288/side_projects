import sys

def save_coord(file,index,refe=1):
	e={'14':'Si','1':'H','7':'N','8':'O','6':'C','53':'I','36':'Kr','9':'F'}
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
			if refe==2:
				print file[i]
				an=file[i].strip().split()[1]
				c=map(float,file[i].strip().split()[2:])
				li.append([int(an)]+[c])
			else:
				an=file[i].strip().split()[1]
				c=map(float,file[i].strip().split()[3:])
				li.append([int(an)]+[c])

	return li


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
	return energy,len(forces)

print coord(sys.argv[1])
















