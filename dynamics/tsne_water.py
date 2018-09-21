from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import save_crd_amber as amb
import numpy as np
import sys
import data
import connections
import warnings
warnings.simplefilter('ignore', DeprecationWarning)
plt.style.use('ggplot')

def write_o(graph,d):
	#file=open('output.txt','w')
	mers={}
	for i in graph:
		if len(i) not in mers:
			mers[len(i)]=[i]
		else:
			mers[len(i)].append(i)
	arr=[0]*3000
	for i in mers:
		print i, len(mers[i])
		for k in mers[i]:
			for j in k:
				if i==3:
					arr[j-1]=[0,0,0.9,0.3]
				elif i==6:
					arr[j-1]=[0,0.9,0,1]
				else:
					arr[j-1]=[0.9,0,0,1]
	#print arr
	return np.array(arr)

#d=amb.get_coord(sys.argv[1],sys.argv[2])[0]
d=np.load(sys.argv[1]).item()
d,links_h,links_o,hbonds,obonds=data.data(d)
graph=connections.connectivity(d,links_h,links_o,hbonds,obonds)
labels = write_o(graph,d)

#print graph

df = np.array([d[i][1:] for i in d])
#print df
print df.shape

tsne=TSNE(n_components=2,verbose=1,perplexity=300,n_iter=5000)

tsne_results=tsne.fit_transform(df)
plt.scatter(tsne_results[:,0],tsne_results[:,1], c=labels)
plt.show()



