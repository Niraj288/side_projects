import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
import copy

def PBC(lis,a,b,c):
	x,y,z=lis
	return [x,y,z]
	x=check(x,0,a)
	y=check(y,0,b)
	z=check(z,0,c)
	return [x,y,z]

def angle(a,b,c,e,f,d):
	#print a,b,c
	x1,y1,z1=d[c][1:]
	x2,y2,z2=d[b][1:]
	x3,y3,z3=d[a][1:]
	x4,y4,z4=d[e][1:]
	x5,y5,z5=d[f][1:]
	v1=[x1-x2,y1-y2,z1-z2]
	v2=[x3-x2,y3-y2,z3-z2]
	angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
	a1=min(angle*360/6.28,(2 * np.pi - angle)*360/6.28)
	v3=[x5-x3,y5-y3,z5-z3]
	v4=[x4-x3,y4-y3,z4-z3]
	v5=[x2-x3,y2-y3,z2-z3]
	#print v3,v4
	angle1 = np.arccos(np.dot(v4, v5) / (np.linalg.norm(v4) * np.linalg.norm(v5)))
	a2= min(angle1*360/6.28,(2 * np.pi - angle)*360/6.28)

	angle2 = np.arccos(np.dot(v3, v5) / (np.linalg.norm(v3) * np.linalg.norm(v5)))
	a3= min(angle2*360/6.28,(2 * np.pi - angle)*360/6.28)
	if a1>100 and a2+a3>110:
		return True
	return False

def check(x,a,x_size):
	if (x <  -x_size * 0.5):
		x = x + x_size
	if (x >=  x_size * 0.5):
		x = x - x_size
	return x

def distance(a,b):	
	res=0
	for i in range (len(a)):
		res+=(a[i]-b[i])**2
	return math.sqrt(res)

def get_donars(o,h,o_refe,h_refe,o_boun,h_boun,ab,bb,cb):
    point_tree = spatial.cKDTree(h)
    li_a={}
    le=1.1
    for i in range (len(o)):
        li1=(point_tree.query_ball_point(o[i], le))
        if i in o_boun:
        	for j in o_boun[i]:
        		a,b=j
        		for k in h_boun:
        			for l in h_boun[k]:
        				c,d=l 
        				if b==d and a!=c:
        					if b=='x':
        						hx,hy,hz=h[k]
        						if a=='+':
        							hx+=ab
        						else:
        							hx-=ab
        						if distance(o[i],[hx,hy,hz])<le:
        							li1+=[k]
        					elif b=='y':
        						hx,hy,hz=h[k]
        						if a=='+':
        							hy+=bb
        						else:
        							hy-=bb
        						if distance(o[i],[hx,hy,hz])<le:
        							li1+=[k]
        					elif b=='z':
        						hx,hy,hz=h[k]
        						if a=='+':
        							hz+=cb
        						else:
        							hz-=cb
        						if distance(o[i],[hx,hy,hz])<le:
        							li1+=[k]

        li1=[h_refe[j] for j in li1]
        li_a[o_refe[i]]=li1
    return li_a

def get_acceptors(links_o):
    li_a={}
    for i in links_o:
        for j in links_o[i]:
        	if i not in li_a:
        		li_a[j]=[i]
        	else:
        		li_a[j].append(i)
    return li_a

def result(arr1,arr2,mi,ma,o_boun,h_boun,ab,bb,cb):
    points = arr2
    if len(arr2)==0:
        raise Exception("There are no hydrogen atoms !!")
    point_tree = spatial.cKDTree(points)
    li1,li2=[],[]
    res=[]
    for i in range (len(arr1)):
        #print i
        li1=(point_tree.query_ball_point(arr1[i], ma))
        li2=(point_tree.query_ball_point(arr1[i], mi))
        
        if i in o_boun:
        	for j in o_boun[i]:
        		a,b=j
        		for k in h_boun:
        			for l in h_boun[k]:
        				c,d=l 
        				if b==d and a!=c:
        					hx,hy,hz=arr2[k]
        					if b=='x':
        						if a=='+':
        							hx+=ab
        						else:
        							hx-=ab
        						dist=distance(arr1[i],[hx,hy,hz])
        						if dist<mi:
        							li2+=[k]
        						elif dist<ma:
        							li1+=[k]
        					elif b=='y':
        						if a=='+':
        							hy+=bb
        						else:
        							hy-=bb
        						dist=distance(arr1[i],[hx,hy,hz])
        						if dist<mi:
        							li2+=[k]
        						elif dist<ma:
        							li1+=[k]
        					elif b=='z':
        						if a=='+':
        							hz+=cb
        						else:
        							hz-=cb
        						dist=distance(arr1[i],[hx,hy,hz])
        						if dist<mi:
        							li2+=[k]
        						elif dist<ma:
        							li1+=[k]
		
        res.append([i,list(set(li1)-set(li2))])
    
    return res

