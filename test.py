import CSSIT
import time

t0 = time.time()
g = CSSIT.StatusIdentification('Data/pingdata.csv')
g.determine_n_cl()
g.clustering()
t = time.time()-t0
print t
