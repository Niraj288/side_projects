import sys

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if (len(l_)==0 or l_.isdigit() or l_ == 'A') and r !='H':
        chain='backbone'
    else:
        chain='side_chain' 
    return chain

def get_backbone(path):
        f = open(path,'r')
        lines = f.readlines()
        f.close()

        ref =0
        d = {}
        for line in lines:
                if "TER" in line.split()[0]:
                        break
                if line.split()[0] in ['ATOM']:
                        #print line
                        id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
                        s=line.strip().split()[-1]
                        if chain(s,at) == 'backbone':
                                d[id]=[s,x,y,z]
                                ref+=1
        lis = map(int,list(d))
        lis.sort()

        return lis,d

def check(lis,id,d):
	if id+11>len(lis):
		return [0,None] 
	st = ''
	a,b =None,None
	for i in range (11):
		j = str(lis[id+i])
		st += d[j][0]
		if i == 2:
			a = j
		if i == 6:
			b = j

	#print st
	if st == 'CONCCONCCON':
		return [1,[a,b]]
	return [0,None] 

def get_I5(lis,d):
	li = []
	for i in range (len(lis)):
		a,b = check(lis,i,d)
		if a:
			li.append(b)
	return li


if __name__ == '__main__':
        lis,d = get_backbone(sys.argv[1])
        #print list(d)
        get_I5(lis,d)

        st = ''
        for i in lis:
        	print d[str(i)]
        	st+=d[str(i)][0]

        #print st
        
