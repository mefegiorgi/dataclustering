# polar
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
	ilauf = 0
	for line in f_in.readlines():
		if not ilauf==0:
			l = line.split(',')
			data.append(l)
		ilauf+=1
	data = np.array(data).astype(float)
	return data

def cart_to_polar(x,y,z):
	r = np.sqrt(x**2+y**2+z**2)
	theta = np.arccos(z/r)
	phi = np.arctan(y/x)
	return r, theta, phi

d_name = 'Data/pingdata_after_pca.csv'
f_in = open(d_name)
data = read_data(f_in)
f_in.close()

f_out = open('Data/pingdata_pca_polar.csv','w')

for l in data:
	r, t, p = cart_to_polar(l[0],l[1],l[2])
	f_out.write(str(r)+','+str(t)+','+str(p)+'\n')
f_out.close()
