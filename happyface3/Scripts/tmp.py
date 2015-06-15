f_in = open('pingdata_old.csv')
f_out = open('pingdata.csv','w')
for l in f_in.readlines():
	w_l = l[:-1]+',\n'
	f_out.write(w_l)
f_in.close()
f_out.close()

	
