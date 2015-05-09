#silhouette plot

import numpy as np
from matplotlib import pyplot as plt

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
		l = line.split(',')
		data.append(l)
		ilauf+=1
	data = np.array(data).astype(float)
	return data




# hierarchical

arr_TYP = ('hierarchichal', 'kmeans','GMM')
arr_STRU = ('CUT', 'PCA')

hier_pca_sil = []
hier_pca_sse = []
hier_cut_sil = []
hier_cut_sse = []

kmeans_pca_sil = []
kmeans_pca_sse = []
kmeans_cut_sil = []
kmeans_cut_sse = []

gmm_pca_sil = []
gmm_pca_sse = []
gmm_cut_sil = []
gmm_cut_sse = []


for TYP in arr_TYP:
	for STRU in arr_STRU:

		sse_names = []
		sil_names = []
		tempSSE_name = 'Data/Results/Results/'+TYP+'/'+STRU+'/'+TYP+'_cluster_SSE'
		tempSIL_name = 'Data/Results/Results/'+TYP+'/'+STRU+'/'+TYP+'_cluster_silhouette'

		for i in range(10):
			tsse = tempSSE_name+str(i)+'.csv'
			tsil = tempSIL_name+str(i)+'.csv'
			sse_names.append(tsse)
			sil_names.append(tsil)

		f_in = open(sse_names[0])
		sse_data = read_data(f_in)
		f_in.close()

		for s in sse_names[1:]:
			f_in = open(s)
			tmp_data=read_data(f_in)
			f_in.close()
			sse_data = np.insert(sse_data, len(sse_data[0,:]), tmp_data[:,1],  axis = 1)

		f_in = open(sil_names[0])
		sil_data = read_data(f_in)
		f_in.close()

		for s in sil_names[1:]:
			f_in = open(s)
			tmp_data=read_data(f_in)
			f_in.close()
			sil_data = np.insert(sil_data, len(sil_data[0,:]), tmp_data[:,1],  axis = 1)

		if TYP=='hierarchichal' and STRU=='CUT':
			hier_cut_sil = sil_data
			hier_cut_sse = sse_data
		if TYP=='hierarchichal' and STRU=='PCA':
			hier_pca_sil = sil_data
			hier_pca_sse = sse_data
		if TYP=='kmeans' and STRU=='CUT':
			kmeans_cut_sil = sil_data
			kmeans_cut_sse = sse_data
		if TYP=='kmeans' and STRU=='PCA':
			kmeans_pca_sil = sil_data
			kmeans_pca_sse = sse_data
		if TYP=='GMM' and STRU=='CUT':
			gmm_cut_sil = sil_data
			gmm_cut_sse = sse_data
		if TYP=='GMM' and STRU=='PCA':
			gmm_pca_sil = sil_data
			gmm_pca_sse = sse_data

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_xlabel('Number of Clusters')
# ax.set_title('SSE for Clustering on normalised data')
# ax.set_ylabel('SSE [s$^2$]')
# p1 = ax.errorbar(hier_cut_sse[:,0], hier_cut_sse[:,1:].mean(axis=1), yerr=hier_cut_sse[:,1:].std(axis=1), color= 'red')
# p2 = ax.errorbar(kmeans_cut_sse[:,0], kmeans_cut_sse[:,1:].mean(axis=1), yerr=kmeans_cut_sse[:,1:].std(axis=1), color = 'green')
# ax.legend((p1,p2),('hierarchichal', 'kmeans'))
# fig.tight_layout()
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Number of Clusters')
ax.set_title('Silhouette Coefficient for Clustering on normalised data')
ax.set_ylabel('Silhouette Coefficient')
p1 = ax.errorbar(hier_cut_sil[:,0], hier_cut_sil[:,1:].mean(axis=1), yerr=hier_cut_sil[:,1:].std(axis=1), color= 'red')
p2 = ax.errorbar(kmeans_cut_sil[:,0], kmeans_cut_sil[:,1:].mean(axis=1), yerr=kmeans_cut_sil[:,1:].std(axis=1), color = 'green')
p3 = ax.errorbar(gmm_cut_sil[:,0], gmm_cut_sil[:,1:].mean(axis=1), yerr=gmm_cut_sil[:,1:].std(axis=1), color = 'blue')
ax.legend((p1,p2, p3),('hierarchichal', 'kmeans', 'gmm'))
fig.tight_layout()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Number of Clusters')
ax.set_title('Silhouette Coefficient for Clustering on PCA-transformed data')
ax.set_ylabel('Silhouette Coefficient')
p1 = ax.errorbar(hier_pca_sil[:,0], hier_pca_sil[:,1:].mean(axis=1), yerr=hier_pca_sil[:,1:].std(axis=1), color= 'red')
p2 = ax.errorbar(kmeans_pca_sil[:,0], kmeans_pca_sil[:,1:].mean(axis=1), yerr=kmeans_pca_sil[:,1:].std(axis=1), color = 'green')
p3 = ax.errorbar(gmm_pca_sil[:,0], gmm_pca_sil[:,1:].mean(axis=1), yerr=gmm_pca_sil[:,1:].std(axis=1), color = 'blue')
ax.legend((p1,p2, p3),('hierarchichal', 'kmeans', 'gmm'))
fig.tight_layout()
plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_xlabel('Number of Clusters')
# ax.set_title('SSE for Clustering on PCA-transformed data')
# ax.set_ylabel('SSE [s$^2$]')
# p1 = ax.errorbar(hier_pca_sse[:,0], hier_pca_sse[:,1:].mean(axis=1), yerr=hier_pca_sse[:,1:].std(axis=1), color= 'red')
# p2 = ax.errorbar(kmeans_pca_sse[:,0], kmeans_pca_sse[:,1:].mean(axis=1), yerr=kmeans_pca_sse[:,1:].std(axis=1), color = 'green')
# p3 = ax.errorbar(gmm_pca_sse[:,0], gmm_pca_sse[:,1:].mean(axis=1), yerr=gmm_pca_sse[:,1:].std(axis=1), color = 'blue')
# ax.legend((p1,p2),('hierarchichal', 'kmeans'))
# fig.tight_layout()
# plt.show()
