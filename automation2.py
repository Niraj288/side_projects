import os
import subprocess
import sys

path=sys.argv[1]

def output():
	global path
	filename=path.split('/')[-1].split('.')[0]+'.out2'
	li=[]
	f=open(filename,'r')
	lines=f.readlines()
	f.close()
	for line in lines:
		l=line.strip().split()
		if len(l)==0:
			continue
		if 'Frequencies'==l[0]:
			li+=l[1:]
	print filename.split('.')[0]+'    '+'  '.join(li)

def step1(path):
	#print 'performing step 1 ...'
	filename=path.split('/')[-1].split('.')[0]
	s1="""
 $contrl
   qcprog="gaussian"
   iprint=1
   isymm=1
   ifmatlab=.True.
   ifsave=.True.
 $end

$qcdata
 """
 	s2='fchk="'+filename+'.fchk"'
 	s3="""$end

$LocMod $End
1 2 : R1
1 3 : R2
1 4 
2 1 4
2 1 3 
1 -2 -3 -4 
"""
	f=open(filename+'.alm1','w')
	f.write(filename+'\n')
	f.write(s1)
	f.write(' '+s2+'\n')
	f.write(s3+'\n')
	f.close()

	os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+'.alm1' +' >'+' '+filename+'.out1')
	step2('job.m')

def step2(path):
	#print 'performing step 2 ...'
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	ref,index=0,0
	st='];\nb2=[\n'
	for i in range (len(lines)):
		if '];' in lines[i] and ref==3:
			index=i
			break
		if 'b=[' in lines[i]:
			lines[i]=lines[i].replace('b','b1')
			ref=1
		if ref==2 or ref==1:
			ref+=1
		if ref==3:

			st+=' '.join(lines[i].strip().split()[:12])+'\n'
	st+='];\n\n'

	st+="""% Do the transformation

compliance_matrix=b1*(inv(f))*b1'
newHessian=b2'*inv(compliance_matrix)*b2


% Print out the newHessian 
printf('Please copy the following part:\\n')
nrow=rows(newHessian);
counter=0;
for i = 1: nrow
  for j = 1 : i
    if (j<=i)
       counter = counter + 1;
       printf('%17.10E ', newHessian(i,j) )
       if (counter==5)
          printf('\\n')
          counter=0;
       endif 
    endif
  endfor
endfor  

printf('\\n\\n')
"""
	g=open(path,'w')
	for j in range (index):
		g.write(lines[j])
	g.write(st)
	g.close()
	step4('job-ALMODE.dat',step3('job.m'))

def step3(path):
	#print 'performing step 3 ...'
	#proc = subprocess.Popen('/usr/local/octave/3.8.0/bin/octave '+path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	data = subprocess.check_output('/usr/local/octave/3.8.0/bin/octave '+path, shell=True)
	#tmp = proc.stdout.read()
	data=data.split('\n')
	ref=0
	st='\n'
	for i in data:
		if 'Please copy the following part:' in i:
			ref=1
		if ref==1 or ref==2:
			ref+=1
		if ref==3:
			st+=i+'\n'
	return st

def step4(path,ext):
	#print 'performing step 4 ...'
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	ref=0
	st=[]
	t_ref=0
	for line in lines:
		st.append(line)
		if 'NATM' in line:
			ref=1
		if ref==1 or ref==2:
			ref+=1
		if ref==3:
			st[-1]='   4\n'
			ref+=1
		if 'FFX' in line:
			st[-1]='FFXLT'
			break
		if 'APT' in line:
			ref=14
			st[-1]='NOAPT\n'
			t_ref=0
		if ref==14 or ref==15:
			ref+=1
		if ref==16:
			st.pop()
		if 'XYZ' in line:
			ref=11
			t_ref=0
		if ref==11 or ref==12:
			ref+=1
		if ref==13:
			t_ref+=1
			if t_ref==3:
				st[-1]=' '.join(st[-1].split()[:2])+'\n'
			if t_ref>3:
				st.pop()
		if 'ZA' in line:
			ref=8
			t_ref=0
		if ref==8 or ref==9:
			ref+=1
		if ref==10:
			t_ref+=1
			st[-1]=' '.join(st[-1].split()[:4])+'\n'
			if t_ref>1:
				st.pop()
		if 'AMASS' in line:
			ref=5
		if ref==5 or ref==6:
			ref+=1
		if ref==7:
			t_ref+=1
			st[-1]=' '.join(st[-1].split()[:4])+'\n'
			if t_ref>1:
				st.pop()
	st+=ext
	g=open('job-ALMODE.dat','w')
	g.write(''.join(st))
	g.close()
	step5()

def step5():
	#print 'performing step 5 ...'
	global path
	filename=path.split('/')[-1].split('.')[0]
	s1="""
 $contrl
   qcprog="ALMODE"
   iprint=0
   isymm = 1
   ifsave=.false.
   ifmolden=.true.
 $end

$qcdata
 """
 	s2='fchk="job-ALMODE.dat"'
 	s3="""$end

$LocMod $End
1 2   : W1-R1
1 3   : W1-R2
1 4 
2 1 4 
2 1 3 
1  -2  -3  -4 

"""
	f=open(filename+'.alm2','w')
	f.write(filename+'\n')
	f.write(s1)
	f.write(' '+s2+'\n')
	f.write(s3+'\n')
	f.close()

	os.system("/Users/47510753/Downloads/LocalMode-2016/lmodes.exe -b "+'< '+filename+'.alm2' +' >'+' '+filename+'.out2')
	output()

step1(path)













