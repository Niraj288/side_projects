import maya.cmds as cmds
import numpy as np

#cmds.select(all=1)
#cmds.delete()


path = '/Users/47510753/Desktop/water_ref/stuff/maya_test_temp.txt'

g = open(path)
lines = g.readlines()
g.close()

arr = []

for line in lines:
    k = line.strip().split()
    if len(k) < 1:
        continue
    elif len(k) == 1:
        arr.append([])
    else:
        arr[-1].append(list(map(float,k)))
        
for j in range (len(arr[0])):
    cmds.sphere(n = 'R' + str(j+1) + 'R')
    cmds.move(0,0,j)
    
for i in range (len(arr)):
    for j in range(len(arr[i])):
        x,y,z,r = arr[i][j]
        r = r * 10
        if r > 7:
            r = 0.01
        
        tim = (i+1) * 10
        
        cmds.select('R' + str(j+1) + 'R')
    
        cmds.setKeyframe( v=r, at='scaleX', t = tim)
        cmds.setKeyframe( v=r, at='scaleY', t = tim)
        cmds.setKeyframe( v=r, at='scaleZ', t = tim)
        
        cmds.setKeyframe( v=x, at='translateX', t = tim)
        cmds.setKeyframe( v=y, at='translateY', t = tim)
        cmds.setKeyframe( v=z, at='translateZ', t = tim)
    
