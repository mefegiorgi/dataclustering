import numpy as np

def array2d_to_string(arr):
	s = ''
	line = 0
	for l in arr:
		line +=1
		column = 0
		for c in l[:-1]:
			column +=1
			s = s+str(c)+','
			print (line, column)
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

f_in = open('/home/winz3r/Documents/Data/z_normalized_data.csv')
data = read_data(f_in)
f_in.close()


for i in range(len(data)):
	for j in range(len(data[i,:])):
		if data[i,j]>500.:
			data[i,j]=500.

f_out = open('/home/winz3r/Documents/Data/z_normalized_data_cut.csv','w')
for n in data.astype(str):
	newline = str(n[0])
	for c in n[1:]:
		newline = newline + ',' + str(c)
	newline = newline +'\n'
	f_out.write(newline)
f_out.close()

