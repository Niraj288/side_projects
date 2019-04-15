import sys
import data
import itertools as itt
import matplotlib.pyplot as plt
import copy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
import multiprocessing as mp
import numpy as np
style.use("ggplot")

sys.setrecursionlimit(1500)

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
    lim = 18 # limit backtrack

    if count > lim :
    	return 

    vs.add(cstate)
    path.append(cstate) 
    count += 1
    # If current vertex is same as destination, then print 
    # current path[] 
    
    if cstate in goal and count > 5: 
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

	flis_f = []
	fcheck = []
	for i in fli:
		temp = copy.copy(i)
		temp.sort()
		if temp not in fcheck:
			flis_f.append(i)
			fcheck.append(temp)

	output.put((x, flis_f))


def make_block(a,b,c,d,incr):
	coord = np.array([[i]+d[i][1:] for i in d])
	#print np.min(coord)
	block = []
	for i in range (-a,a,incr):
		for j in range (-b,b,incr):
			for k in range (-c,c,incr):
				ct = coord[coord[:,1]>i]
				ct = ct[ct[:,1]<i+incr]
				#print ct
				ct = ct[ct[:,2]>j]
				ct = ct[ct[:,2]<j+incr]
				ct = ct[ct[:,3]>k]
				ct = ct[ct[:,3]<k+incr]
				#print ct
				ld = {}
				for ij in ct:
					ld[int(ij[0])] = d[int(ij[0])]
				block.append(ld)
	for i in range (-a+incr/2,a,incr):
		for j in range (-b+incr/2,b,incr):
			for k in range (-c+incr/2,c,incr):
				ct = coord[coord[:,1]>i]
				ct = ct[ct[:,1]<i+incr]
				#print ct
				ct = ct[ct[:,2]>j]
				ct = ct[ct[:,2]<j+incr]
				ct = ct[ct[:,3]>k]
				ct = ct[ct[:,3]<k+incr]
				#print ct
				ld = {}
				for ij in ct:
					ld[int(ij[0])] = d[int(ij[0])]
				block.append(ld)
	return block


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


def compute_all_cycles2(d,links_h,links_o,hbonds,obonds):

	output = mp.Queue()

	processes = [mp.Process(target=compute, args=(x, d,links_h,links_o,hbonds,obonds, output)) for x in d if d[x][0] == 'O']

	for p in processes:
		p.start()
	for p in processes:
		p.join()
	
	results = [output.get() for p in processes]

	check_lis = []
	res = []
	for i in results:
		for j in i[1]:
			temp = copy.copy(j)
			temp.sort()
			if temp not in check_lis:
				res.append(j)
				check_lis.append(temp)
	#print len(check_lis)
	return res

def combo(rings):
	rd = {} # dictionary for all atoms in rings

	#rings = [ringsD[i] for i in ringsD]

	#print rings
	
	for i in range (len(rings)):
		for j in rings[i]:
			if j in rd:
				rd[j].append(i)
			else:
				rd[j] = [i]
	#print rd

	
	check_lis = []
	flis = []

	def recr(ring_lis, id):

		for k in ring_lis:
			if k in rd:
				coms = []
				for l in range (len(rd[k])):
					coms += list(itt.combinations(rd[k], l+1))
				combs = []
				for c in coms:
					ct = list(set([id] + list(c)))
					temp = copy.copy(ct)
					temp.sort()
					if temp not in check_lis:
						check_lis.append(temp)
						flis.append(ct)
	
	for i in range (len(rings)):
		recr(rings[i], i)

	return flis

def writeO(li, comb, rings, d,links_h,links_o,hbonds,obonds):
	f = open(li+'.com','w')
	coords = []
	vs = set()
	for i in comb:
		temp = rings[i] 
		#print temp
		for j in temp:
			if d[j][0] == 'O':
				t = links_o[j]
				#print t
				for k in t:
					if k not in vs:
						coords.append(' '.join(map(str, d[k])))
						vs.add(k)

			if d[j][0] == 'H':
				t = links_h[j]
				#print t
				for k in t:
					if k not in vs:
						coords.append(' '.join(map(str, d[k])))
						vs.add(k)

			if j not in vs:
				coords.append(' '.join(map(str, d[j])))
				vs.add(j)

	st = '''hf/b3lyp

comment

0 1
'''
	st += '\n'.join(coords)
	st+= '\n\n'

	f.write(st)
	f.close()



# user readable format for ring type
def conv_combo(rings, comb, d,links_h,links_o,hbonds,obonds):
	rd = {}

	for i in comb:
		li = [len(rings[j]) for j in i]
		li.sort(reverse = True)

		li = '-'.join(map(str, li))
		'''
		if li == '12-10-10':
			for k in [' '.join(map(str, rings[j]))+'\n' for j in i]:
				print k
		'''
		if li in rd:
			rd[li]+=1
		else:
			rd[li] = 1
			writeO(li, i, rings, d,links_h,links_o,hbonds,obonds)
	
	return rd 

def job(d,links_h,links_o,hbonds,obonds,a=100,b=100,c=100):
	block = make_block(int(a)+1, int(b/2)+1, int(c/2)+1, d, 6)
	res = []
	check_lis = []
	for i in block:
		#print len(i)
		results = compute_all_cycles2(i,links_h,links_o,hbonds,obonds)
		for j in results:
			temp = copy.copy(j)
			temp.sort()
			if temp not in check_lis:
				res.append(j)
				check_lis.append(temp)

	allComboRings = combo(res)

	#print allComboRings

	return conv_combo(res, allComboRings, d,links_h,links_o,hbonds,obonds) 


if __name__=='__main__':

	d,links_h,links_o,hbonds,obonds=data.data()

	print job(d,links_h,links_o,hbonds,obonds,35, 35, 35)

	'''

	allRings = compute_all_cycles2(d,links_h,links_o,hbonds,obonds)
	
	print len(allRings)

	allComboRings = combo(allRings)

	#print allComboRings

	print conv_combo(allRings, allComboRings)
	'''

	'''

	block = make_block(int(35.1403200/2)+1, int(35.0343200/2)+1, int(34.9203200/2)+1, d, 6)
	#print len(block[0])
	res_dict = {}
	for i in block:
		#print len(i)
		res_dict = merge_two_dicts(compute_all_cycles(i,links_h,links_o,hbonds,obonds),res_dict)
	
	#print res_dict	
	pr = get_max_cycles_only(res_dict)

	#print pr[3][0][0]
	write_o(pr, d, links_h,links_o,hbonds,obonds, range(15))

	
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













