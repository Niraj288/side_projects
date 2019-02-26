import sys
import hbtype
import save_crd_amber as sca
import data
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import os
import rings

def run_each_frame(file, topo):
	alld, pbc = sca.get_coord(file, topo)
	res_d = {} # contains information for each frame

	avg_dict = {}
	count = 0

	for frame in alld:
		a,b,c = pbc[frame]
		d,links_h,links_o,hbonds,obonds=data.data(alld[frame], a, b, c)
		
		temp_d = rings.job(d,links_h,links_o,hbonds,obonds,a,b,c)

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

	print res_d
	print avg_dict

	np.save(file[:-6]+'_RING_perFrame.npy', res_d)
	np.save(file[:-6]+'_RING_avg.npy', avg_dict)

def test():
	for i in os.listdir('.'):
		if i[-6:] =='.mdcrd':
			file = i 
			topo = i[:-6]+'.prmtop'
			run_each_frame(file, topo)

def visual(alld):
	avg_dict = {}
	count = 0

	for frame in alld:
		
		temp_d = alld[frame]

		for i in temp_d:
			temp_d[i] = temp_d[i]
			if i not in avg_dict:
				avg_dict[i] = temp_d[i]
			else:
				avg_dict[i] += temp_d[i]
		count += 1

	res = avg_dict

	lis = []
	for i in res:
		lis.append([res[i], i])

	lis.sort(reverse = True)
	#lis.sort()

	x_labels = [i[1] for i in lis if i[0]!= 0]
	frequencies = [i[0] for i in lis if i[0]!=0]

	print file, x_labels[0], frequencies[0]

	#print lis

	plt.figure(figsize=(12, 8))
	freq_series = pd.Series.from_array(frequencies)
	ax = freq_series.plot(kind='bar')
	ax.set_ylabel('Frequency')
	ax.set_xticklabels(x_labels)

	#plt.savefig(file+'.png')
	plt.show()

def observations(alld):
	avg_dict = {}
	count = 0

	for frame in alld:
		
		temp_d = alld[frame]

		for i in temp_d:
			temp_d[i] = temp_d[i]
			if i not in avg_dict:
				avg_dict[i] = temp_d[i]
			else:
				avg_dict[i] += temp_d[i]
		count += 1
	return avg_dict

def write_o():
	fd = {}
	st_file = 'Type '
	st = []
	count = 0
	f_d = {}
	labels = set()
	for i in os.listdir('.'):
		if i[-17:] =='RING_perFrame.npy':

			

			#print i
			d = observations(np.load(i).item())
			filename = i[:-18]
			filename = filename.replace('-','_')

			if filename not in fd:
				fd[filename] = count
				count+=1

			for j in d:
				labels.add(j)

				f_d[(filename, j)] = d[j] 

	for j in fd:
		st_file += j +' ' 
				
	print st_file+' count'
	labels = list(labels)

	for i in range (len(labels)):
		st = str(labels[i])+' '
		ref = 0
		for j in fd:
			if (j,labels[i]) not in f_d:
				st += '0 '
			else:
				st +=  str(f_d[(j,labels[i])])+' '
				ref += f_d[(j,labels[i])]
		if ref != 0:
			print st+str(ref)+' '


if __name__ == '__main__':
	#run_each_frame(sys.argv[1], sys.argv[2])
	#test()

	#f = sys.argv[1].split('.')[0]
	#d = np.load(sys.argv[1]).item()

	#visual(d) # give RING_perFrame.npy

	write_o()


