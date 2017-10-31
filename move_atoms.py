import maya.cmds as cmds
cmds.select(all=1)
cmds.delete()

rad={'I':.4,'Kr':.3,'O':0.2,'H':0.15,'F':.2,'Si':.25,'C':.2}

def move(d):
    global rad
    for i in range (len(d[0])):
            name_=d[0][i][0]+str(i+1)
            cmds.sphere(name=name_,r=rad[d[0][i][0]])

    for i in range (len(d)):
        li=d[i]
        time_=1*i+2
        for j in range (len(li)):
                a,[x,y,z]=li[j]
                cmds.select(a+str(j+1))
                cmds.move(float(x),float(y),float(z))
                cmds.setKeyframe(time=time_)


def extract_data(lis):
	d={}
	for i in range (len(lis)):
		d[i]=lis[i]
	move(d)

def save_coord(file,index):
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

			an=file[i].strip().split()[1]
			c=file[i].strip().split()[3:]
			li.append([e[an]]+[c])
	
	return li


def coord(path):
	file_o = open(path,'r')
	file=file_o.readlines()
	file_o.close()
	energy=[]
	lowest_energy=99999
	bl=[]
	ref=0
	last=0.0
	key="-- Stationary point found."
	index=0
	for line in file:
		#print line
		if key in line:
			energy.append(last)
			
		if 'Standard orientation:' in line:
			last=save_coord(file,index)
			#print last
		index+=1
	extract_data(energy)
	return energy 


#move(extract_data(path))

coord('/Users/47510753/Desktop/Kr_I2_Kr.g16.out')