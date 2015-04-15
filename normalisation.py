from scipy.ndimage.filters import gaussian_filter
import numpy as np


sigma = 1

inname = 'Data/pingdata_processed.csv'
f_in = open(inname)

lines = []
for line in f_in.readlines():
	lines.append(line.strip().split(','))
data = np.array(lines).astype(float)

enum = data[:,0]
out = gaussian_filter(data[:,1:], sigma)
new = np.insert(out,0, enum, axis = 1)

new = new.astype(str)
print new[-1]
f_in.close()
f_out = open('Data/pingdata_normalised.csv','w')
for n in new:
	newline = n[0]
	for c in n[1:]:
		newline = newline + ',' + c
	newline = newline +'\n'
	f_out.write(newline)


f_out.close()
