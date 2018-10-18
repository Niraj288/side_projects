import os
import sys
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


def make_alm(path,suffix):
	#print 'performing step 1 ...'
	ids=get_ids(path.split('/')[-1].split('.')[0]+'.txt',suffix)
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
	f=open(filename+suffix+'.alm','w')
	f.write(filename+'\n')
	f.write(s1)
	f.write(' '+s2+'\n')
	f.write(s3)
	f.write(s4+'\n')
	f.close()

	#/Users/47510753/Downloads/LocalMode-2016/lmodes.exe

	os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+suffix+'.alm' +' >'+' '+filename+suffix+'.out')

'''
lis=os.listdir('.')
for i in lis:
	if i[-5:]=='.fchk':
		make_alm(i)
		break
'''
#make_alm(sys.argv[1])

if __name__=='__main__':
	make_alm(sys.argv[1],'')


	
