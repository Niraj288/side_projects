import copy
import maya.cmds as cmds
import math
cmds.select(all=1)
cmds.delete()

f=open('/Users/47510753/Downloads/temp.xyz','r')
rad={'N':.2,'I':.4,'Kr':.3,'O':0.25,'H':0.15,'F':.2,'Si':.25,'C':.2}

atom = {'6':'C', '1':'H', '7':'N', '8':'O', '9':'F'}
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

lines=f.readlines()
f.close()

ref=0
coord = []
for line in lines[2:]:
    if len(line.strip().split())==0:
        break
    a,x,y,z=line.strip().split()
    coord.append([a]+map(float,[x,y,z]))
    
count = 0    
    
def make_bond(n1, n2, li1, li2):
    global count
    cmds.circle(name = n1+'_c'+str(count), r = 0.08)
    cmds.pointConstraint(n1, n1+'_c'+str(count))
    
    count+=1
    cmds.circle(name = n2+'_c'+str(count), r= 0.08)
    cmds.pointConstraint(n2, n2+'_c'+str(count))
    
    cmds.aimConstraint(n1+'_c'+str(count-1), n2+'_c'+str(count), aim = [0.0,1.0,0.0])
    cmds.aimConstraint(n2+'_c'+str(count), n1+'_c'+str(count-1), aim = [0.0,1.0,0.0])
    
    cmds.loft(n2+'_c'+str(count), n1+'_c'+str(count-1), n = n1+n2+'_l')
    count+=1
    
def distance(li1,li2):
    res=0
    for i in range (len(li1)):
        res+=(li1[i]-li2[i])**2
    return math.sqrt(res)
    
def bonds(coord):
    for i in range (len(coord)):
        for j in range (i+1,len(coord)):
            a,x1,y1,z1,b,x2,y2,z2=coord[i]+coord[j]
            if distance([x1,y1,z1],[x2,y2,z2])<1.6:
                
                if 0 and a=='C' and b=='O':
                    #arrow(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x1-x2,y1-y2,z1-z2])
                    make_bond(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                    
                elif 0 and a=='O' and b=='C':
                    
                    #arrow(a+str(i)+'_'+b+str(j),[x2,y2,z2],[x2-x1,y2-y1,z2-z1])
                    make_bond(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                else:
                    make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2])
    
def render_(coord):
    global rad
    ref=1
    for li in coord:
        a,x,y,z=li
        #print a,x,y,z
        cmds.sphere(name=a+str(ref),r=rad[a])
        cmds.move(float(x),float(y),float(z))
        
        '''
        
        if a in ['C','Si','Kr']:
            cmds.sets(forceElement='blinn1SG')
        elif a in ['H']:
            cmds.sets(forceElement='blinn2SG')
            #arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['O']:
            cmds.sets(forceElement='blinn3SG')
            #arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['N']:
            cmds.sets(forceElement='blinn4SG')
            #arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        elif a in ['F']:
            cmds.sets(forceElement='blinn5SG')
            #arrow('dipole'+str(ref),[float(x),float(y),float(z)],dipole[ref-1])
        '''
        ref+=1
    bonds(coord)
    
coord = [['O',0,0,0],['H',1,0,0]]
render_(coord)


'''
cmds.sphere(n = 'O')
cmds.circle(n = 'O_c', nr = [0,1,0])
cmds.pointConstraint('O','O_c')

cmds.sphere(n = 'H')
cmds.move(1,0,0)
cmds.circle(n = 'H_c', nr = [0,1,0])
cmds.pointConstraint('H','H_c')

cmds.aimConstraint('O_c','H_c', aim = [0,1,0])
cmds.aimConstraint('H_c','O_c', aim = [0,1,0])

cmds.loft('O_c', 'H_c')
'''









