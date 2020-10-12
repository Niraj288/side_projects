import copy
import maya.cmds as cmds
import math
import atom_data as ad
cmds.select(all=1)
cmds.delete()


#f=open('/Users/47510753/Downloads/temp.xyz','r')
def initiate():
    
    
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
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn6SG')
    cmds.connectAttr('blinn6.outColor','blinn6SG.surfaceShader')
    cmds.setAttr('blinn6.transparency',0.50,0.50,0.50)
    cmds.setAttr('blinn6.color',0.,0.0,0.0)
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn7SG')
    cmds.connectAttr('blinn7.outColor','blinn7SG.surfaceShader')
    #cmds.setAttr('blinn6.transparency',0.50,0.50,0.50)
    cmds.setAttr('blinn7.color',0.8,0.8,0.0)
  
    
def make_bond(n1, n2, li1, li2, ref, count, key = 1):
    #global count
    if ref ==1:
        cmds.circle(name = n1+'_c'+str(count), r = 0.08, nr = [0,-1,0])
        cmds.pointConstraint(n1, n1+'_c'+str(count))
        
        count+=1
        cmds.circle(name = n2+'_c'+str(count), r= 0.08, nr = [0,1,0])
        cmds.pointConstraint(n2, n2+'_c'+str(count))
        
        
        cmds.aimConstraint(n1+'_c'+str(count-1), n2+'_c'+str(count), aim = [0.0,1.0,0.0], u = [1.0, 0.0, 0.0])
        #cmds.xform( r=True, ro=(0, 0, 0) )
        cmds.aimConstraint(n2+'_c'+str(count), n1+'_c'+str(count-1), aim = [0.0,1.0,0.0], u = [1.0, 0.0, 0.0])
        #cmds.xform( r=True, ro=(0, 0, 0) )
        
        cmds.loft(n1+'_c'+str(count-1), n2+'_c'+str(count), n = n1+n2+'_l', ar = False)
        count+=1
        return count
    elif ref == 2:
        cmds.circle(name = n1+'_c1_'+str(count), r = 0.05, nr = [0,1,0])
        cmds.move(-0.06,0,0)
        cmds.circle(name = n1+'_c2_'+str(count), r= 0.05, nr = [0,1,0])
        cmds.move(0.06,0,0)
        cmds.group(n1+'_c1_'+str(count),n1+'_c2_'+str(count), n = n1+'_c'+str(count))
        cmds.pointConstraint(n1, n1+'_c'+str(count))
        
        count+=1
        cmds.circle(name = n2+'_c1_'+str(count), r= 0.05, nr = [0,1,0])
        cmds.move(-0.06,0,0)
        cmds.circle(name = n2+'_c2_'+str(count), r= 0.05, nr = [0,1,0])
        cmds.move(0.06,0,0)
        cmds.group(n2+'_c1_'+str(count),n2+'_c2_'+str(count), n = n2+'_c'+str(count))
        cmds.pointConstraint(n2, n2+'_c'+str(count))
        
        cmds.aimConstraint(n1+'_c'+str(count-1), n2+'_c'+str(count), aim = [0.0,1.0,0.0])
        cmds.xform( r=True, ro=(0, 0, 0) )
        cmds.aimConstraint(n2+'_c'+str(count), n1+'_c'+str(count-1), aim = [0.0,1.0,0.0])
        cmds.xform( r=True, ro=(0, 0, 0) )
        
        cmds.loft(n2+'_c1_'+str(count), n1+'_c2_'+str(count-1), n = n1+n2+'_l1')
        cmds.loft(n2+'_c2_'+str(count), n1+'_c1_'+str(count-1), n = n1+n2+'_l2')
        count+=1
        return count
    elif ref == 3:
        cmds.circle(name = n1+'_c'+str(count), r = 0.02, nr = [0,-1,0])
        cmds.pointConstraint(n1, n1+'_c'+str(count))
        
        count+=1
        cmds.circle(name = n2+'_c'+str(count), r= 0.02, nr = [0,1,0])
        cmds.pointConstraint(n2, n2+'_c'+str(count))
        
        
        cmds.aimConstraint(n1+'_c'+str(count-1), n2+'_c'+str(count), aim = [0.0,1.0,0.0], u = [1.0, 0.0, 0.0])
        #cmds.xform( r=True, ro=(0, 0, 0) )
        cmds.aimConstraint(n2+'_c'+str(count), n1+'_c'+str(count-1), aim = [0.0,1.0,0.0], u = [1.0, 0.0, 0.0])
        #cmds.xform( r=True, ro=(0, 0, 0) )
        
        cmds.loft(n1+'_c'+str(count-1), n2+'_c'+str(count), n = n1+n2+'_l', ar = False)
        cmds.sets(forceElement='blinn5SG')
        
        #print (key)
        
        #cmds.setKeyframe(v = 1, at = 'visibility', t = key)
        #cmds.setKeyframe(v = 0, at = 'visibility', t = key - 1)
        #cmds.setKeyframe(v = 0, at = 'visibility', t = key + 1)
        count+=1
        return count
    
def distance(li1,li2):
    res=0
    for i in range (len(li1)):
        res+=(li1[i]-li2[i])**2
    return math.sqrt(res)
    
