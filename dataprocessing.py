inname = 'Data/pingdata.csv'
f_in = open(inname)
outname = (inname.split('.'))[0]+'_processed.csv'
f_out = open(outname, 'w')
for line in f_in:
	line = (line.split('\r\n'))[0]
	columns = line.split(',')
	line_is_okay = True
	i = 2
	while line_is_okay and i< len(columns):
		if columns[i] == '-1' or columns[i] == 'none':
			line_is_okay = False
		i+=1
	if line_is_okay:
		newline = columns[0]
		for c in columns[2:]:
			newline = newline + ',' + c
		newline = newline + '\n'
		f_out.write(newline)

f_in.close()
f_out.close()
	
