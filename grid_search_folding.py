# grid search for protein folding
import sys
import protein_folding_modified as pfm
import rmsd
import copy
import os

def save_plot(path,name):
	#print path
	s,e,t=[],[],[]
	#total_frames = 2500000

	step_frames = 50
	print 'step frame used :',step_frames
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

score = 99999
min_params = None
count = 1

f = open('Results.txt','w')
f.close()

for NHNd1 in [1.9,2.0,2.1,2.2,2.3,2.4]:
	for NHNd2 in [1.9,2.0,2.1,2.2,2.3,2.4]:
		for NHNk1 in [15,20,25,30,35,40,45]:
			for NHOd1 in [1.9,2.0,2.1,2.2,2.3,2.4]:
				for NHOd2 in [1.9,2.0,2.1,2.2,2.3,2.4]:
					for NHOk1 in [15,20,25,30,35,40,45]:
						for NHNd3 in [2.5,2.8,3.0]:
							for NHOd3 in [2.5,2.8,3.0]:
								for ff in ['oldff/leaprc.ff99SB','oldff/leaprc.ff14SB']:
									if NHNd1 > NHNd2 or NHOd1 > NHOd2:
										continue
									params = {'NH-Nd0':1.5,
							            'NH-Nd1':NHNd1,
							            'NH-Nd2':NHNd2,
							            'NH-Nd3':NHNd3,
							            'NH-Nk1':NHNk1,
							            'NH-Nk2':NHNk1,
							            'NH-Od0':1.5,
							            'NH-Od1':NHOd1,
							            'NH-Od2':NHOd2,
							            'NH-Od3':NHOd3,
							            'NH-Ok1':NHOk1,
							            'NH-Ok2':NHOk1,
							            'steps':25000,
							            'ff':ff}

							        pfm.run_folding(sys.argv[1], sys.argv[1].split('.')[-1], params)
							        job(sys.argv[1])


							        sc = rmsd.rms(sys.argv[1],'lowest_energy_struct.pdb')
							        if sc < score:
							        	score = sc 
							        	min_params = copy.copy(params)

							        f = open('Results.txt','a') 
							        f.write('Run '+str(count)+'\n')
							        f.write(str(params)+'\n')
							        f.write('Score : '+str(sc)+'\n\n')
							        f.close()

							        os.system('mv equil1.out '+'equi_'+'0'*(4-len(str(count)))+str(count)+'.out')
							        os.system('mv lowest_energy_struct.pdb '+'equi_'+'0'*(4-len(str(count)))+str(count)+'.pdb')
								count+=1
f = open('Results.txt','a') 
f.write('\n\n')
f.write('Minimum rmsd has the params :'+str(min_params)+' with the rmsd of '+str(score))
f.close()








