import connections
import os
import data
import save_crd_amber as amb
import sys
import numpy as np
import time 

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

def job():
	if 'dict.npy' in os.listdir('.'):
		alld=np.load('dict.npy').item()
	else: 
		t=time.time()
		print 'Extracting coords from amber files ...\n'
		alld=amb.get_coord(sys.argv[1],sys.argv[2])
		np.save('dict.npy',alld)
		print 'Done in '+str(time.time()-t)+' seconds'
	print alld[0]
	f=open('clusters.txt','w')
	total=100
	for i in range (total):
		progress(i, total, status='Progress ')
		d,links_h,links_o,hbonds,obonds=data.data(alld[i])
		graph=connections.connectivity(d,links_h,links_o,hbonds,obonds)
		f.write(connections.write_o(graph,d))
	f.close()

if __name__=='__main__':
	job()




