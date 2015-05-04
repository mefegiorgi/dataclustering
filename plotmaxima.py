import numpy as np
from matplotlib import pyplot as plt

def as_decimal(x):
	return str(float(int(x*10))/10.)

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
median = np.median(data, axis=0)
dev = data.std(axis=0)

# fig = plt.figure()
# ax = fig.add_subplot(4,1,1)
# ax.set_xlabel('Service')
# ax.set_ylabel('Responsetime [s]')
# ax.set_xticks(x[::10])
# ax.set_yticks(range(0,180000,40000))

# ax.set_title('Maxima')

# pmax = ax.bar(x,maxima,color='cornflowerblue')

# ax = fig.add_subplot(4,1,2)
# ax.set_xlabel('Service')
# ax.set_ylabel('Responsetime [s]')
# ax.set_xticks(x[::10])
# ax.set_yticks(range(0,18,4))

# ax.set_title('Minima')

# pmin = ax.bar(x,minima,color='khaki')

# ax = fig.add_subplot(4,1,3)
# ax.set_xlabel('Service')
# ax.set_ylabel('Responsetime [s]')
# ax.set_xticks(x[::10])
# ax.set_yticks(range(0,180,40))

# ax.set_title('Means')

# pmean = ax.bar(x,means, color='lightcoral')

# ax = fig.add_subplot(4,1,4)
# ax.set_xlabel('Service')
# ax.set_ylabel('Responsetime [s]')
# ax.set_xticks(x[::10])

# ax.set_title('Standard Deviation')

# pmean = ax.bar(x,dev, color='seagreen')

I=0
fig2 = plt.figure()
ax = fig2.add_subplot(1,1,1)
data = data.reshape(-1)
data = data[data<500.]
# data = np.log10(data)
# print data, len(data), 39000*141
ax.hist(data,100)
ax.set_title('Histogram of measured Responsetimes of all Services combined')
ax.text(110000, 10**6, "Mean = "+as_decimal(means.mean())+"s\nMedian = "+as_decimal(np.median(median))+"s\nMaximum = "+as_decimal(maxima.max())+"s\nMinimum = "+as_decimal(minima.min())+"s\nStd. Deviation = "+as_decimal(dev.std())+"s", size=15, rotation=0,
         ha="left", va="top",
         bbox = dict(boxstyle="square",
         			alpha = 0.5
                     )
        )
# ax.set_xlabel('Responsetime $log_{10}([s])$')
ax.set_xlabel('Responsetime [s]')
ax.set_ylabel('Number of Occurences')
ax.set_yscale('log',nonposy='clip')
# ax.set_xscale('log',nonposy='clip')
ax.grid(True)


fig2.tight_layout()

plt.show()






