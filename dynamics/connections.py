import data
import copy
import sys
sys.setrecursionlimit(1500)

def connect(d,item,links_o,links_h,hbonds,obonds,vs,liss):
	nstate=[]
	vs.add(item)
	liss.append(item)
	#print item
	if d[item][0]=='H':
		if item in obonds:
			nstate=links_h[item]+obonds[item]
		else:
			nstate=links_h[item]
	elif d[item][0]=='O':
		nstate=links_o[item]+hbonds[item]
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
	for i in mers:
		st+= str(i/3)+' '+str(len(mers[i]))+'\n'
	return st 

if __name__=='__main__':
	
	d,links_h,links_o,hbonds,obonds=data.data()
	graph=connectivity(d,links_h,links_o,hbonds,obonds)
	#print links_o
	print write_o(graph,d)
