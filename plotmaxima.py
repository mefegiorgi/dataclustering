import numpy as np
from matplotlib import pyplot as plt

f_in = open('Data/pingdata_processed.csv')
data = []
ilauf = 0
for line in f_in.readlines():
	if not ilauf==0:
		l = line.split(',')
		data.append(l)
	ilauf+=1
data = np.array(data).astype(float)
data = data[:,1:]
f_in.close()

x = np.arange(1,len(data[0,:])+1)
maxima = data.max(axis=0)
minima = data.min(axis=0)
means = data.mean(axis=0)
dev = data.std(axis=0)

fig = plt.figure()
ax = fig.add_subplot(4,1,1)
ax.set_xlabel('Service')
ax.set_ylabel('Responsetime')
ax.set_xticks(x[::10])
ax.set_yticks(range(0,180000,40000))

ax.set_title('Maxima')

pmax = ax.bar(x,maxima,color='cornflowerblue')

ax = fig.add_subplot(4,1,2)
ax.set_xlabel('Service')
ax.set_ylabel('Responsetime')
ax.set_xticks(x[::10])
ax.set_yticks(range(0,18,4))

ax.set_title('Minima')

pmin = ax.bar(x,minima,color='khaki')

ax = fig.add_subplot(4,1,3)
ax.set_xlabel('Service')
ax.set_ylabel('Responsetime')
ax.set_xticks(x[::10])
ax.set_yticks(range(0,180,40))

ax.set_title('Means')

pmean = ax.bar(x,means, color='lightcoral')

ax = fig.add_subplot(4,1,4)
ax.set_xlabel('Service')
ax.set_ylabel('Responsetime')
ax.set_xticks(x[::10])

ax.set_title('Standard Deviation')

pmean = ax.bar(x,dev, color='seagreen')

fig.tight_layout()

plt.show()






