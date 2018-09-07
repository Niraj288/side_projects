from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import save_crd_amber as amb
import numpy as np
import sys

d=amb.get_coord(sys.argv[1],sys.argv[2])[0]
df = np.array([d[i][1:] for i in d])
print df
print df.shape

tsne=TSNE(n_components=2,verbose=1,perplexity=40,n_iter=300)

tsne_results=tsne.fit_transform(df)
plt.scatter(tsne_results[:,0],tsne_results[:,1])
plt.show()
