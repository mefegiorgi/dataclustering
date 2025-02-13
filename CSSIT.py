#------------------------------------------------------------
# COMPOSITE SERVICE STATUS IDENTIFICATION TOOL V.0.1
#
#
#
#
#
#
# Author: Philip Marszal
# Date: 29.05.15
#------------------------------------------------------------

import numpy as np
from matplotlib import pyplot as plt
import random
from sklearn import cross_validation
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import scipy.signal as signal
from sklearn.decomposition import PCA
import ConfigParser

class StatusIdentification:
    config = ConfigParser.ConfigParser()
    try:
        config.read("config.cfg")
    except IOError:
        print "file config.cfg not available please check if it exists"

    filename = ''
    raw_data = []
    processed_data = []
    pca_components = []
    pca_data = []
    sample = []
    K = 0
    cluster_centers = []
    N_Points = int(config.get('normalisation', 'window_size'))
    Std_Dev = float(config.get('normalisation', 'standard_deviation'))
    cut_value = float(config.get('main', 'cut_value'))
    sample_size = int(config.get('main', 'sample_size'))
    conf_interval = float(config.get('main', 'confidence_interval'))
    display_size = int(config.get('main', 'display_size'))


#--------------------------------------------------------------
# FUNCTIONS
#--------------------------------------------------------------

    def __init__(self, arr):
        '''
        The object is initialised with an argument. This can be
            a) The name of the file in which the SRT-vectors are written
            in the following format:

            1,YY-MM-DD HH:MM:SS,SRT Service 1(FLOAT),SRT Service 2,...
            2,YY-MM-DD HH:MM:SS,SRT Service 1(FLOAT),SRT Service 2,...
            3,YY-MM-DD HH:MM:SS,SRT Service 1(FLOAT),SRT Service 2,...

            b) An already existing numpy array or a list formated in the
            following way:

            [['YY-MM-DD HH:MM:SS' , SRT Service 1(FLOAT), SRT Service 2, ...],
            ['YY-MM-DD HH:MM:SS' , SRT Service 1(FLOAT), SRT Service 2, ...],
            ['YY-MM-DD HH:MM:SS' , SRT Service 1(FLOAT), SRT Service 2, ...],
            ...]

        '''
        if type(arr) is str:
            self.filename = arr
        elif type(arr) is numpy.ndarray:
            self.raw_data = arr
        elif type(arr) is list:
            self.raw_data = np.array(arr)
        self.__process_data()

    def __generate_gaussian_window(self, Number_of_Points, Standard_Deviation):
        '''
        This function is used for the normalisation of the data. It produces a
        Gaussian window with fixed width and standard deviation.
        '''
        window=signal.gaussian(Number_of_Points,std=Standard_Deviation)
        window=window/sum(window)
        return window

    def __normalise(self):
        '''
        The data is normalised by convolving it with a Gaussian Window of fixed
        width and standard deviation. The tails of the result are cut off.
        '''
        norm_g = []
        window = self.__generate_gaussian_window(self.N_Points, self.Std_Dev)
        for i in range(1,len(self.raw_data[0,:])):
            tmp = np.convolve(self.raw_data[:,i].astype(float), window)
            norm_g.append(list(tmp))
        norm_g = np.array(norm_g)
        n_tmp = np.zeros((len(norm_g[0,:]), len(norm_g[:,0])))
        for i in range(len(norm_g[:,0])):
            n_tmp[:,i] = norm_g[i,:]
        n_tmp = n_tmp[14:-15,:]
        n_tmp = n_tmp.astype(str)
        n_tmp2 = []
        for i in range(len(n_tmp)):
            n_tmp2.append(np.insert(n_tmp[i,:], 0, str(self.raw_data[i,0])))
        n_tmp2 = np.array(n_tmp2)
        self.processed_data = n_tmp2

    def __PrincipleComponentAnalysis(self):
        '''
        Principle Component Analysis is used to reduce the number of features
        of the data. The principle components with a cumulative variance of
        more than 95 percent are chosen to represent the data.
        '''
        pca = PCA(0.95)
        pca.fit(self.processed_data[:,1:].astype(float))
        pca_score = pca.explained_variance_ratio_
        self.pca_components = pca.components_
        self.pca_data = np.array(pca.transform(self.processed_data[:,1:].astype(float)))

    def __process_data(self):
        '''
        At first the data is processed in a way that invalid SRT-vectors are
        depreciated and values exceeding 500 ms are set to 500 ms.

        This is done here a) while reading the data from a CSV file
        or b) while processing an already existing array.
        '''
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
                    self.raw_data.append(columns[1:])
            f_in.close()
        else:
            for i in range(len(self.raw_data[:,0])):
                for j in range(len(self.raw_data[0,:])):
                    if self.raw_data[i,j] > self.cut_value:
                        self.raw_data[i,j] = self.cut_value
        self.raw_data = np.array(self.raw_data)
        self.__normalise()
        self.__PrincipleComponentAnalysis()
        self.__determine_n_cl()

    def __determine_n_cl(self):
        '''
        The number of clusters is identified by calculating the clustering
        for a sample of the data for different number of clusters. The first
        number of clusters which exceeds the defined confidence value of 0.8
        is taken to be the correct number of clusters.
        The confidence value corresponds to the mean silhouette coefficient of
        the clustering.
        '''
        #-----------------------------------------------------------------
        # SAMPLING
        index_list = []
        index_list_pre= range(len(self.pca_data))
        random.shuffle(index_list_pre)

        for i in range(self.sample_size):
            index_list.append(index_list_pre[i])

        self.sample = self.pca_data[index_list]
        #------------------------------------------------------------------
        k = len(self.pca_components)
        sil = 0
        while sil<self.conf_interval and k >=2:
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(self.sample)
            sil = (silhouette_samples(self.sample,kmeans.labels_)).mean(axis = 0)
            k = k-1
        self.K=k+1

    def clustering(self):
        '''
        For clustering the K-Means algorithm is used. The resulting clusters are
        labeled corresponding to their distance from the 0-vector. The label '0'
        corresonds to the cluster closest to the point of origin.

        This function returns the labels and time stamps of the latest 30
        SRT-vectors.
        '''
        kmeans = KMeans(n_clusters=self.K)
        kmeans.fit(self.pca_data)
        def sort_key(arr):
            return arr.dot(arr)
        self.cluster_centers = sorted(kmeans.cluster_centers_, key=sort_key)
        analysis = []
        for i in range(self.display_size):
            mini = 10e30
            label = 0
            for j,c in enumerate(self.cluster_centers):
                dist = c-self.pca_data[-i-1]
                if dist.dot(dist) < mini:
                    mini = dist.dot(dist)
                    label = j
            time_stamp = self.raw_data[-i-1, 0]
            n_cl = self.K
            analysis.append([time_stamp, label, n_cl])
        return analysis
