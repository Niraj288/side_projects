import copy
#import maya.cmds as cmds
import numpy as np
import math
import itertools
import sys
#cmds.select(all=1)
#cmds.delete()



# only for maya purpose !!
def move(d):
    rad={'N':.2,'I':.4,'Kr':.3,'O':0.2,'H':0.15,'F':.2,'Si':.25,'C':.2}
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

def save_cord(d):
    filename='.'.join(sys.argv[1].split('.')[:-1])
    f=open(filename+'_modified.xyz','w')

    print 'Saving xyz as',filename+'_modified.xyz'

    for i in range (len(d)):
        f.write(str(len(d[i]))+'\n')
        f.write('comment line\n')
        for j in range (len(d[i])):
            a,l=d[i][j]
            st=a+' '+' '.join(map(str,l))+'\n'
            f.write(st)
    f.close()

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def rotate(lis,axis,theta):
    li=[]
    for v in lis:
        li.append(list(np.dot(rotation_matrix(axis,theta), v)))
    return li

def operations():
    li1=['a1','a2','a3']
    li2=['0','1','2','3']

    fli=[]
    #l1=list(itertools.combinations(li1,1))
    #l2=list(itertools.permutations(li2,2))

    #l3=list(itertools.chain(itertools.product(l1, l2)))

    # one at a time
    l1=list(itertools.combinations(li1,1))
    for i in l1:
        for j in li2:
            fli+=[zip(i,[j])]


    # two at a time
    l1=list(itertools.combinations(li1,2))
    for i in l1:
        for j in li2:
            for k in li2:
                fli+=[zip(i,[j,k])]

    # three at a time
    l1=list(itertools.combinations(li1,3))
    for i in l1:
        for j in li2:
            for k in li2:
                for l in li2:
                    fli+=[zip(i,[j,k,l])]

    return fli

def distance(a,b):
    res=0
    for i in range (len(a)):
        res+=(a[i]-b[i])**2
    return math.sqrt(res)

def translate(d,i,li3): # ref2 is to move to ref1
    #return li3
    li1,li2=[],[]
    for j in range (len(d[i])):
        a0,l0=d[i-2][j]
        a0,l1=d[i-1][j]
        li1.append(l0)
        li2.append(l1)
    dist_min=99999
    for j in range (len(li1)):
        dist=distance(li1[j],li2[j])
        if dist<dist_min:
            dist_min=dist 
            ref1,ref2=li2[j],li3[j]
            #print dist_min
            #print ref1
            #print ref2

    delta_x,delta_y,delta_z=ref1[0]-ref2[0],ref1[1]-ref2[1],ref1[2]-ref2[2]
    for j in range (len(li3)):
        li3[j]=[delta_x+li3[j][0],delta_y+li3[j][1],delta_z+li3[j][2]]
    return li3
	
def get_min_dev_cord(d,i):
    li1,li2,at1,at2=[],[],[],[]
    for j in range (len(d[i])):
        a0,l0=d[i-1][j]
        a1,l1=d[i][j]
        li1.append(l0)
        li2.append(l1)
        at1.append(a0)
        at2.append(a1)

    #cord= translate(d,i,li2)
    
    def refe(li1,li2):
        ref=[0,0,0]
        for j in range (len(li1)):
            x0,y0,z0=li1[j]
            x1,y1,z1=li2[j]

            ref[0]+=abs(float(x1)-float(x0))
            ref[1]+=abs(float(y1)-float(y0))
            ref[2]+=abs(float(z1)-float(z0))
        return sum(ref)/len(li1)

    mi,cord=99999,li2

    op=operations()
    for j in op:
        #print i
        c_li=copy.copy(li2)
        for k in j:
            a,r=k
            if a=='a1':
                a=[1,0,0]
            elif a=='a2':
                a=[0,1,0]
            else:
                a=[0,0,1]
            r=(math.pi/2)*float(r)
            #print a,r
            c_li=rotate(c_li,a,r)
            
            #if i>1:
            #    c_li=translate(d,i,c_li) # currently not used
            
        res=refe(li1,c_li)
        if res<mi:
            mi=res 
            cord=c_li
    
    for j in range (len(cord)):
        cord[j]=[at2[j],cord[j]]
    #print mi
    return cord 


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
    threshold=[0.1,0.1,0.1]
    for i in range (1,len(d)):
                ref=[0,0,0]
                #print (len(d[i]))
                for j in range (len(d[i])):
                        a0,[x0,y0,z0]=d[i-1][j]
                        a1,[x1,y1,z1]=d[i][j]

                        ref[0]+=abs(float(x1)-float(x0))
                        ref[1]+=abs(float(y1)-float(y0))
                        ref[2]+=abs(float(z1)-float(z0))
                
                #for k in range (len(ref)):
                #print d[i-1][0],'previous'
                #print d[i][0],'current'
                #print ''
                if sum(ref)/len(d[0])>sum(threshold):
                    
                    print 'modifying point',i+1
                    print 'Deviation :',sum(ref)/len(d[0])
                    d[i]=get_min_dev_cord(d,i)
                    #print d[i-1][0]
                    #print d[i][0]
                    print 'Deviation after modification :',sum(update_ref(d,i))/len(d[0])
                    print ''
                
                        
def extract_data(lis):
        d={}
        for i in range (len(lis)):
                d[i]=lis[i]
        #print d
        filte(d)

        save_cord(d)

	
	
	#move(d)

def get_cords_xyz(file,i):
    li=[]
    for i in range (i+2,len(file)):
        #print file[i]
        if len(file[i].strip().split())<4:
            break

        l=file[i].strip().split()
        if len(l)==4:
            li.append([l[0],map(float,l[1:])])
    return li

def coord_xyz(path):
    file_o = open(path,'r')
    file=file_o.readlines()
    file_o.close()
    cords=[]
    i=0
    while i<(len(file)):
        #print file[i]
        if len(file[i].strip().split())==1:
            cords.append(get_cords_xyz(file,i))
            i+=int(file[i].strip().split()[0])+2
        else:
            print 'Warning: Inconsitency in numer of atoms'
            i+=1


    extract_data(cords)


#move(extract_data(path))

coord_xyz(sys.argv[1])

#coord_xyz('/root/Downloads/marek_nassim.xyz')




