import os

def make_xyz(file):
    f=open(file,'r')
    list1=f.readlines()
    f.close()
    d={}
    id=0
    for line in list1:
        if len(line.strip().split())==0:
            continue
        if "END" in line.split()[0]:
            break
        if 'ATOM' in line.split()[0]: #use HETATM only when required
            print line
            x,y,z=line.strip().split()[5:8]
            s=line.strip().split()[-1]
            d[id]=[s,x,y,z]
            id+=1
    g=open(file.split('.')[0]+'.xyz','w')
    for i in range (len(d)):
        g.write('  '.join(d[i])+'\n')
    g.close()


def zmatrix(file):
    if file.split('.')[-1]=='pdb':
        make_xyz(file)
    return 'boo yeah'
    file=file.split('.')[0]+'.xyz'
    os.system('module load gaussian/g16a')
    filename=file.split('.')[0]+'.com'
    os.system('newzmat -ixyz -Ozmat -rebuildzmat '+file+' '+filename)
    f=open(filename,'r')
    lines=f.readlines()
    f.close()
    ref=0
    string=''
    var=0
    count=-1
    li=[]
    d,dr={},0
    for i in range (len(lines)):
	if len(lines[i].strip().split())==0:
		if ref==0:
                        continue
                elif ref==1:
                        break
        if 'C'==lines[i].split()[0]:
            ref=1
        elif ref==1:
            line=lines[i].strip().split(',')
            if len(line)>=7:
                li.append(line[2])
                li.append(line[4])
                li.append(line[6])
	    elif len(line)>=5:
                li.append(line[2])
                li.append(line[4])
            elif len(line)>=3:
                li.append(line[2])
            if 'Variables:' in lines[i]:
                dr=1
	    if dr==1 or dr==2:
		dr+=1
	    if dr==3:
		a,b=lines[i].strip().split('=')
		d[a]=b
    for line in lines:
	if len(line.strip().split())==0:
		if ref==1:
			continue
		elif ref==0:
			break
        if 'C'==line.strip().split()[0]:
            ref=0
        if ref==0:
            if 'Variables:' in line:
                break
	    string+=' '.join(line.strip().split(','))+'\n'

    li=['='.join([r,d[r]]) for r in li]
    string+='\n Variables:\n'
    li1=li[:6]
    string+='\n'.join(li1)
    string+='\n Constants:\n'
    string+='\n'.join(li[6:])+'\n'
    return string 



            


