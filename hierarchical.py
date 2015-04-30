#hierarchical

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from sklearn import cross_validation

# from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
# from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs


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

f_in = open('/home/winz3r/Documents/Data/z_normalized_data.csv')
data = read_data(f_in)
X = data[:20000,:]
f_in.close()
knn_graph = kneighbors_graph(X, 1000)

for n_cl in range(2,11):
	model = AgglomerativeClustering(connectivity='knn_graph' , linkage= 'ward', n_clusters = n_cl, memory= '/home/winz3r/Documents/Data/')
	model.fit(X)
	hier_labels = model.labels_
	SSE=0
	for k in range(n_cl):
		members = hier_labels==k
		centre = X[members,:].mean(axis=0)
		for x in X[members]:
			SSE += np.dot(x-centre,(x-centre).T)
	print SSE