def near_boundry(lis,a,b,c):
	x,y,z=lis
	li=[]
	if x>0.5*a-2:
		li.append('+x')
	elif x<-0.5*a+2:
		li.append('-x')
	if y>0.5*b-2:
		li.append('+y')
	elif y<-0.5*b+2:
		li.append('-y')
	if z>0.5*c-2:
		li.append('+z')
	elif z<-0.5*c+2:
		li.append('-z')
	return li

def temp_d():
	file = open('/Users/47510753/Downloads/test-2.pdb','r')
	lines=file.readlines()
	file.close()
	d={}
	ref=1
	inde1,inde2=2,6
	for line in lines:
		if len(line.strip().split())<4:
			continue
		if 'O' in line.strip().split()[inde1]:
			x,y,z=map(float,line.strip().split()[inde2:inde2+3])
			d[ref]=['O',x,y,z]
			ref+=1
		elif 'H'==line.strip().split()[inde1][0]:
			x,y,z=map(float,line.strip().split()[inde2:inde2+3])
			d[ref]=['H',x,y,z]
			ref+=1
	return d
		

def data(file=None):
	'''
	d={1:['O',0,0,0],
	   2:['H',1,0,0],
	   3:['H',0,1,0],
	   4:['O',0,-1.8,0],
	   5:['H',0.7,-2.5,0],
	   6:['H',-0.7,-2.5,0],
	   7:['O',0,3.0,0],
	   8:['H',0,2.6,-0.7],
	   9:['H',0,2.6,0.7],
	   10:['O',0,-4.5,0],
	   11:['H',0,-4.5,1],
	   12:['H',0,-5.5,0],
	   13:['O',2.8,0,0],
	   14:['H',3.5,0.7,0],
	   15:['H',3.5,-0.7,0],
	   16:['O',-4.9,0,0],
	   17:['H',-4.2,-0.7,0],
	   18:['H',-4.2,0.7,0]}
	'''

	d=temp_d()

	o,h,o_ref,h_ref=[],[],0,0
	o_refe,h_refe={},{}
	o_bou,h_bou,o_boun,h_boun=[],[],{},{}

	#a,b,c=31.269,31.175,31.073
	a,b,c=100,100,100

	for i in range (1,len(d)+1):
		p=PBC(d[i][1:],a,b,c)
		#print d[i][1:],p
		if d[i][1:]!=p:
			d[i]=[d[i][0]]+p 
			print i,p

		if d[i][0]=='O':
			o.append(d[i][1:])
			bou_ref=near_boundry(d[i][1:],a,b,c)
			if bou_ref:
				o_boun[o_ref]=bou_ref
			o_refe[o_ref]=i
			o_ref+=1

		if d[i][0]=='H':
			h.append(d[i][1:])
			bou_ref=near_boundry(d[i][1:],a,b,c)
			if bou_ref:
				h_boun[h_ref]=bou_ref
			h_refe[h_ref]=i
			h_ref+=1

	links_o=get_donars(o,h,o_refe,h_refe,o_boun,h_boun,a,b,c)
	links_h=get_acceptors(links_o)

	res=result(o,h,1.5,2.0,o_boun,h_boun,a,b,c)
	
	hbonds={}
	obonds={}
	for i in res:
		li=i[1]
		#li=[h_refe[j] for j in li]
		if len(links_o[o_refe[i[0]]])>=2:
			try:
				h1,h2=links_o[o_refe[i[0]]] # acceptor oxygen links
			except ValueError:
				h1=links_o[o_refe[i[0]]][0]
				h2=links_o[o_refe[i[0]]][1]
				#print links_o[o_refe[i[0]]]

			kli=[]
			for j in li:

				if 1 or angle(o_refe[i[0]],h_refe[j],links_h[h_refe[j]][0],h1,h2,d):
					kli.append(h_refe[j])
					obonds[h_refe[j]]=[o_refe[i[0]]]
			hbonds[o_refe[i[0]]]=kli
		elif len(links_o[o_refe[i[0]]])==1:
			kli=[]
			for j in li:
					kli.append(h_refe[j])
					obonds[h_refe[j]]=[o_refe[i[0]]]
			hbonds[o_refe[i[0]]]=kli

	
	return d,links_h,links_o,hbonds,obonds

	



if __name__=='__main__':
	data()




















