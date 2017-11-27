import os

def pdb_xyz(file):
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
            x,y,z=line.strip().split()[6:9]
            s=line.strip().split()[-1]
            d[id]=[s,x,y,z]
            id+=1
    g=open(file.split('.')[0]+'.xyz','w')
    for i in range (len(d)):
        g.write('  '.join(d[i])+'\n')
    g.close()

def make_fchk(path):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    s,cord=[],[]
    ref=0
    sym={'14':'Si','1':'H','7':'N','8':'O','6':'C','53':'I','36':'Kr','9':'F'}
    for line in lines:
        if 'Number of symbols in /Mol/' in line:
            break
        if len(line.strip().split())==0:
            continue
        if 'Nuclear charges' in line:
            ref=1
        if ref==1 or ref==2:
            ref+=1
        if ref==3:
            lis=[i.split('.')[0] for i in line.strip().split()]
            s+=lis 
        if 'Current cartesian coordinates' in line:
            ref+=1
        if ref==4 or ref==5:
            ref+=1
        if ref==6:
            lis=[str((float(i.split('E')[0])*(10**int(i.split('E')[1])))*0.529177) for i in line.strip().split()]
            cord+=lis
        
    cords=[]
    i,ref=0,0
    g=open(path[:-5]+'.xyz','w')
    while i < (len(cord)):
        g.write(sym[s[ref]]+' '+' '.join(cord[i:i+3])+'\n')
        i+=3
        ref+=1
    g.close()

def make_out(path):
    data = subprocess.check_output('gcartesian '+path, shell=True)
    g=open(path[:-4]+'.xyz','w')
    g.write(data)
    g.close()

def make_xyz(path):
    if path.split('.')[-1]=='fchk':
        make_fchk(path)
        return 2
    elif path.split('.')[-1]=='out':
        make_out(path)
        return 3
    elif path.split('.')[-1]=='pdb':
        pdb_xyz(path)
        return 4
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    lis=''
    ref=0
    sym={'15':'P','14':'Si','1':'H','7':'N','8':'O','6':'C','53':'I','36':'Kr','9':'F'}
    for line in lines:
        if '#p ' in line:
            ref+=1
        if len(line.strip().split())==0:
            ref+=1
        if ref==6:
            break
        if ref==3 or ref==4:
            ref+=1
        if ref==5:
            list1=line.strip().split()
            try:
                if len(line.strip().split())==2:
                    lis+=line
                else:
                    int(list1[0])
                    lis+=sym[list1[0]]+'  '+' '.join(list1[1:])+'\n'
            except ValueError:
                lis+=line
    g=open(path[:-4]+'.xyz','w')
    g.write(lis)
    g.close()
    return 1

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

def get_ids(path):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    ref=0
    st=''
    for line in lines:
        if ref==5:
            break
        if 'File format' in line:
            ref=1
        if len(line.strip().split())==0 and ref>0:
            ref+=1
        if ref==2 or ref==3:
            ref+=1
        if ref==4:
            s,e=line.index('('),line.index(')')
            l=line[s+1:e].split(',')
            st+=l[0].strip()+' '+l[1].strip()+' 0 0 : '+line[e+1:].split()[0]+'\n'
    return st


def make_lmode(path):
    #print 'performing step 1 ...'
    ids=get_ids('output.txt')
    filename=path.split('/')[-1].split('.')[0]
    s1="""
 $Contrl QCProg="gaussian"
   iprint=0
   isymm = 1
 $end

$qcdata
 """
    s2='fchk="'+filename+'.fchk"'
    s3="""$end

$LocMod $End
"""
    s4=ids
    f=open(filename+'.alm','w')
    f.write(filename+'\n')
    f.write(s1)
    f.write(' '+s2+'\n')
    f.write(s3)
    f.write(s4+'\n')
    f.close()

    os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+'.alm' +' >'+' '+filename+'.out')



            


