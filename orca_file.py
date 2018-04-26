
import subprocess
import os
import atom_data

def xyz_value(path):
	data = subprocess.check_output('gcartesian '+path, shell=True)
	data=data.split('\n')
	d=atom_data.data(sys.argv[0])
	ref=1
	for l in data[1:]:
		a,x,y,z=l.strip().split()
		try:
			int(a)
			a=d[int(a)]['Symbol']
		except TypeError:
			pass
		data[ref]='    '.join([a,x,y,z])
		ref+=1
	'\n'.join(data)

	return '* xyz '+data+'\n'

def func(path):
	s0='! DLPNO-CCSD(T) ECP{aug-cc-pVTZ-PP} aug-cc-pVTZ AutoAux TightSCF XYZFile PModel\n'
	filename=path.split('/')[-1].split('.')[0]
	s1='%id "'+filename+'"\n%base "'+filename+'"\n'
	s2='%MaxCore 10000\n%pal nprocs 8\nend\n'
	s3=xyz_value(path)
	s4='* \n\n'
	return s0+s1+s2+s3+s4

def job():
	mode=raw_input('Enter mode : ')
	path=raw_input('Enter path : ')
	ref=raw_input('Make all .g16.out files ?? (y/n) : ')
	li=[]
	try:
		for i in os.listdir(path):
			if '.g16.out'==i[-8:]:
				if ref=='y' or raw_input('Is the file '+i+' an input ?? (y/n) : ')=='y':
					filename=i.split('.')[0]
					f=open(filename+'.orca','w')
					f.write(func(i))
					f.close()
					li.append(filename+'.orca')
	except OSError:
		filename=path.split('.')[0]
                f=open(filename+'.orca','w')
                f.write(func(i))
                f.close()
                li.append(filename+'.orca')
	for i in li:
		os.system('orcarun '+i+' '+mode)

job()
