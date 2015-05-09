# hierarchical

import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from sklearn import cross_validation

from sklearn.mixture import GMM
# from sklearn.cluster import AgglomerativeClustering
# from sklearn.neighbors import kneighbors_graph
# from sklearn.metrics.pairwise import pairwise_distances_argmin
# from sklearn.datasets.samples_generator import make_blobs
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

dat_name = ('Data/pingdata_after_pca.csv', '/home/winz3r/Documents/Data/z_normalized_data_cut.csv')
dir_name = 'Data/Results/Results/gmm/'

# f_in = open('/home/winz3r/Documents/Data/z_normalized_data.csv')
for d_name in dat_name:
	f_in = open(d_name)
	data = read_data(f_in)
	f_in.close()
	if d_name == 'Data/pingdata_after_pca.csv':
		dir_name = '/home/winz3r/Bachelor/dataclustering/Data/Results/Results/GMM/full/PCA/'
	if d_name == '/home/winz3r/Documents/Data/z_normalized_data_cut.csv':
		dir_name = '/home/winz3r/Bachelor/dataclustering/Data/Results/Results/GMM/full/CUT/'

	# knn_graph = kneighbors_graph(X, len(X[:,0])/10)
	for i in range(1):
		# X = []
		# for j in range(15000):
		# 	X.append(random.choice(data))
		# X = np.array(X)
		X = data
		sil_name = dir_name+'GMM_cluster_silhouette'+str(i)+'.csv'
		sse_name = dir_name+'GMM_cluster_SSE'+str(i)+'.csv'
		time_name = dir_name+'GMM_cluster_time'+str(i)+'.csv'

		w_SSE = []
		w_sil = []
		w_time = []
		for n_cl in range(2,11):
			SSE= []
			sil = []
			tim = []

			model =GMM(n_components = n_cl)
			t0 = time.time()
			model.fit(X)



			hier_labels = model.predict(X)
			label_name = dir_name+'GMM_cluster_labels_K'+str(n_cl)+'_'+str(i)+'.csv'
			f_out = open(label_name,'w')
			for w in hier_labels:
				f_out.write(str(w)+'\n')
			f_out.close()

			##Silhouette Calculation
			sil_spec = (silhouette_samples(X,hier_labels)).mean(axis=0)
			tim_spec = time.time()-t0
			##SSE Calculation
			SSE_spec=0
			for k in range(n_cl):
				members = hier_labels==k
				centre = X[members,:].mean(axis=0)
				for x in X[members]:
					SSE_spec += np.dot(x-centre,(x-centre).T)

			tim.append(n_cl)
			SSE.append(n_cl)
			sil.append(n_cl)
			tim.append(tim_spec)
			sil.append(sil_spec)
			SSE.append(SSE_spec)

			w_time.append(tim)
			w_sil.append(sil)
			w_SSE.append(SSE)


		f_out = open(sil_name, 'w')
		f_out.write(array2d_to_string(w_sil))
		f_out.close()

		f_out = open(sse_name, 'w')
		f_out.write(array2d_to_string(w_SSE))
		f_out.close()

		f_out = open(time_name, 'w')
		f_out.write(array2d_to_string(w_time))
		f_out.close()
