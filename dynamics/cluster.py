import numpy as np
from sklearn.cluster import MeanShift
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
import pandas as pd
#style.use("ggplot")

def data_extraction(path,pdb_ref=0):
  file = open(path,'r')
  lines=file.readlines()
  file.close()
  o,h,o_ref,h_ref=[],[],0,0
  o_refe,h_refe={},{}
  d,d_ref={},0
  ref=1
  if pdb_ref==0:
    inde1,inde2=2,6
  else:
    inde1,inde2=0,1
  lis=[]
  for line in lines:
    if len(line.strip().split())<4:
      continue
    if 'O' in line.strip().split()[inde1]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      d[ref]=['O',x,y,z]
      o.append([x,y,z])
      o_refe[o_ref]=ref
      o_ref+=1
      ref+=1
      lis.append([x,y,z])
    elif pdb_ref==0 and 'H'==line.strip().split()[inde1][0]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      d[ref]=['H',x,y,z]
      h.append([x,y,z])
      h_refe[h_ref]=ref 
      h_ref+=1
      ref+=1
      lis.append([x,y,z])
    elif pdb_ref==1 and 'H'==line.strip().split()[inde1]:
      x,y,z=map(float,line.strip().split()[inde2:inde2+3])
      d[ref]=['H',x,y,z]
      h.append([x,y,z])
      h_refe[h_ref]=ref 
      h_ref+=1
      ref+=1
      lis.append([x,y,z])
  return lis

def count(lis):
  #print np.unique(lis)
  d={}
  for i in lis:
    if i in d:
      d[i]+=1
    else:
      d[i]=1
  for i in d:
    pass
    #print i,d[i]
  df = {}
  for i in d:
    if d[i] in df:
      df[d[i]]+=1
    else:
      df[d[i]] = 1

  return df

def visual(labels, X, filename):
  colors = 100*['r','g','b','c','k','y','m']
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  for i in range(len(X)):
      ax.scatter(X[i][0], X[i][1], X[i][2], c=colors[labels[i]], marker='o', s= 50, alpha = 0.8)

  # ax.scatter(cluster_centers[:,0],cluster_centers[:,1],cluster_centers[:,2],
  #             marker="x",color='k', s=150, linewidths = 5, zorder=10)

  plt.savefig(filename+'.png')

def visual2(res, file):
  lis = []
  for i in res:
    lis.append([res[i], i])

  lis.sort(reverse = True)

  x_labels = [i[1] for i in lis if i[0]!= 0]
  frequencies = [i[0] for i in lis if i[0]!=0]

  #print lis

  plt.figure(figsize=(12, 8))
  freq_series = pd.Series.from_array(frequencies)
  ax = freq_series.plot(kind='bar')
  ax.set_ylabel('Frequency')
  ax.set_xticklabels(x_labels)

  plt.show()

def cluster(X, file): # give coord and filename
  ms = MeanShift(bandwidth=5,bin_seeding=False,min_bin_freq=1)
  ms.fit(X)
  labels = ms.labels_
  cluster_centers = ms.cluster_centers_

  filename = file[:-6]
  #visual(labels, X, filename)
  #print(cluster_centers)
  n_clusters_ = len(np.unique(labels))
  print("Number of estimated clusters:", n_clusters_)

  df = count(labels)

  return df

def data():
  X=np.array(data_extraction('/Users/47510753/Downloads/test-2.pdb',0))
  #X, _ = make_blobs(n_samples = 10, centers = 10 ,n_features=3)
  return X 

if __name__ == '__main__':
  print cluster(data(), '')
  #visual2(cluster(data(), 'test.mdcrd'), 'test.mdcrd')















