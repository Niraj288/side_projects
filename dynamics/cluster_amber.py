import sys
import hbtype
import save_crd_amber as sca
import data
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import os
import cluster

def run_each_frame(file, topo):
	alld, pbc = sca.get_coord(file, topo)
	res_d = {} # contains information for each frame

	avg_dict = {}
	count = 0

	for frame in alld:
		a,b,c = pbc[frame]
		d,links_h,links_o,hbonds,obonds=data.data(alld[frame], a, b, c)

		coord = np.array([d[i][1:] for i in d])
		
		temp_d = cluster.cluster(coord, file)

		for i in temp_d:
			temp_d[i] = temp_d[i]
			if i not in avg_dict:
				avg_dict[i] = temp_d[i]
			else:
				avg_dict[i] += temp_d[i]
		count += 1

		res_d[frame] = temp_d

	print file, 'Number of frames', len(res_d)
	for i in avg_dict:
		avg_dict[i] = avg_dict[i]/count

	np.save(file[:-6]+'_CMS_perFrame.npy', res_d)
	np.save(file[:-6]+'_CMS_avg.npy', avg_dict)

def test():
	for i in os.listdir('.'):
		if i[-6:] =='.mdcrd':
			file = i 
			topo = i[:-6]+'.prmtop'
			run_each_frame(file, topo)


if __name__ == '__main__':
	#run_each_frame(sys.argv[1], sys.argv[2])
	test()


