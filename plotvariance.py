#plotvariance
from matplotlib import pyplot as plt
import numpy as np

f_in= open("Data/PCAVariance.csv")

x = []
sigma = []
percvar = []
cumvar = []
i = 1
for line in f_in.readlines():
	l= line.split(',')
	x.append(i)
	sigma.append(float(l[0]))
	percvar.append(float(l[1]))
	cumvar.append(float(l[2]))
	i=i+1

x = np.array(x)
xlabel = []
for i in x:
	xlabel.append('PC'+str(i)) 

sigma=np.array(sigma)
percvar=np.array(percvar)
cumvar=np.array(cumvar)

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.set_xlabel('Principle Components')
ax.set_ylabel('Percentage of Variance')
ax.set_title('Variance Distribution over Components')
ax.set_xticks(x)
ax.set_xticklabels(xlabel, rotation=45)
p1=ax.bar(x, cumvar, color='cornflowerblue')
p2=ax.bar(x, percvar, color='lightcoral')
ax.legend((p1,p2),('cumulative Variance', 'Variance'))
ax.grid(True)
ax.set_yscale('log',nonposy='clip')

ax = fig.add_subplot(2,1,2)
ax.set_xlabel('Principle Components')
ax.set_ylabel('Percentage of Variance')
ax.set_title('Variance Distribution over Components')
ax.set_xticks(x)
ax.set_xticklabels(xlabel, rotation=45)
p1=ax.bar(x, cumvar, color='cornflowerblue')
p2=ax.bar(x, percvar, color='lightcoral')
ax.legend((p1,p2),('cumulative Variance', 'Variance'), loc = 4)
ax.grid(True)
#plt.plot(x,percvar, 'o')
fig.tight_layout()
plt.show()