import data
import copy
import sys
sys.setrecursionlimit(1500)

vs=set()
liss=[]
def connect(d,item,links_o,links_h,hbonds,obonds):
	global vs,liss
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
			connect(d,state,links_o,links_h,hbonds,obonds)

def connectivity(d,links_h,links_o,hbonds,obonds):
	fli=[]
	global vs,liss
	for item in d:
		if item not in vs:
			liss=[]
			connect(d,item,links_o,links_h,hbonds,obonds)
			fli.append(copy.copy(liss))
	return fli

if __name__=='__main__':
	
	d,links_h,links_o,hbonds,obonds=data.data()
	graph=connectivity(d,links_h,links_o,hbonds,obonds)
	for i in graph:
		print len(i)
