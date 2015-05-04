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

s_title = 'K-Means'

data = read_data(f_in)
f_in.close()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('Validation Plot: '+ s_title)
ax.set_xlabel('Number of Clusters')
ax.set_ylabel('$(SSE-<SSE\'>)/\sigma $[s]')
ax.set_xticks(data[:,0])
Klabel = []
for k in data[:,0]:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)
print data
yerr= data[:,3]
# ax.errorbar(data[:,0],data[:,2], fmt ='o',yerr=yerr, linestyle='-', color='red')
ax.errorbar(data[:,0],(data[:,1]-data[:,2])/data[:,3],fmt='o', linestyle='-', color='green')
fig.tight_layout()
plt.show()
plt.close('all')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('Validation Plot: '+ s_title)
ax.set_xlabel('Number of Clusters')
ax.set_ylabel('SSE [s$^2$]')
ax.set_xticks(data[:,0])
Klabel = []
for k in data[:,0]:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)
yerr= data[:,3]
for i in range(4,len(data[0,:])):
	ax.plot(data[:,0].astype(int),data[:,i],'o', linestyle='-', color='red')
ax.plot(data[:,0].astype(int),data[:,1],'o', linestyle='-', color='green')
fig.tight_layout()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('Validation Plot: '+ s_title)
ax.set_xlabel('Number of Clusters')
ax.set_ylabel('SSE [s$^2$]')
ax.set_xticks(data[:,0])
Klabel = []
for k in data[:,0]:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)
yerr= data[:,3]
# for i in range(4,len(data[0,:])):
	# ax.plot(data[:,0],data[:,i],'o', linestyle='-', color='red')
ax.plot(data[:,0].astype(int),data[:,1],'o', linestyle='-', color='green', label='Standard Data')
ax.errorbar(data[:,0].astype(int),data[:,2], fmt='o', yerr=data[:,3], linestyle='-', color='red', label='Mean of shuffled Data')
ax.legend(loc = 1)
fig.tight_layout()
plt.show()