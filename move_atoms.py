import copy
import maya.cmds as cmds
cmds.select(all=1)
cmds.delete()

rad={'N':.2,'I':.4,'Kr':.3,'O':0.2,'H':0.15,'F':.2,'Si':.25,'C':.2}

def move(d):
    global rad
    for i in range (len(d[0])):
            name_=d[0][i][0]+str(i+1)
            cmds.sphere(name=name_,r=rad[d[0][i][0]])

    for i in range (len(d)):
        li=d[i]
        time_=10*i+2
        for j in range (len(li)):
                a,[x,y,z]=li[j]
                cmds.select(a+str(j+1))
                cmds.move(float(x),float(y),float(z))
                cmds.setKeyframe(time=time_)

def rotate_180(lis,axis):
	if axis==0:
		lis=map(lambda x : [x[0],[-x[1][0],x[1][1],x[1][2]]], lis)
	elif axis==1:
		lis=map(lambda x : [x[0],[x[1][0],-x[1][1],x[1][2]]], lis)
	elif axis==2:
		lis=map(lambda x : [x[0],[x[1][0],x[1][1],-x[1][2]]], lis)
	return lis
	
def rotate_90(lis,axis):
    

def update_ref(d,i):
    ref=[0,0,0]
    for j in range (len(d[i])):
                        a0,[x0,y0,z0]=d[i-1][j]
                        a1,[x1,y1,z1]=d[i][j]

                        ref[0]+=abs(float(x1)-float(x0))
                        ref[1]+=abs(float(y1)-float(y0))
                        ref[2]+=abs(float(z1)-float(z0))
    return ref

def filte(d):
    threshold=[0.4,0.4,0.4]
    for i in range (1,len(d)):
                ref=[0,0,0]
                for j in range (len(d[i])):
                        a0,[x0,y0,z0]=d[i-1][j]
                        a1,[x1,y1,z1]=d[i][j]

                        ref[0]+=abs(float(x1)-float(x0))
                        ref[1]+=abs(float(y1)-float(y0))
                        ref[2]+=abs(float(z1)-float(z0))
                least=99999
                l_cord=None
                prev=copy.copy(d[i])
                for a in range (3):
                    for b in range (3):
                        for c in range (3):
                            d[i]=rotate_90(a,b,c)
                            ref=update_ref(d,i)
                            if sum(ref)<least:
                                l_cord=d[i]
                                least=sum(ref)
                            d[i]=prev
                d[i]=copy.copy(l_cord)
                '''
                for k in range (len(ref)):
                    print ref[k]/len(d[i]),k,i
                    if ref[k]/len(d[i])>threshold[k]:
                        #pass
                        d[i]=rotate_180(d[i],k)
                        print map(lambda x : x/len(d[i]),ref)
                        ref=update_ref(d,i)
                        print map(lambda x : x/len(d[i]),ref)
                
                ref=[0,0,0]
                for j in range (len(d[i])):
                        a0,[x0,y0,z0]=d[i-1][j]
                        a1,[x1,y1,z1]=d[i][j]

                        ref[0]+=abs(float(x1)-float(x0))
                        ref[1]+=abs(float(y1)-float(y0))
                        ref[2]+=abs(float(z1)-float(z0))
                
                for k in range (len(ref)):
                    print ref[k]/len(d[i]),k,i
                '''
                        
def extract_data(lis):
        d={}
        for i in range (len(lis)):
                d[i]=lis[i]
        filte(d)

	
	print d
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
			c=map(float,file[i].strip().split()[3:])
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
			
		if 'Input orientation:' in line:
			last=save_coord(file,index)
			#print last
		index+=1
	extract_data(energy)
	return energy 


#move(extract_data(path))

coord('/Users/47510753/Downloads/marek_coord.txt')




