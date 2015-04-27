#plotvar

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
	for line in f_in.readlines():
		l = line.split(',')
		data.append(l)
	data = np.array(data).astype(float)
	return data

f_in = open('Data/val.csv')

# K= []
# I = []

data = read_data(f_in)

# K = np.array(K).astype(float)
# I = np.array(I).astype(float)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('elbow plot')
ax.set_xlabel('number of clusters')
ax.set_ylabel('$(SSE-<SSE\'>)/\sigma$')
ax.set_xticks(data[:,0])
Klabel = []
for k in data[:,0]:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)
print data
yerr= data[:,3]
# ax.errorbar(data[:,0],data[:,2], fmt ='o',yerr=yerr, linestyle='-', color='red')
ax.plot(data[:,0],(data[:,1]-data[:,2])/data[:,3],'o', linestyle='-', color='green')
fig.tight_layout()
plt.show()
plt.close('all')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('elbow plot')
ax.set_xlabel('number of clusters')
ax.set_ylabel('SSE')
ax.set_xticks(data[:,0])
Klabel = []
for k in data[:,0]:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)
yerr= data[:,3]
for i in range(4,len(data[0,:])):
	ax.plot(data[:,0],data[:,i],'o', linestyle='-', color='red')
ax.plot(data[:,0],data[:,1],'o', linestyle='-', color='green')
fig.tight_layout()
plt.show()
