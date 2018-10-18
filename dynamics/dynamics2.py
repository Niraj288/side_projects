import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
import copy

class Queue:
    def __init__(self):
        self.list = []
    def push(self,item):
        self.list.insert(0,item)
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
        return len(self.list) == 0

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def next_state(cstate,d,links_h,links_o,hbonds,obonds):
	if d[cstate][0]=='H':
		try:
			nstate=links_h[cstate]+obonds[cstate]
		except KeyError:
			nstate=links_h[cstate]
	elif d[cstate][0]=='O':
		nstate=links_o[cstate]+hbonds[cstate]
	return nstate

def bfs(cstate,d,links_h,links_o,hbonds,obonds):    
    path=[]
    item=[cstate,path]
    vs=set()
    f=Stack()
    ref=0
    goal,fstate=None,cstate
    vs.add(cstate)
    while cstate!=goal:
        [cstate,path]=item
        nstate=next_state(cstate,d,links_h,links_o,hbonds,obonds)
        #print nstate
        for i in nstate:
        	if ref>3 and (cstate==fstate or fstate in next_state(cstate,d,links_h,links_o,hbonds,obonds)):
        		return path+[cstate]
        	f.push([i,path+[cstate]])
        while True:
            if f.isEmpty():
                return []
            item=f.pop()
            if item[0] not in vs:
                break
        cstate=item[0]
        vs.add(item[0])
        ref+=1
        #print path,cstate
    return []

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def check(x,a,x_size):
	if (x <  -x_size * 0.5):
		x = x + x_size
	if (x >=  x_size * 0.5):
		x = x - x_size
	return x

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

def PBC(lis):
	x,y,z=lis
	a,b,c=31.269,31.175,31.073
	x=check(x,0,a)
	y=check(y,0,b)
	z=check(z,0,c)
	return [x,y,z]

def m_boundary(d,index,a):
	b={}
	r=2
	for i in d:
		#inside
		if abs(a/2+d[i][index])<r:
			#print d[i]
			b[i]=copy.copy(d[i])
		
		if abs(d[i][index]-a/2)<r:
			#print d[i]
			b[i]=copy.copy(d[i])
		
		#outside
		if abs((d[i][index]+a)-a/2)<r:
			li=copy.copy(d[i])
			li[index]=d[i][index]+a
			b[i]=li
			#print b[i]
		if abs(a/2+(d[i][index]-a))<r:
			li1=copy.copy(d[i])
			li1[index]=d[i][index]-a
			b[i]=li1
			#print b[i] 
	
	return b

def boundary(d):
	a,b,c=31.269,31.175,31.073
	b1=m_boundary(d,1,a)
	b2=m_boundary(d,2,b)
	b3=m_boundary(d,3,c)
	b_refe,h,o={},[],[]
	h_refe,h_ref={},0
	o_refe,o_ref={},0
	for i in b1:
		b_refe[i]=b1[i]
		if 'H'==b_refe[i][0]:
			h.append(b_refe[i][1:])
			h_refe[h_ref]=i
			h_ref+=1
		elif 'O'==b_refe[i][0]:
			o.append(b_refe[i][1:])
			o_refe[o_ref]=i
			o_ref+=1
	for i in b2:
		b_refe[i]=b2[i]
		if 'H'==b_refe[i][0]:
			h.append(b_refe[i][1:])
			h_refe[h_ref]=i
			h_ref+=1
		elif 'O'==b_refe[i][0]:
			o.append(b_refe[i][1:])
			o_refe[o_ref]=i
			o_ref+=1
	for i in b3:
		b_refe[i]=b3[i]
		if 'H'==b_refe[i][0]:
			h.append(b_refe[i][1:])
			h_refe[h_ref]=i
			h_ref+=1
		elif 'O'==b_refe[i][0]:
			o.append(b_refe[i][1:])
			o_refe[o_ref]=i
			o_ref+=1
	res=result(o,h,1.5,2.2)
	c_refe={}
	for i in res:
		a,b=i
		oref=o_refe[a]
		li1=[h_refe[j] for j in b]
		c_refe[oref]=li1

	return c_refe

