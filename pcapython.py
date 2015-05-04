from sklearn.decomposition import PCA

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

f_in = open('/home/winz3r/Documents/Data/z_normalized_data_cut.csv')
data = []
ilauf = 0
for line in f_in.readlines():
	if not ilauf==0:
		l = line.split(',')
		data.append(l)
	ilauf+=1
f_in.close()
data = np.array(data).astype(float)

pca = PCA()
pca.fit(data)
pca_score = pca.explained_variance_ratio_
V = pca.components_
V = np.matrix(V)

f_out = open("Data/PCA/pca_components.csv",'w')
for n in pca.components_.astype(str):
	newline = str(n[0])
	for c in n[1:]:
		newline = newline + ',' + str(c)
	newline = newline +'\n'
	f_out.write(newline)
f_out.close()

newdata = np.zeros_like(data)
for i in range(len(data[:,0])):
# for i in range(5):
	newdata[i,:] = np.dot(V,data[i,:])

f_out = open('Data/pingdata_after_pca.csv','w')

for n in newdata.astype(str):
	newline = str(n[0])
	for c in n[1:]:
		newline = newline + ',' + str(c)
	newline = newline +'\n'
	f_out.write(newline)
f_out.close()

# print newdata[0,:]

# plt.plot(newdata[:,0],newdata[:,1], '.')
# plt.show()





