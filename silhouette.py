#kmeans silhouette

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from sklearn import cross_validation

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples


def array2d_to_string(arr):
	s = ''
	for l in arr:
		for c in l[:-1]:
			s = s+str(c)+','
		s = s+str(l[-1])+'\n'
	return s

def read_data(f_in):
	data = []
	ilauf = 0
	for line in f_in.readlines():
		if not ilauf==0:
			l = line.split(',')
			data.append(l)
		ilauf+=1
	data = np.array(data).astype(float)
	return data

# f_in = open('/home/winz3r/Documents/Data/z_normalized_data.csv')
f_in = open('Data/pingdata_after_pca.csv')
data = read_data(f_in)
X = data[:,:19]
f_in.close()

w_SSE = []
w_sil = []
w_time = []
for n_cl in range(2,11):
	SSE= []
	sil = []
	tim = []

	hier_labels = []
	f_in = open('Data/Kmeans/N40000PCA/kmeans_cluster_labels_K'+str(n_cl)+'.csv')
	for w in f_in.readlines():
		hier_labels.append(int(w))
	f_in.close()
	hier_labels=np.array(hier_labels)
	##Silhouette Calculation
	sil_spec = (silhouette_samples(X,hier_labels)).mean(axis=0)
	# sil_spec=0
	##SSE Calculation
	SSE_spec=0
	# for k in range(n_cl):
	# 	members = hier_labels==k
	# 	centre = X[members,:].mean(axis=0)
	# 	for x in X[members]:
	# 		SSE_spec += np.dot(x-centre,(x-centre).T)

	tim.append(n_cl)
	SSE.append(n_cl)
	sil.append(n_cl)
	tim.append(tim_spec)
	sil.append(sil_spec)
	SSE.append(SSE_spec)

	w_time.append(tim)
	w_sil.append(sil)
	w_SSE.append(SSE)


f_out = open('Data/Kmeans/kmeans_cluster_silhouette.csv', 'w')
f_out.write(array2d_to_string(w_sil))
f_out.close()

f_out = open('Data/Kmeans/kmeans_cluster_SSE.csv', 'w')
f_out.write(array2d_to_string(w_SSE))
f_out.close()

f_out = open('Data/Kmeans/kmeans_cluster_time.csv', 'w')
f_out.write(array2d_to_string(w_time))
f_out.close()




