#------------------------------------------------------------
# COMPOSITE SERVICE STATUS IDENTIFICATION TOOL V.0.1
#
#
#
#
#
#
#
#------------------------------------------------------------

import numpy as np
from matplotlib import pyplot as plt
import random
from sklearn import cross_validation
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import scipy.signal as signal
from sklearn.decomposition import PCA

class StatusIdentification:
    path_to_data = ''
    raw_data = []
    processed_data = []
    pca_components = []
    pca_data = []
    sample = []
    N_Points = 30
    Std_Dev = 5
    cut_value = 500
    sample_size = 5000


#--------------------------------------------------------------
# FUNCTIONS
#--------------------------------------------------------------

    def __init__(self, filename):
        self.path_to_data = filename
        self.__process_data()

    def __array2d_to_file(arr):
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

    def __read_data(self, filename):
        f_in = open(filename)
    	data = []
    	ilauf = 0
    	for line in f_in.readlines():
    		if not ilauf==0:
    			l = line.split(',')
    			data.append(l)
    		ilauf+=1
    	return data

    def __generate_gaussian_window(self, Number_of_Points, Standard_Deviation):
        window=signal.gaussian(Number_of_Points,std=Standard_Deviation)
        window=window/sum(window)
        # print "%d Gaussian Distribution Coefficients with %d Standard Deviation Has Generated"%(Number_of_Points,Standard_Deviation)
        return window

    def __normalise(self):
        norm_g = []
        window = self.__generate_gaussian_window(self.N_Points, self.Std_Dev)
        for i in range(len(self.raw_data[0,:])):
            tmp = np.convolve(self.raw_data[:,i], window)
            norm_g.append(list(tmp))
        norm_g = np.array(norm_g)
        n_tmp = np.zeros((len(norm_g[0,:]), len(norm_g[:,0])))
        for i in range(len(norm_g[:,0])):
            n_tmp[:,i] = norm_g[i,:]
        self.processed_data = n_tmp

    def __PrincipleComponentAnalysis(self):
        pca = PCA(0.95)
        pca.fit(self.processed_data)
        pca_score = pca.explained_variance_ratio_
        self.pca_components = pca.components_
        self.pca_data = pca.transform(self.processed_data)


    def __process_data(self):
        f_in = open(self.path_to_data)
        for line in f_in:
            line = (line.split('\r\n'))[0]
            columns = line.split(',')
            line_is_okay = True
            i=2
            while line_is_okay and i<len(columns):
                if columns[i] == '-1' or columns[i] == 'none':
                    line_is_okay=False
                i+=1
            if line_is_okay:
                for j in range(2,len(columns)):
                    if float(columns[j]) > cut_value:
                        columns[j] = str(cut_value)
                self.raw_data.append(columns[2:])
        f_in.close()
        self.raw_data = np.array(self.raw_data).astype(float)
        self.__normalise()

    def determine_n_cl(self):
        hist = np.histogramdd(pca_data, int(cut_value))




    def pr1nt(self):
        print self.path_to_data
        print self.raw_data
        print self.processed_data
        print self.pca_data
