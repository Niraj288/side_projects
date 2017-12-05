import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
import maya.cmds as cmds
import maya.mel as mel
cmds.select(all=1)
cmds.delete()

def plot(path):
    d={}
    rad={'I':.4,'Kr':.3,'O':0.2,'H':0.1,'F':.2,'Si':.25,'C':.2,'N':0.18}
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    index=1
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn1SG')
    cmds.connectAttr('blinn1.outColor','blinn1SG.surfaceShader')
    cmds.setAttr('blinn1.color',0,0,0)
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn2SG')
    cmds.connectAttr('blinn2.outColor','blinn2SG.surfaceShader')
    cmds.setAttr('blinn2.color',255,0,0)
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn3SG')
    cmds.connectAttr('blinn3.outColor','blinn3SG.surfaceShader')
    cmds.setAttr('blinn3.color',0,0,255)
    
    cmds.shadingNode('blinn',asShader=True)
    cmds.sets(renderable=True,noSurfaceShader=True,empty=True,name='blinn4SG')
    cmds.connectAttr('blinn4.outColor','blinn4SG.surfaceShader')
    cmds.setAttr('blinn4.color',0,255,0)
    
    for line in lines:
        if len(line.strip().split())==4:
            s,x,y,z=line.strip().split()
            nam=s+str(index)
            d[index]=nam
            cmds.sphere(name=nam,r=rad[s])
            cmds.move(x,y,z)
            if s=='H':
                cmds.sets(forceElement='blinn4SG')
            elif s=='C':
                cmds.sets(forceElement='blinn1SG')
            elif s=='N':
                cmds.sets(forceElement='blinn3SG')
            elif s=='O':
                cmds.sets(forceElement='blinn2SG')
            index+=1
    return d
            
path='/Users/47510753/Desktop/To-Niraj/test/1k43-qm3/1k43-qm3.xyz'

dic=plot(path)
                
def selec(li,d):
    cmds.select(cl=1)
    for i in li:
        cmds.select(d[i],add=1)
              
string=raw_input()
lis=map(int,string.split(','))
selec(lis,dic)

'''
while len(string)>0:
    lis=map(int,string.split(','))
    selec(lis,dic)
    string=raw_input()
'''
  
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
    
    
    
    