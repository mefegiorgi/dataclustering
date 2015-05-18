#------------------------------------------------------------
# COMPOSITE SERVICE STATUS IDENTIFICATION TOOL V.0.1
#
#
#
#
#
#
# Author: Philip Marszal
# Date: 15.05.15
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
    filename = ''
    raw_data = []
    processed_data = []
    pca_components = []
    pca_data = []
    sample = []
    K = 0
    cluster_centers = []
    N_Points = 30
    Std_Dev = 5
    cut_value = 500
    sample_size = 5000
    conf_interval = 0.8


#--------------------------------------------------------------
# FUNCTIONS
#--------------------------------------------------------------

    def __init__(self, arr):
        if type(arr) is str:
            self.filename = arr
        elif type(arr) is numpy.ndarray:
            self.raw_data = arr
        elif type(arr) is list:
            self.raw_data = np.array(arr)

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
        self.pca_data = np.array(pca.transform(self.processed_data))


    def __process_data(self):
        if self.filename != '':
            f_in = open(self.filename)
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
                        if float(columns[j]) > self.cut_value:
                            columns[j] = str(self.cut_value)
                    self.raw_data.append(columns[2:])
            f_in.close()
        else:
            for i in range(len(self.raw_data[:,0])):
                for j in range(len(self.raw_data[0,:])):
                    if self.raw_data[i,j] > self.cut_value:
                        self.raw_data[i,j] = self.cut_value
        self.raw_data = np.array(self.raw_data).astype(float)
        self.__normalise()
        self.__PrincipleComponentAnalysis()

    def determine_n_cl(self):

        #-----------------------------------------------------------------
        # SAMPLING
        # r_projected_data = np.sqrt(np.sum(self.pca_data**2, axis = 1))
        # bins = []
        # for i in range(int(self.cut_value)):
        #     bins.append([])
        # max = r_projected_data.max()
        # r_bins = float(max/int(self.cut_value)) * np.arange(0,int(self.cut_value))
        # for i in range(self.cut_value):
        #     for j in range(len(r_projected_data)):
        #         if (r_projected_data[j] >= r_bins[i]) and (r_projected_data[j] < r_bins[i]+float(max/int(self.cut_value))):
        #             bins[i].append(self.pca_data[j,:])
        # bins = np.array(bins)
        # for b in bins:
        #     for i in range(int(float(len(b))/len(self.pca_data)*self.sample_size)):
        #         self.sample.append(random.choice(b))
        index_list = []
        index_list_pre= range(len(self.pca_data))
        random.shuffle(index_list_pre)

        for i in range(self.sample_size):
            index_list.append(index_list_pre[i])

        self.sample = self.pca_data[index_list]
        #------------------------------------------------------------------
        k = len(self.pca_components)
        sil = 0
        print len(self.sample)
        while sil<self.conf_interval and k >=2:
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(self.sample)
            # print kmeans.cluster_centers_
            sil = (silhouette_samples(self.sample,kmeans.labels_)).mean(axis = 0)
            k = k-1
            print k+1, sil
        # print k+1, sil





    def pr1nt(self):
        print self.path_to_data
        print self.raw_data
        print self.processed_data
        print self.pca_data