def cross_check(hbonds,d2):
	d3={}
	for i in hbonds:
		b=hbonds[i]
		for j in b:
			try:
				if j not in d2[i]:
					if i not in d3:
						d3[i]=[j]
					else:
						d3[i].append(j)
			except KeyError:
				pass
	return d3


def get_donars(o,h,o_refe,h_refe):
    point_tree = spatial.cKDTree(h)
    li_a={}
    for i in range (len(o)):
        li1=(point_tree.query_ball_point(o[i], 1.1))
        li1=[h_refe[j] for j in li1]
        li_a[o_refe[i]]=li1
    return li_a

def get_acceptors(o,h,o_refe,h_refe):
    point_tree = spatial.cKDTree(o)
    li_a={}
    for i in range (len(h)):
        li1=(point_tree.query_ball_point(h[i], 1.1))
        li1=[o_refe[j] for j in li1]
        li_a[h_refe[i]]=li1
    return li_a

def result(arr1,arr2,mi,ma):
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
        res.append([i,list(set(li1)-set(li2))])
    return res

vs=set()
liss=[]
def connect(d,item,links_o,links_h,hbonds):
	global vs,liss
	nstate=[]
	vs.add(item)
	liss.append(item)
	if d[item][0]=='H':
		nstate=links_h[item]
	elif d[item][0]=='O':
		nstate=links_o[item]+hbonds[item]
	for state in nstate:
		if state not in vs:
			connect(d,state,links_o,links_h,hbonds)

def connectivity(d,links_h,links_o,hbonds):
	fli=[]
	global vs,liss
	for item in d:
		if item not in vs:
			liss=[]
			connect(d,item,links_o,links_h,hbonds)
			fli.append(copy.copy(liss))
	return fli
def plot_graph(graph,d):
	colors = 200*['r','g','b','c','k','y','m']
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	col=0
	for i in graph:
		for j in i:
			x,y,z=d[j][1:]
			ax.scatter(x,y,z, c=colors[col], marker='o')
		col+=1
	plt.show()

def write_o(graph,d):
	#file=open('output.txt','w')
	print 'mers ....'
	mers={}
	for i in graph:
		if len(i) not in mers:
			mers[len(i)]=[i]
		else:
			mers[len(i)].append(i)
	for i in mers:
		print i/3,len(mers[i])

	plot_graph(graph,d)
	return mers 

def check_ring(ring,ring_set):
	temp=set(ring)
	if temp not in ring_set:
		ring_set.append(temp)
		return True
	return False


def visual(rings,ring,d,ring_set,ax,links_o,links_h,coordinates):
	for i in ring:
		s,x,y,z=d[i]
		if [x,y,z] in coordinates:
			continue
		else:
			coordinates.append([x,y,z])
		if s=='O':
			a,b=links_o[i]
			s1,x1,y1,z1=d[b]
			ax.scatter(x1,y1,z1,c='b',marker='o')
			s1,x1,y1,z1=d[a]
			ax.scatter(x1,y1,z1,c='b',marker='o')
			ax.scatter(x,y,z,c='r',marker='o')
		else:
			ax.scatter(x,y,z,c='b',marker='o')
			a=links_h[i]
			s1,x1,y1,z1=d[a[0]]
			ax.scatter(x1,y1,z1,c='r',marker='o')
			a,b=links_o[a[0]]
			if a==i:
				s1,x1,y1,z1=d[b]
				ax.scatter(x1,y1,z1,c='b',marker='o')
			else:
				s1,x1,y1,z1=d[a]
				ax.scatter(x1,y1,z1,c='b',marker='o')
	check_ring(ring,ring_set)

	X=[d[ring[0]][1]]
	Y=[d[ring[0]][2]]
	Z=[d[ring[0]][3]]

	if [X[0],Y[0],Z[0]] not in coordinates:
		coordinates.append([X[0],Y[0],Z[0]])
	
	for i in range (1,len(ring)):
		if len(rings[ring[i]])<len(ring) and rings[ring[i]][1] not in ring:
			if 1 or check_ring(ring,ring_set):
				x,y,z=visual(rings,rings[ring[i]],d,ring_set,ax,links_o,links_h,coordinates)
				X+=x
				Y+=y 
				Z+=z 
		else:
			X+=[d[ring[i]][1]]
			Y+=[d[ring[i]][2]]
			Z+=[d[ring[i]][3]]
	X+=[d[ring[0]][1]]
	Y+=[d[ring[0]][2]]
	Z+=[d[ring[0]][3]]
	print len(ring_set)
	return X,Y,Z 
	
	'''
	for i in ring:
		x,y,z=d[i][1:]
		if d[i][0]=='H':
			ax.scatter(x, y, z, c='red',marker='o')
		else:
			ax.scatter(x, y, z, c='blue',marker='^')
		ax.text(x,y,z,i)
	'''

