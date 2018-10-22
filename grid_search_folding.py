# grid search for protein folding
import sys
import protein_folding_modified as pfm
import rmsd
import copy

score = 99999
min_params = None

f = open('Results.txt','w')

for NHNd1 in [1.9,2.0,2.1,2.2,2.3,2.4]:
	for NHNd2 in [1.9,2.0,2.1,2.2,2.3,2.4]:
		for NHNk1 in [15,20,25,30,35,40,45]:
			for NHOd1 in [1.9,2.0,2.1,2.2,2.3,2.4]:
				for NHOd2 in [1.9,2.0,2.1,2.2,2.3,2.4]:
					for NHOk1 in [15,20,25,30,35,40,45]:
						for NHNd3 in [2.5,2.8,3.0]:
							for NHOd3 in [2.5,2.8,3.0]:
								for ff in ['oldff/leaprc.ff99SB','oldff/leaprc.ff14SB']:
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

							        sc = rmsd.rmsd('1l2y.pdb','lowest_energy_struct.pdb')
							        if sc < score:
							        	score = sc 
							        	min_params = copy.copy(params)

							        f.write('Run '+str(count)+'\n')
							        f.write(str(params)+'\n')
							        f.write('Score : '+sc+'\n')

f.write('\n\n')
f.write('Minimum rmsd has the params :'+str(min_params)+' with the rmsd of '+str(score))
f.close()







