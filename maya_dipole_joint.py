import math
import maya.cmds as cmds
import maya.mel as mel
import numpy as np
cmds.select(all=1)
cmds.delete()

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn1SG')
cmds.connectAttr('blinn1.outColor','blinn1SG.surfaceShader')
#cmds.setAttr('blinn1.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn1.color',0.6,0.6,0.6)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn2SG')
cmds.connectAttr('blinn2.outColor','blinn2SG.surfaceShader')
#cmds.setAttr('blinn2.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn2.color',255/255,255/255,255/255)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn3SG')
cmds.connectAttr('blinn3.outColor','blinn3SG.surfaceShader')
#cmds.setAttr('blinn3.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn3.color',255/255,0.0,0.0)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn4SG')
cmds.connectAttr('blinn4.outColor','blinn4SG.surfaceShader')
#cmds.setAttr('blinn4.transparency',0.50,0.50,0.50)
cmds.setAttr('blinn4.color',0.,0.,1.)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn5SG')
cmds.connectAttr('blinn5.outColor','blinn5SG.surfaceShader')
cmds.setAttr('blinn5.transparency',0.50,0.50,0.50)
cmds.setAttr('blinn5.color',0.,0.8,0.8)

rad={'N':.2,'I':.4,'Kr':.3,'O':0.25,'H':0.15,'F':.2,'Si':.25,'C':.2}

atom = {'6':'C', '1':'H', '7':'N', '8':'O', '9':'F'}

def get_coord(lines,count):
	global atom
	coord = []
	for i in range (count,len(lines)):
		if '----------------' in lines[i]:
			break
		l = lines[i].strip().split()

		coord.append([atom[l[1]]]+map(float,l[3:6]))

	return coord



def get_data(file):
    f=open(file,'r')
    lines=f.readlines()
    f.close()
    coord,dipole=[],[]
    ref = 0
    count = 0
    for line in lines:
        #print line
        if len(line.strip().split())==0:
                ref=0
        if 'Dipole orientation:' in line:
                ref=1
                continue
        if ref==1:
                _,x,y,z=line.strip().split()
                ar=np.array(map(float,[x,y,z]))
                x,y,z = ar/np.abs(ar)
                dipole.append([x,y,z])

        if 'Input orientation:' in line:
                coord = get_coord(lines,count+5)

        count += 1
        
    return coord,dipole
    
def arrow(nam,centre,direcn):
    #print centre , direcn
    cmds.select(clear=True)
    cmds.joint(p = (0.,0.,0.), n = nam+'_p')
    cmds.joint(p = tuple(direcn), n = nam+'_c')
    x,y,z = centre
    cmds.select(nam+'_p',r=True)
    cmds.move(x,y,z)
    

    
def distance(li1,li2):
    res=0
    for i in range (len(li1)):
        res+=(li1[i]-li2[i])**2
    return math.sqrt(res)
  
def make_bond(nam,li1,li2,ref=1):
    cmds.select(clear=True)
    cmds.joint(p = tuple(li1), n = nam+'_p')
    cmds.joint(p = tuple(li2), n = nam+'_c')
    cmds.select(clear = True)
    
def make_bond2(nam,li1, li2, ref = 1):
    if distance(li1,[0,0,0])>distance(li2,[0,0,0]):
        li1,li2 = li2,li1
    x1, y1, z1 = li1
    x2 , y2, z2 = li2
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    
    l=distance(li1,li2)
    if ref==2:
        cmds.cylinder(n=nam.split('_')[0]+'_1_'+nam.split('_')[1])
        cmds.scale(l/2,0.05,0.05)
        cmds.move(0,0,0.1)
        cmds.cylinder(n=nam.split('_')[0]+'_2_'+nam.split('_')[1])
        cmds.scale(l/2,0.05,0.05)
        cmds.move(0,0,-0.1)
        #cmds.select(clear=1)
        #cmds.select(nam+'a')
        
        cmds.select(nam.split('_')[0]+'_1_'+nam.split('_')[1],add=1)
        cmds.group(n=nam)
    else:
        
        cmds.cylinder(n=nam)
        cmds.scale(l/2,0.05,0.05)
    
    cmds.move(dx/2+x1,dy/2+y1,dz/2+z1)
    theta = math.degrees(math.atan(dz/dx))
    phi = math.degrees(math.acos(math.sqrt(dx**2+dy**2)/l))
    
    print theta,phi
    cmds.rotate(0,abs(phi),theta)
    
        
    #cmds.curve(n = nam+'_cv', p =[(-l/2,0,0),(l/2,0,0)], d=1)
    
    #cmds.curve(nam+'_cv', p=[tuple(li1),tuple(li2)], d=1, r=True)
    #cmds.xform( cp =True)
    #cmds.select(clear=True)
    
    #cmds.parentConstraint(nam+'_cv',nam)
    #cmds.curve(nam+'_cv', p=[tuple(li1),tuple(li2)], d=1, r=True)
    #cmds.orientConstraint(nam+'_cv',nam)
        

    

def bonds(coord):
    for i in range (len(coord)):
        for j in range (i+1,len(coord)):
            a,x1,y1,z1,b,x2,y2,z2=coord[i]+coord[j]
            if distance([x1,y1,z1],[x2,y2,z2])<1.6:
                
                if a=='C' and b=='O':
                    #arrow(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x1-x2,y1-y2,z1-z2])
                    make_bond(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                    
                elif a=='O' and b=='C':
                    
                    #arrow(a+str(i)+'_'+b+str(j),[x2,y2,z2],[x2-x1,y2-y1,z2-z1])
                    make_bond(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                else:
                    make_bond(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x2,y2,z2])
                
            
     
    
def render_(file):
    global rad
    coord,dipole=get_data(file)#[['C',0.,0.,0.],['O',1.,1.,1.]],[[1.,0.,0.],[0.,1.,0.]]#
    print coord,dipole
    ref=1
    for li in coord:
        a,x,y,z=li
        cmds.sphere(name=a+str(ref),r=rad[a])
        cmds.move(float(x),float(y),float(z))
        
        if a in ['C','Si','Kr']:
            cmds.sets(forceElement='blinn1SG')
        elif a in ['H']:
            cmds.sets(forceElement='blinn2SG')
            arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['O']:
            cmds.sets(forceElement='blinn3SG')
            arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['N']:
            cmds.sets(forceElement='blinn4SG')
            arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['F']:
            cmds.sets(forceElement='blinn5SG')
            arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        ref+=1
    bonds(coord)
    #arrow('dipole',[0,0,0],[0,-1,0])
        
#render_('/Users/47510753/Downloads/chain_NHO/chain.g16.out')

#render_('/Users/47510753/Downloads/5e61_cut.g16.out')

render_('/Users/47510753/Documents/NHO/MP2/CF3_N.g16.out')
        
    
    






