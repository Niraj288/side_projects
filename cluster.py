import numpy as np
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")

def cluster(X):
  ms = MeanShift(bandwidth=5)
  ms.fit(X)
  labels = ms.labels_
  cluster_centers = ms.cluster_centers_

  print(cluster_centers)
  n_clusters_ = len(np.unique(labels))
  print("Number of estimated clusters:", n_clusters_)

  colors = 100*['r','g','b','c','k','y','m']
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  for i in range(len(X)):
      ax.scatter(X[i][0], X[i][1], X[i][2], c=colors[labels[i]], marker='o')

  ax.scatter(cluster_centers[:,0],cluster_centers[:,1],cluster_centers[:,2],
              marker="x",color='k', s=150, linewidths = 5, zorder=10)

  plt.show()

def data_extraction(path,pdb_ref):
  file = open(path,'r')
  lines=file.readlines()
  file.close()
  X=[]
  if pdb_ref==0:
    inde1,inde2=2,6
  else:
    inde1,inde2=0,1
  for line in lines:
    if len(line.strip().split())<4:
      continue
    if 'O' in line.strip().split()[inde1]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      X.append([x,y,z])
      
    elif pdb_ref==0 and 'H'==line.strip().split()[inde1][0]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      X.append([x,y,z])
    elif pdb_ref==1 and 'H'==line.strip().split()[inde1]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      X.append([x,y,z])
  return X

def data(path,pdb_ref=0):
  X=data_extraction(path,pdb_ref)
  return X 

cluster(data('/Users/47510753/Downloads/water_test.com',1))