def bonds(coord, atoms):
    global s_data
    count = 0
    for i in range (len(coord)):
        for j in range (i+1,len(coord)):
            x1,y1,z1,x2,y2,z2=coord[i]+coord[j]
            a,b = atoms[int(i%len(coord))], atoms[int(j%len(coord))]
            vdw_r = (float(s_data[a]['vanDelWaalsRadius']) + float(s_data[a]['vanDelWaalsRadius'])) * 0.00529
            dis = distance([x1,y1,z1],[x2,y2,z2])
            #print (a, '-', b, dis, vdw_r)
            if dis < vdw_r:
                
                if a=='C' and b=='O':
                    #arrow(a+str(i)+'_'+b+str(j),[x1,y1,z1],[x1-x2,y1-y2,z1-z2])
                    count = make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2],2, count)
                    
                elif a=='O' and b=='C':
                    
                    #arrow(a+str(i)+'_'+b+str(j),[x2,y2,z2],[x2-x1,y2-y1,z2-z1])
                    count = make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2],2, count)
                else:
                    count = make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2],1, count)
            elif (a in ['H'] and b in ['F', 'N', 'O']) or (b in ['H'] and a in ['F', 'N', 'O']):
                if dis < 2.2 and dis > 1.5:
                    #print (dis)
                    pass
                    #count = make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2],3, count)
    



def make_(atoms, coord):
    
    global s_data
    rad = {}
    for i in s_data:
        if s_data[i]['atomicRadius']:
            #print (s_data[i]['atomicRadius'])
            rad[i] = float(s_data[i]['atomicRadius']) * 0.00529
    
    ref=1
    #rad={'N':.2,'I':.4,'Kr':.3,'O':0.25,'H':0.15,'F':.2,'Si':.25,'C':.2}
    names = []
    for li in range (len(coord)):
        #print li
        x,y,z=coord[li]
        a = atoms[li]
        
        #print a
        cmds.sphere(name=a+str(ref),r=rad[a])
        names.append(a+str(ref))
        cmds.move(float(x),float(y),float(z))
        
        
        
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
        else:
            cmds.sets(forceElement='blinn7SG')
        
        ref+=1
    bonds(coord, atoms)

    return names
    
def update(name, key, new = 0):
    cmds.select(name)
    if new:
        cmds.setKeyframe(v = 0, at = 'visibility', t = key - 1)
    cmds.setKeyframe(v = 1, at = 'visibility', t = key)
    cmds.setKeyframe(v = 0, at = 'visibility', t = key + 1)
    
def hbonds(coord, atoms, key = 1):
    global s_data, dic
    count = 10000
    for i in range (len(coord)):
        for j in range (i+1,len(coord)):
            x1,y1,z1,x2,y2,z2=coord[i]+coord[j]
            a,b = atoms[int(i%len(coord))], atoms[int(j%len(coord))]
            vdw_r = (float(s_data[a]['vanDelWaalsRadius']) + float(s_data[a]['vanDelWaalsRadius'])) * 0.00529
            dis = distance([x1,y1,z1],[x2,y2,z2])
            if (a in ['H'] and b in ['F', 'N', 'O']) or (b in ['H'] and a in ['F', 'N', 'O']):
                if dis < 2.5 and dis > 1.5:
                    n1, n2 = a+str(i+1), b+str(j+1)
                    if n1+n2+'_l' in dic:
                        update(n1+n2+'_l', key, 0)
                    else:
                        dic[n1+n2+'_l'] = 1
                        count = make_bond(a+str(i+1), b+str(j+1),[x1,y1,z1],[x2,y2,z2],3, count, key)
                        update(n1+n2+'_l', key, 1)
    
                    

def render_(names, coord, atoms, key = 1):
    for j in range (len(names)):
        print (coord[j])
        x,y,z=coord[j]
        cmds.select(names[j])
        cmds.move(float(x),float(y),float(z))
        cmds.setKeyframe(t = key)
        
    cmds.select(clear = True)
        
    hbonds(coord, atoms, key)


def get_lis(lines):
    st = []
    for i in range (len(lines)):
        try:
            float(lines[i].strip())
            st.append('')
        except ValueError:
            if lines[i]:
                st[-1] += lines[i]
    atoms = None
    coords = []
    for li in st:
        crds = li.split('\n')[:-1]
        #print (crds)
        status, crds = crds[0], crds[1:]
        crds2 = [list(map(float,j.strip().split()[1:])) for j in crds if j]
        if crds:
            coords.append(crds2)
        if not atoms:
            atoms = [j.strip().split()[0] for j in crds if j]

    return atoms, coords 

def job(file):

    f = open(file,'r')
    lines = f.readlines()
    f.close()

    atoms, coords = get_lis(lines)

    names = make_(atoms, coords[0])
    
    for h in range (len(coords)):
    
        render_(names, coords[h], atoms, h+1)



dic = {}
count = 0
    
a_data = ad.data()
s_data = {}
for i in a_data:
    s_data[a_data[i]['symbol']] = a_data[i]



initiate()

job('/Users/47510753/Downloads/6-6_318_28.xyz')


#cmds.setKeyframe(v = 0, at = 'visibility', t = 5)
    


