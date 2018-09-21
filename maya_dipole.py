import math
import maya.cmds as cmds
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
cmds.setAttr('blinn4.color',0.8,0.8,0.8)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn5SG')
cmds.connectAttr('blinn5.outColor','blinn5SG.surfaceShader')
cmds.setAttr('blinn5.transparency',0.50,0.50,0.50)
cmds.setAttr('blinn5.color',0.8,0.8,0.8)

rad={'N':.2,'I':.4,'Kr':.3,'O':0.25,'H':0.15,'F':.2,'Si':.25,'C':.2}

def get_data(file):
    f=open('/Users/47510753/Downloads/for-maya-coordinates-example.gjf','r')
    lines=f.readlines()
    f.close()
    coord,dipole=[],[]
    for line in lines:
        #print line
        if len(line)==0:
            continue
        _,x,y,z=line.strip().split()
        x,y,z=map(float,[x,y,z])
        coord.append([_,x,y,z])
        dipole.append([x,y,z])
        
    return coord,dipole
    
def arrow(nam,centre,direcn):
    l=1
    cmds.select(clear=1)
    cmds.cylinder(name=nam+'cy')
    cmds.scale(l,0.1,0.28)
    cmds.polyCone(name=nam+'_co',rcp=1,ax=[1,0,0])
    #cmds.rotate(90,0,0)
    cmds.scale(0.5,0.1,0.5)
    cmds.move(l+0.5,0,0)
    cmds.select(nam+'cy',add=1)
    cmds.group(name=nam+'_g')
    cmds.sets(forceElement='blinn5SG')
    x,y,z=centre
    angles=map(lambda x: math.degrees(math.atan(x)),direcn)
    
    a,b,c=direcn
    r=math.sqrt(a**2+b**2+c**2)
    if a<0:
        a,b,c=-a,-b,-c
    #a,b,c=a/r,b/r,c/r
    #print a,b,c
    if math.sqrt(a**2+b**2)==0.0 and c>0:
        b1=90
    elif math.sqrt(a**2+b**2)==0.0 and c<0:
        b1=-90
    elif c==0:
        b1=0.0
    else:
        #print math.sqrt(a**2+b**2)
        b1=math.degrees(math.atan(c/math.sqrt(a**2+b**2)))
    if a==0 and b>0:
        c1=90
    elif a==0 and b<0:
        c1=-90
    elif b==0:
        c1=0
    else:
        c1=math.degrees(math.atan(b/a))
    print b1,c1
    if c1<=0:
        c1=180+c1
    lant=0
    if a>0 and c<0:
        b1=-(180-b1)
        lant=1
    cmds.rotate(0,-b1,c1)
    b1=(math.pi/180)*b1
    c1=(math.pi/180)*c1
    l=1.5*l
    x1,y1,z1=l*math.cos(b1)*math.cos(c1),l*math.cos(b1)*math.sin(c1),l*math.sin(b1)
    #print x1,y1,z1
    #cmds.move(x+x1,y+y1,z+z1)
    if lant==1:
        cmds.move(x+x1/2-0.438,y+y1/2+0.038,z+z1/2)
    else:
        cmds.move(x+x1/2-0.438,y+y1/2+0.038,z+z1/2)
    
def distance(li1,li2):
    res=0
    for i in range (len(li1)):
        res+=(li1[i]-li2[i])**2
    return math.sqrt(res)
  
def make_bond(nam,li1,li2,ref=1):
    l=distance(li1,li2)
    if ref==2:
        cmds.cylinder(n=nam.split('-')[0]+'_1_'+nam.split('-')[1])
        cmds.scale(l/2,0.05,0.05)
        cmds.move(0,0,0.1)
        cmds.cylinder(n=nam.split('-')[0]+'_2_'+nam.split('-')[1])
        cmds.scale(l/2,0.05,0.05)
        cmds.move(0,0,-0.1)
        #cmds.select(clear=1)
        #cmds.select(nam+'a')
        
        cmds.select(nam.split('-')[0]+'_1_'+nam.split('-')[1],add=1)
        cmds.group(n=nam)
    else:
        
        cmds.cylinder(n=nam)
        cmds.scale(l/2,0.05,0.05)
    cmds.sets(forceElement='blinn4SG')
    if li2[0]>li1[0]:#distance(li1,[0,0,0])> distance(li2,[0,0,0]):
        x2,y2,z2,x1,y1,z1=map(float,li1+li2)
    else:
        x1,y1,z1,x2,y2,z2=map(float,li1+li2)
    xm,ym,zm=[(x1+x2)/2,(y1+y2)/2,(z1+z2)/2]
    #print xm,ym,zm
    cmds.move(xm,ym,zm)
    direcn=[x2-x1,y2-y1,z2-z1]
    a,b,c=direcn
    #print a,b,c
    r=math.sqrt(a**2+b**2+c**2)
    if math.sqrt(a**2+b**2)==0.0 and c>0:
        b1=90
    elif math.sqrt(a**2+b**2)==0.0 and c<0:
        b1=-90
    elif c==0:
        b1=0.0
    else:
        #print math.sqrt(a**2+b**2)
        b1=math.degrees(math.atan(c/math.sqrt(a**2+b**2)))
    if a==0 and b>0:
        c1=90
    elif a==0 and b<0:
        c1=-90
    elif b==0:
        c1=0
    else:
        c1=math.degrees(math.atan(b/a))
    print b1,c1
    if c1<=0:
        c1=180+c1
    if b1>-7 and b1<0:
        b1=-b1
    elif b1>0 and b1<6:
        b1=-b1
    
    #if (x1>0 and x2<0) or (X1<0 and x2>0):
    #    b1=b1
    print b1,c1
    cmds.rotate(0,b1,c1)
    

def bonds(coord):
    for i in range (len(coord)):
        for j in range (i+1):
            a,x1,y1,z1,b,x2,y2,z2=coord[i]+coord[j]
            if distance([x1,y1,z1],[x2,y2,z2])<1.6:
                
                if a=='C' and b=='O':
                    arrow(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x1-x2,y1-y2,z1-z2])
                    make_bond(a+str(i)+'-'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                    
                elif a=='O' and b=='C':
                    
                    arrow(a+str(i)+'_'+b+str(j),[x2,y2,z2],[x2-x1,y2-y1,z2-z1])
                    make_bond(a+str(i)+'-'+b+str(j),[x1,y1,z1],[x2,y2,z2],2)
                else:
                    make_bond(a+str(i)+'-'+b+str(j),[x1,y1,z1],[x2,y2,z2])
                
            
     
    
def render_(file):
    global rad
    coord,dipole=get_data(file)
    ref=1
    for li in coord:
        a,x,y,z=li
        cmds.sphere(name=a+str(ref),r=rad[a])
        cmds.move(float(x),float(y),float(z))
        if a in ['C','Si','Kr']:
            cmds.sets(forceElement='blinn1SG')
        elif a in ['H']:
            cmds.sets(forceElement='blinn2SG')
        else:
            cmds.sets(forceElement='blinn3SG')
        #arrow(a+str(ref),[x,y,z],dipole[ref-1])
        ref+=1
    bonds(coord)
    arrow('dipole',[0,0,0],[0,-1,0])
        
render_('')
        
    
    






