import data
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
import multiprocessing as mp
style.use("ggplot")

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

class Queue:
    def __init__(self):
        self.list = []
    def push(self,item):
        self.list.insert(0,item)
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
        return len(self.list) == 0

def next_state(item,d,links_h,links_o,hbonds,obonds):
	try:
		if d[item][0]=='H':
			if item in obonds:
				nstate=links_h[item]+obonds[item]
			else:
				nstate=links_h[item]
		elif d[item][0]=='O':
			if item in hbonds:
				nstate=links_o[item]+hbonds[item]
			else:
				nstate=links_o[item]
	except KeyError:
		nstate = []
	return nstate

def printAllPaths(cstate, goal, d,links_h,links_o,hbonds,obonds, vs, path, count, fli): 

    # Mark the current node as visited and store in path 
    #print cstate, next_state(cstate, d,links_h,links_o,hbonds,obonds), path, count
    
    vs.add(cstate)
    path.append(cstate) 
    count += 1
    # If current vertex is same as destination, then print 
    # current path[] 
    if cstate in goal and count >3: 
        fli.append(copy.copy(path)) 
    else: 
        # If current vertex is not destination 
        #Recur for all the vertices adjacent to this vertex 
        for i in next_state(cstate, d,links_h,links_o,hbonds,obonds): 
            if i not in vs: 
                printAllPaths(i, goal, d,links_h,links_o,hbonds,obonds, vs, path, count, fli) 
                  
    # Remove current vertex from path[] and mark it as unvisited 
    path.pop() 
    vs.remove(cstate)

def compute(x, d,links_h,links_o,hbonds,obonds, output):
	vs = set()
	path = []
	count = 0
	fli = []
	goal = next_state(x, d,links_h,links_o,hbonds,obonds)
	printAllPaths(x, goal, d,links_h,links_o,hbonds,obonds, vs, path, count, fli)

	'''#print fli
				c_li = []
				for i in fli:
					c = copy.copy(i)
					c.sort()
					c_li.append(c)
			
				inde = []
				for i in range (len(c_li)):
					for j in range (len(c_li)):
						if i == j:
							continue
						if c_li[i] == c_li[j]:
							inde.append(j)
			
				print inde
				fli_f = []
				for i in range (len(fli)):
					if i not in inde:
						fli_f.append(fli[i])'''

	output.put((x, fli))

def compute_all_cycles(d,links_h,links_o,hbonds,obonds):

	output = mp.Queue()

	processes = [mp.Process(target=compute, args=(x, d,links_h,links_o,hbonds,obonds, output)) for x in range (1, len(d)) if d[x][0] == 'O']

	for p in processes:
		p.start()
	for p in processes:
		p.join()
	
	results = [output.get() for p in processes]
	
	return results


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
        #print path+[cstate],nstate,vs
        for i in nstate:
        	if len(path)>2 and (cstate==fstate or fstate in next_state(cstate,d,links_h,links_o,hbonds,obonds)):
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

def ring_extract(d,links_h,links_o,hbonds,obonds):
	ring_d={}
	for i in d:
		if d[i][0]=='O':
			ring=bfs(i,d,links_h,links_o,hbonds,obonds)
			ring_d[i]=ring
	return ring_d 

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
			ax.text(x1,y1,z1,str(b))
			s1,x1,y1,z1=d[a]
			ax.scatter(x1,y1,z1,c='b',marker='o')
			ax.text(x1,y1,z1,str(a))
			ax.scatter(x,y,z,c='r',marker='o')
			ax.text(x,y,z,str(i))
		else:
			ax.scatter(x,y,z,c='b',marker='o')
			ax.text(x,y,z,str(i))
			a=links_h[i]
			s1,x1,y1,z1=d[a[0]]
			ax.scatter(x1,y1,z1,c='r',marker='o')
			ax.text(x1,y1,z1,str(a[0]))
			a,b=links_o[a[0]]
			if a==i:
				s1,x1,y1,z1=d[b]
				ax.scatter(x1,y1,z1,c='b',marker='o')
				ax.text(x1,y1,z1,str(i))
			else:
				s1,x1,y1,z1=d[a]
				ax.scatter(x1,y1,z1,c='b',marker='o')
				ax.text(x1,y1,z1,str(a))
	check_ring(ring,ring_set)

	X=[d[ring[0]][1]]
	Y=[d[ring[0]][2]]
	Z=[d[ring[0]][3]]

	if [X[0],Y[0],Z[0]] not in coordinates:
		coordinates.append([X[0],Y[0],Z[0]])
	
	for i in range (1,len(ring)):
		if len(rings[ring[i]])<len(ring) and len(rings[ring[i]])>1 and rings[ring[i]][1] not in ring:
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

def visualize(rings,links_o,links_h):
	main_ring=[]
	for i in rings:
		ring=rings[i]
		if ring!=None:
			pass
			#print len(ring)
		if ring!=None and len(ring)/2==2:
			if set(ring) not in main_ring:
				main_ring.append(set(ring))
				ring_set=[]
				print '********'
				fig = plt.figure()
				ax = fig.add_subplot(111, projection='3d')
				X,Y,Z=visual(rings,ring,d,ring_set,ax,links_o,links_h,[])
				ax.plot(X,Y,Z,marker='o')
				plt.show()


if __name__=='__main__':
	d,links_h,links_o,hbonds,obonds=data.data()

	print compute_all_cycles(d,links_h,links_o,hbonds,obonds)
	'''
	vs = set()
	path = []
	count = 0
	fli = []
	goal = next_state(1, d,links_h,links_o,hbonds,obonds)
	printAllPaths(1, goal, d,links_h,links_o,hbonds,obonds, vs, path, count, fli)

	print fli
	#ring_d=ring_extract(d,links_h,links_o,hbonds,obonds)
	#print ring_d
	#visualize(ring_d,links_o,links_h)
	'''













