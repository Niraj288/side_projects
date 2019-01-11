import matplotlib.pyplot as plt
import matplotlib
import sys
import module
from sklearn.linear_model import LinearRegression
import numpy as np
import os

def save_plot(path,name):
	#print path
	s,e,t=[],[],[]
	#total_frames = 2500000
	step_frames = 200
	low_ene = 999999
	low_s = None

	f=open(path,'r')
	lines=f.readlines()
	f.close()

	for i in lines:
		if ' R M S  F L U C T U A T I O N S' in i:
			break
		if 'NSTEP =' in i:
			l=i.strip().split()
			s.append(int(l[2]))
			t.append(float(l[5]))
		if 'Etot   =' in i:
			en = float(i.strip().split()[-1])
			if low_ene > en and s[-1] > 1000:
				low_ene = en 
				low_s = s[-1]

			e.append(en)

	if len(e)!=len(t) or len(t)<5:
		return
	plt.plot(t,e,'r--')
	plt.xlabel('Time (PS)')
	plt.ylabel('Energy (PE)')
	plt.savefig(path[:-4]+'.png')
	clfe=LinearRegression()
	t_=[]
	for i in t:
		t_.append([i])
	#t_=np.reshape(t_,(1,-1))
	#print t_
	clfe.fit(t_,e)
	if '4_npt' in path:
		print path.split('/')[1].split('-')[-1],float(clfe.coef_[0])
	plt.clf()

	frame = low_s/step_frames
	print 'Lowest energy is:', low_ene,'at step:',low_s

	f = open('extract_lowest_frame.trajin','w')
	st = """trajin equil1.mdcrd frame frame 1
trajout lowest_energy_struct.pdb pdb
quit"""
	
	st = st.replace('frame',str(frame))
	f.write(st)
	f.close()

	st2 = 'cpptraj name.prmtop < extract_lowest_frame.trajin > extract_lowest_frame.out'
	st2 = st2.replace('name',name)
	print 'Saving lowest conformer as pdb file'
	os.system(st2)

	return 
	#plt.show()

def job(file):
	name = '.'.join(file.split('/')[-1].split('.')[:-1])

	save_plot('equil1.out',name)
	#module.search_deep('.',save_plot,['.out'])

if __name__=='__main__':
	job(sys.argv[1])




















