#plot.py

import numpy as np
from matplotlib import pyplot as plt

f = plt.figure()
f_in = open('Data/PrincipalComponents.csv')
plt.xlabel('Principle Component 1')
plt.ylabel('Principle Component 2')
plt.title('$\sigma = 1$')
lines = []
for line in f_in.readlines():
	lines.append(line.strip().split(','))
data = np.array(lines).astype(float)
plt.plot(data[:,0],data[:,1],'.')
plt.show()