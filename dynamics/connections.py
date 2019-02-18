import data
import copy
import sys
sys.setrecursionlimit(1500)

def connect(d,item,links_o,links_h,hbonds,obonds,vs,liss):
	nstate=[]
	vs.add(item)
	liss.append(item)
	#print item
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
		pass
	#print item,nstate
	for state in nstate:
		if state not in vs:
			connect(d,state,links_o,links_h,hbonds,obonds,vs,liss)

def connectivity(d,links_h,links_o,hbonds,obonds):
	fli=[]
	vs=set()
	liss=[]
	for item in d:
		if item not in vs:
			liss=[]
			connect(d,item,links_o,links_h,hbonds,obonds,vs,liss)
			fli.append(copy.copy(liss))
	return fli

def write_o(graph,d):
	#file=open('output.txt','w')
	st='mers ....\n'
	mers={}
	for i in graph:
		if len(i) not in mers:
			mers[len(i)]=[i]
		else:
			mers[len(i)].append(i)
	st+='  Atoms         Frequency\n'
	for i in mers:
		st+= "{:>6}  {:>10}".format(*[str(i),str(len(mers[i]))])+'\n'
	return mers, st 

def mer_dict(d,links_h,links_o,hbonds,obonds):
	graph=connectivity(d,links_h,links_o,hbonds,obonds)
	mers, st = write_o(graph,d)
	print st 
	dic = {}
	for i in st.split('\n')[2:-1]:
		a,b = i.strip().split()
		dic[int(a)] = int(b)
	return dic

if __name__=='__main__':
	
	d,links_h,links_o,hbonds,obonds=data.data(None, 100, 100, 100)
	#print links_o[1183]
	#print obonds
	graph=connectivity(d,links_h,links_o,hbonds,obonds)
	#print links_o
	mers, st = write_o(graph,d)

	dic = {}
	for i in st.split('\n')[2:-1]:
		a,b = i.strip().split()
		dic[int(a)] = int(b)
	print dic
