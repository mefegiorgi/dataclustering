#plotvar

import numpy as np
from matplotlib import pyplot as plt

f_in = open('Data/val.csv')

K= []
I = []

for line in f_in.readlines():
	l = line.split(',')
	K.append(l[0])
	I.append(l[1])

K = np.array(K).astype(float)
I = np.array(I).astype(float)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title('elbow plot')
ax.set_xlabel('number of clusters')
ax.set_ylabel('Inertia')
ax.set_xticks(K)
Klabel = []
for k in K:
	Klabel.append(str(k))
ax.set_xticklabels(Klabel)

ax.plot(K,I,'o', linestyle='-')
fig.tight_layout()
plt.show()