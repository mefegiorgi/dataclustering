#K-Means
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
from sklearn import cross_validation

from sklearn.cluster import MiniBatchKMeans, KMeans
# from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs

#################################################################

#Read Data
f_in = open('Data/pingdata_after_pca.csv')
data = []
ilauf = 0
for line in f_in.readlines():
	if not ilauf==0:
		l = line.split(',')
		data.append(l)
	ilauf+=1
f_in.close()
data = np.array(data).astype(float)
# data = data[:,:70]

#Compute Clustering with kmeans
def kmeans_on_data(dataset, n_cl, save_bool, n_jobs):
	k_means = KMeans(init='random', n_clusters=n_cl, n_init=10, n_jobs=n_jobs)
	t0 = time.time()
	k_means.fit(dataset)
	t_batch = time.time() - t0
	k_means_labels = k_means.labels_
	k_means_cluster_centers = k_means.cluster_centers_
	k_means_labels_unique = np.unique(k_means_labels)
	# This Option saves the Clustercenters and labels for the data 
	# Also Plots the Data with Clusterlabels
	if save_bool:
		f_labels = open('Data/kmean_labels_k'+str(n_cl)+'.csv','w')
		f_cl_centers = open('Data/kmeans_ccenters_k'+str(n_cl)+'.csv','w')
		for c in k_means_labels:
			s = str(c)+'\n'
			f_labels.write(s)
		for c in range(len(k_means_cluster_centers[:,0])):
			line = ''
			for c2 in k_means_cluster_centers[c,:-2]:
				line = line + str(c2) + ','
			line = line + str(k_means_cluster_centers[c,-1]) + '\n'
			f_cl_centers.write(line)
		f_labels.close()
		f_cl_centers.close()

	# Plotting the Clusters
		fig = plt.figure()
		colors = cm.gist_rainbow(np.linspace(0, 1, n_cl))
		ax = fig.add_subplot(1,1,1)
		ax.set_title('K-Means Clustering with $K = '+str(n_cl) +'$, Inertia $= '+str(k_means.inertia_)+'$')
		ax.set_xlabel('PC1')
		ax.set_ylabel('PC2')
		# 
		C_Labels = []
		for i,clu in enumerate(k_means_cluster_centers):
			C_Labels.append('Cluster '+ str(i+1))
		Ps = []
		for k,col in zip(range(n_cl),colors):
			my_members = k_means_labels==k
			cluster_center = k_means_cluster_centers[k]
			ax.plot(data[my_members,0], data[my_members,1],linestyle='', markerfacecolor = col, marker='.')
			Ps.append(ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6, label = C_Labels[k]))
		
		ax.legend(loc = 'upper left', bbox_to_anchor = (0.85,1.00), fontsize = 12, markerscale = 0.7, numpoints = 1)
		plt.savefig('Plots/K-Means_k'+str(n_cl)+'.pdf', format = 'pdf')

		ax.set_xlim([-5,15])
		ax.set_ylim([-10,4])
		plt.savefig('Plots/K-Means_small_k'+str(n_cl)+'.pdf', format = 'pdf')
		plt.close('all')

	return k_means

f_out = open('Data/val.csv','w')

for K in range(2,11):
	k_means = kmeans_on_data(data, K, True, 4)
	meanInertia = 0
	meanscore = 0 
	for i in range(10):
		X_test = []
		for i in range(len(data[:,0]/10)):
			X_test.append(random.choice(data))
		X_test = np.array(X_test)
		val_means = kmeans_on_data(X_test,K,False, 4)
		meanscore += k_means.score(X_test)/10.
		meanInertia += val_means.inertia_/10.
	f_out.write(str(K)+','+str(meanInertia)+','+str(meanscore)+'\n')

f_out.close()