def data_extraction(path,pdb_ref,PBC_ref=0):
	file = open(path,'r')
	lines=file.readlines()
	file.close()
	o,h,o_ref,h_ref=[],[],0,0
	o_refe,h_refe={},{}
	d,d_ref={},0
	ref=1
	if pdb_ref==0:
		inde1,inde2=2,6
	else:
		inde1,inde2=0,1
	for line in lines:
		if len(line.strip().split())<4:
			continue
		if 'O' in line.strip().split()[inde1]:
			x,y,z=map(float,line.strip().split()[inde2:inde2+3])
			d[ref]=['O',x,y,z]
			o.append([x,y,z])
			o_refe[o_ref]=ref
			o_ref+=1
			ref+=1
		elif pdb_ref==0 and 'H'==line.strip().split()[inde1][0]:
			x,y,z=map(float,line.strip().split()[inde2:inde2+3])
			d[ref]=['H',x,y,z]
			h.append([x,y,z])
			h_refe[h_ref]=ref 
			h_ref+=1
			ref+=1
		elif pdb_ref==1 and 'H'==line.strip().split()[inde1]:
			x,y,z=map(float,line.strip().split()[inde2:inde2+3])
			d[ref]=['H',x,y,z]
			h.append([x,y,z])
			h_refe[h_ref]=ref 
			h_ref+=1
			ref+=1

	links_o=get_donars(o,h,o_refe,h_refe)
	links_h=get_acceptors(o,h,o_refe,h_refe)
	
	if PBC_ref:
		for i in range (len(o)):
			o[i]=PBC(o[i])
		for i in range (len(h)):
			h[i]=PBC(h[i])
	res=result(o,h,0.5,1.3)

	hbonds={}
	obonds={}
	for i in res:
		li=i[1]
		#li=[h_refe[j] for j in li]
		try:
			h1,h2=links_o[o_refe[i[0]]] # acceptor oxygen links
		except ValueError:
			h1=links_o[o_refe[i[0]]][0]
			h2=links_o[o_refe[i[0]]][1]
			#print links_o[o_refe[i[0]]]

		kli=[]
		for j in li:

			if angle(o_refe[i[0]],h_refe[j],links_h[h_refe[j]][0],h1,h2,d):
				kli.append(h_refe[j])
				obonds[h_refe[j]]=[o_refe[i[0]]]
		hbonds[o_refe[i[0]]]=kli
	
	graph=connectivity(d,links_h,links_o,hbonds)
	write_o(graph,d)
	for i in graph:
		if len(i)/3>1:
			pass
			#print len(i)/3
	

	#d2=boundary(d)
	#d3=cross_check(hbonds,d2)




data_extraction('/Users/47510753/Downloads/test-2.pdb',0)











