import os
import numpy as np
ne={}

for i in os.listdir('.'):
	if i[-9:]=='final.npy':
		d=np.load(i).item()
		for j in d:
			ne[j.split('/')[-1].split('.')[0]]=float(d[j][-1])
np.save('pka.npy',ne)

