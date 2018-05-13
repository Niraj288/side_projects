
import maya.cmds as cmds
cmds.select(all=1)
cmds.delete()

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn1SG')
cmds.connectAttr('blinn1.outColor','blinn1SG.surfaceShader')
#cmds.setAttr('blinn1.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn1.color',0.0,0.0,0.0)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn2SG')
cmds.connectAttr('blinn2.outColor','blinn2SG.surfaceShader')
#cmds.setAttr('blinn2.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn2.color',0.0,1.0,0.0)

cmds.shadingNode('blinn',asShader=True)
cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn3SG')
cmds.connectAttr('blinn3.outColor','blinn3SG.surfaceShader')
#cmds.setAttr('blinn3.transparency',0.75,0.75,0.75)
cmds.setAttr('blinn3.color',0.0,0.0,1.0)

rad={'N':.2,'I':.4,'Kr':.3,'O':0.2,'H':0.15,'F':.2,'Si':.25,'C':.2}

def get_data(file):
    return [['C',0,0,0],['N',1,0,0]],[[-1,0,0],[1,0,0]]
    
def arrow(nam,centre,direcn):
    l=.2
    cmds.select(clear=1)
    cmds.cylinder(name=nam+'cy')
    cmds.scale(l,l/10,l/10)
    cmds.polyCone(name=nam+'co',rcp=1,ax=[1,0,0])
    #cmds.rotate(90,0,0)
    cmds.scale(l/4,l/4,l/4)
    cmds.move(l,0,0)
    cmds.select(nam+'cy',add=1)
    cmds.group(name=nam+'_g')
    x,y,z=centre
    angles=map(lambda x: math.degrees(math.atan(x)),direcn)
    
    a,b,c=direcn
    r=math.sqrt(a**2+b**2+c**2)
    if math.sqrt(a**2+b**2)==0:
        b1=90
    else:
        b1=math.degrees(math.atan(c/math.sqrt(a**2+b**2)))
    if a==0:
        c1=90
    else:
        c1=math.degrees(math.atan(b/a))
        
    #print b1,c1
    cmds.rotate(0,-b1,c1)
    b1=(math.pi/180)*b1
    c1=(math.pi/180)*c1
    l=1.5*l
    x1,y1,z1=l*math.cos(b1)*math.cos(c1),l*math.cos(b1)*math.sin(c1),l*math.sin(b1)
    #print x1,y1,z1
    cmds.move(x+x1,y+y1,z+z1)
    
def distance(li1,li2):
    res=0
    for i in range (len(li1)):
        res+=(li1[i]-li2[i])**2
    return math.sqrt(res)
  
def make_bond(nam,li1,li2):
    l=distance(li1,li2)
    cmds.cylinder(n=nam)
    cmds.scale(l/2,0.1,0.1)
    x1,y1,z1,x2,y2,z2=map(float,li1+li2)
    xm,ym,zm=[(x1+x2)/2,(y1+y2)/2,(z1+z2)/2]
    print xm,ym,zm
    cmds.move(xm,ym,zm)
    direcn=[x2-x1,y2-y1,z2-z1]
    a,b,c=direcn
    r=math.sqrt(a**2+b**2+c**2)
    if math.sqrt(a**2+b**2)==0:
        b1=90
    else:
        b1=math.degrees(math.atan(c/math.sqrt(a**2+b**2)))
    if a==0:
        c1=90
    else:
        c1=math.degrees(math.atan(b/a))
        
    #print b1,c1
    cmds.rotate(0,-b1,c1)
    

def bonds(coord):
    for i in range (len(coord)):
        for j in range (i+1):
            a,x1,y1,z1,b,x2,y2,z2=coord[i]+coord[j]
            if distance([x1,y1,z1],[x2,y2,z2])<1.4:
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
        arrow(a+str(ref),[x,y,z],dipole[ref-1])
        ref+=1
    bonds(coord)
        
render_('')
        
    
    






