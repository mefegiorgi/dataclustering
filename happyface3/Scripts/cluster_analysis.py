import CSSIT

inname = '/var/lib/HappyFace3/Scripts/pingdata.csv'
outname = '/var/lib/HappyFace3/Scripts/cluster_log.csv'
confname = '/var/lib/HappyFace3/Scripts/config.cfg'
g = CSSIT.StatusIdentification(inname, confname)
analysis = g.clustering()

f_out = open(outname, 'w')
for line in analysis:
	string = ''
	for entry in line:
		string = string + str(entry)+','
	f_out.write(string[:-1]+'\n')
f_out.close()

