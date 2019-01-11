import hb_connections as hb
import addRing as aR
import sys

vs = set()
count =0

def get_neighbours(lis,con,i):

	global vs
	ns1 = map(lambda x: x+1,con.next_state(a-1,3.0))
	for j in ns1:
		if j not in lis:
			lis.append(j)
	vs.add(i)
	

def xyz(lis,con,ref):
	
	global count
	while count<5:
		#print lis
		for i in lis:
			if i not in vs:
				get_neighbours(lis,con,i)
			print len(lis)
		count+=1
	write_o(lis,ref)

def write_o(lis,ref,con,name = ''):
	#name = '_'.join(map(str,ref_lis))
	#f = open('I5_'+name+'.com','w')
	f = open('I5_'+name+'_'+(3-len(str(ref)))*'0'+str(ref)+'.com','w')
	f.write("""hf/6-31g

comment

0 1
""")
	for i in lis:
		f.write(' '.join(map(str,con.d[i]))+'\n')
	f.write('\n\n')
	f.close()

	return  






if __name__=='__main__':
	ref = 1
	name = sys.argv[1].split('.')[0]
	ids = aR.get_ids(name+'.txt')
	con=hb.connections(name+'.xyz')
	xyz_d = {}
	for i in ids:
		a,b,c = map(int,ids[i])
		lis = con.bfs(b-1,c-1)
		if len(lis) == 5:
			ns1 = map(lambda x: x+1,con.next_state(lis[0],3.5))
			ns2 = map(lambda x: x+1,con.next_state(lis[-1],3.5))
			#print con.d[a][0]
			write_o(list(set(lis+ns1+ns2)),ref,con,con.d[a][0]+con.d[b][0]+con.d[c][0])
			#vs = set()
			#count = 0
			#xyz_d[i] = xyz(lis,con,ref)

			ref+=1
			
	

	

