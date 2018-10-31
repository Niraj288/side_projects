# grid search for protein folding
import sys
import protein_annealing as pfm
import rmsd
import copy
import os

score = 99999
min_params = None
count = 1

f = open('Results.txt','w')
f.close()

for NHNd1 in [2.0,2.15,2.28]:
	for NHNd2 in [2.0,2.15,2.28]:
		for NHNk1 in [15,20,25,35]:
			for NHOd1 in [2.0,2.15,2.28]:
				for NHOd2 in [2.0,2.15,2.28]:
					for NHOk1 in [15,20,25,35]:
						for NHNd3 in [2.8]:
							for NHOd3 in [2.8]:
								for ff in ['oldff/leaprc.ff14SB']:
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


							        sc = rmsd.rms(sys.argv[1],'ann.pdb')
							        if sc < score:
							        	score = sc 
							        	min_params = copy.copy(params)

							        f = open('Results.txt','a') 
							        f.write('Run '+str(count)+'\n')
							        f.write(str(params)+'\n')
							        f.write('Score : '+str(sc)+'\n\n')
							        f.close()

							        os.system('mv ann.out '+'ann_'+'0'*(4-len(str(count)))+str(count)+'.out')
							        os.system('mv ann.mdcrd '+'ann_'+'0'*(4-len(str(count)))+str(count)+'.mdcrd')
							        os.system('mv ann.pdb '+'ann_'+'0'*(4-len(str(count)))+str(count)+'.pdb')
								count+=1
f = open('Results.txt','a') 
f.write('\n\n')
f.write('Minimum rmsd has the params :'+str(min_params)+' with the rmsd of '+str(score))
f.close()








