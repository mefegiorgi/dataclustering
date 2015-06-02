import CSSIT
import time



t0 = time.time()
g = CSSIT.StatusIdentification('Data/pingdata.csv')
analysis = g.clustering()

f_out = open('analysis.csv', 'w')
for line in analysis:
    string = ''
    for entry in line:
        string = string + str(entry)+','
    f_out.write(string[:-1]+'\n')

f_out.close()
t = time.time()-t0
print t
