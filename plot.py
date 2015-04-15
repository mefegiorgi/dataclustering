#plot.py

import numpy as np
from matplotlib import pyplot as plt

f = plt.figure()
f_in = open('Data/pingdata_normalised.csv')
plt.xlabel('Time')
plt.ylabel('Responsetime')
plt.title('$\sigma = 1$')
lines = []
for line in f_in.readlines():
	lines.append(line.strip().split(','))
data = np.array(lines).astype(float)
for i in range(len(data[0,1:])):
	plt.plot(data[:,0], data[:,i+1])
plt.show()