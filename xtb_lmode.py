#xtb_lmode
import os
import sys
import atom_data

def sub_s(lis):
	sub_s,ref='',0
	for i in lis:
		if ref%5==0:
			sub_s+='\n    '+i+'    '
		else:
			sub_s+=i+'    '
		ref+=1
	return sub_s

def get_ids(path,suffix):
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
			if suffix=='_dh':
				
				if '[' in line:
					l=line.strip().split()
					st+=l[6]+' '+l[8]+' 0 0 : '+l[-3]+'\n'
				else:
					l=line.strip().split()
					st+=l[2]+' '+l[4]+' 0 0 : '+l[-3]+'\n'
			else:
				#for acceptor-hydrogen calculation
				s,e=line.index('('),line.index(')')
				l=line[s+1:e].split(',')
				st+=l[0].strip()+' '+l[1].strip()+' 0 0 : '+line[e+1:].split()[0]+'\n'
			
	return st

def make_dat(path):
	filename=path[:-4]+'.xyz'
	#print filename[:-4]+'_hessian'
	h=open(filename[:-4]+'_hessian','r')
	hess0=h.readlines()[1:]
	h.close()
	hess=[]
	for line in hess0:
		hess+=line.strip().split()
	amass,za,xyz=[],[],[]
	f=open(filename,'r')
	lines=f.readlines()
	f.close()
	data=atom_data.data(sys.argv[0])
	sym=atom_data.symbol_dict(sys.argv[0])
	for line in lines[2:]:
		if len(line.strip().split())==0:
			continue

		s,x,y,z=line.strip().split()
		amass.append(data[sym[s]]['atomicMass'][:-3])
		za.append(str(sym[s]))
		xyz+=[x,y,z]

	g=open(filename[:-4]+'.dat','w')
	s=''
	s+='Eventually the world will end in singularity !! \n'
	s+='NATM\n   '+lines[0].strip().split()[0]+'\nAMASS'+sub_s(amass)
	s+='\nZA'+sub_s(za)
	s+='\nXYZ'+sub_s(xyz)
	s+='\nNOAPT'
	s+='\nFFX'+sub_s(hess)
	g.write(s)
	g.close()

def make_alm(path,suffix):
	make_dat(sys.argv[1])
	path=sys.argv[1]
	filename=path.split('/')[-1].split('.')[0]
	s1="""
 $contrl
   qcprog="ALMODE"
   iprint=0
   isymm = 1
   ifsave=.false.
 $end

$qcdata
 """
 	s2='fchk="'+filename+'.dat"'
 	s3="""$end

$LocMod $End
"""
	f=open(filename+suffix+'.alm','w')
	f.write(filename+'\n')
	f.write(s1)
	f.write(' '+s2+'\n')
	f.write(s3)
	f.write(get_ids(path.split('/')[-1].split('.')[0]+'.txt',suffix))
	f.close()

	os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+suffix+'.alm' +' >'+' '+filename+suffix+'.out')
	


	





