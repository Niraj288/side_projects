import sys
import module
import scipy.spatial as spatial
import os
import hb_connections as hb
import math

def xyz(filename,end):
	if end==xyz:
		return
	print 'Making xyz ...'
	print 'Exit status :',module.make_xyz(filename+'.'+end)

# reading from pdb
def read_data(path):
	#xyz(path[:-4],path[-4:])
	os.system('babel '+path+' '+'.'.join(path.split('.')[:-1])+'.xyz')
	f=open(path[:-4]+'.xyz','r')
	lines=f.readlines()
	f.close()

	d={}
	ir=1
	atoms=[]
	atoms_d={}
	for i in lines[2:]:
		l=i.strip().split()
		if len(l)==1:
			break
		if len(l)==0:
			continue
		a,x,y,z=l
		x,y,z=map(float,[x,y,z])
		if a in ['N','C']:
			atoms.append([x,y,z])
			atoms_d[len(atoms)-1]=ir  
		d[ir]=[a,x,y,z]
		ir+=1


	return d,atoms,atoms_d

def pre_data(path,ma,mi):
        d,nitro,nitro_d=read_data(path)
        #print nitro
        arr=[d[i][1:] for i in d]

        point_tree = spatial.cKDTree(arr)
        result=[]
        for j in range(len(nitro)):
                #print j
                li1=(point_tree.query_ball_point(nitro[j], ma))
                li2=(point_tree.query_ball_point(nitro[j], mi))
                #print li2
                re=map(lambda x: x+1,list(set(li1)-set(li2)))
                #print nitro_d[j],re
                re1=[]
                for i in re:
                	if d[i][0] in ['N','O']:
                		re1.append(i)
                h_li = (point_tree.query_ball_point(nitro[j], 1.2))
                for i in h_li:
                	if d[i+1][0]=='H':
                		result.append([nitro_d[j],i+1,re1])

        return result,d 

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def connection_analysis(path,ma=3.0,mi=2.0):
	all_res={}
	res,d=pre_data(path,ma,mi)
	for n,a,li in res:
		#print a,h,li
		for b in li:
			con=hb.connections('.'.join(path.split('.')[:-1])+'.xyz')
			lis = con.bfs(a-1,b-1)
			if len(lis)==5:
				li=[a,b]
				li.sort()
				all_res[tuple(li)]=[lis,d[n][0]+d[a][0]+'-'+d[b][0]]

	return all_res



if __name__=='__main__':
	cd = {}
	scr = connection_analysis(sys.argv[1],ma=3.5,mi=2.0)
	print scr
	for i,j in scr:
		li = [i,j]
		li.sort()
		if tuple(li) in cd:
			print 'Duplicate values found!'
		else:
			cd[tuple(li)]=None




