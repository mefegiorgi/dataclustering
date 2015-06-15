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
import random
from sklearn import cross_validation
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import scipy.signal as signal
from sklearn.decomposition import PCA
import ConfigParser

class StatusIdentification:
    config = ConfigParser.ConfigParser()

    filename = ''
    service_list = []
    raw_data = []
    processed_data = []
    pca_components = []
    pca_data = []
    pca_model = []
    sample = []
    K = 0
    cluster_centers = []
    
#--------------------------------------------------------------
# FUNCTIONS
#--------------------------------------------------------------

    def __init__(self, arr, confname):
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
	try:
          self.config.read(confname)
	except IOError:
          print "file config.cfg not available please check if it exists"
	self.N_Points = int(self.config.get('normalisation', 'window_size'))
	self.Std_Dev = float(self.config.get('normalisation', 'standard_deviation'))
	self.cut_value = float(self.config.get('main', 'cut_value'))
	self.sample_size = int(self.config.get('main', 'sample_size'))
	self.conf_interval = float(self.config.get('main', 'confidence_interval'))
	self.display_size = int(self.config.get('main', 'display_size'))
	self.service_list = (self.config.get('main','service_list')).split('/')[:-1]
	
        if type(arr) is str:
            self.filename = arr
        else:
	    print 'Input Format error'
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
        for i in range(len(self.processed_data[0,:])):
            tmp = np.convolve(self.processed_data[:,i].astype(float), window)
            norm_g.append(list(tmp))
        norm_g = np.array(norm_g)
        n_tmp = np.zeros((len(norm_g[0,:]), len(norm_g[:,0])))
        for i in range(len(norm_g[:,0])):
            n_tmp[:,i] = norm_g[i,:]
        n_tmp = n_tmp[14:-15,:]
        self.processed_data = n_tmp
        '''n_tmp = n_tmp.astype(str)
        n_tmp2 = []
        for i in range(len(n_tmp)):
            n_tmp2.append(np.insert(n_tmp[i,:], 0, str(self.raw_data[i,0])))
        n_tmp2 = np.array(n_tmp2)
        self.processed_data = n_tmp2'''

    def __PrincipleComponentAnalysis(self):
        '''
        Principle Component Analysis is used to reduce the number of features
        of the data. The principle components with a cumulative variance of
        more than 95 percent are chosen to represent the data.
        '''
        pca = PCA(0.95)
        pca.fit(self.processed_data[:,:].astype(float))
        pca_score = pca.explained_variance_ratio_
        self.pca_model = pca
        self.pca_components = pca.components_
        self.pca_data = np.array(pca.transform(self.processed_data[:,:].astype(float)))

    def __process_data(self):
        '''
        At first the data is processed in a way that invalid SRT-vectors are
        depreciated and values exceeding 500 ms are set to 500 ms.

        This is done here a) while reading the data from a CSV file
        or b) while processing an already existing array.
        '''
        
	f_in = open(self.filename)
	processed_data=[]
        for line in f_in:
	    line_is_okay = True
            line = (line.split('\n'))[0]
            columns = line.split(',')
	    missing_services = columns[-1]
	    columns = columns[:-1]
            while len(columns) < len(self.service_list):
		columns.append('-1')
                line_is_okay=False
            i=2
            while line_is_okay and i<len(columns):
                if columns[i] == '-1' or columns[i] == 'none':
                    line_is_okay=False
                i+=1
            for j in range(2,len(columns)):
                if float(columns[j]) > self.cut_value:
                    columns[j] = str(self.cut_value)
	    raw_col = columns[1:]
	    raw_col.append(missing_services)
            self.raw_data.append(raw_col)
            if line_is_okay:
                processed_data.append(columns[2:])
        f_in.close()
        self.processed_data = np.array(processed_data,dtype='float')
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

        for i in range(min([self.sample_size,len(self.pca_data)])):
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
        for i in range(min([self.display_size, len(self.pca_data)])):
            mini = 10e30
            label = 0
            isokay = True
            for col in self.raw_data[-i-1,:-1]:
                if col == -1 or col == '-1' or col=='none':
                    label = 'no response'
                    isokay = False
            if isokay:
                for j,c in enumerate(self.cluster_centers):
                    X = self.raw_data[-i-1,1:-1].astype(float)
                    X =  self.pca_model.transform(X)
                    dist = c-X
                    if np.dot(dist,dist.T) < mini:
                        mini = np.dot(dist,dist.T)
                        label = j
            time_stamp = self.raw_data[-i-1, 0]
            n_cl = self.K
            d_from_0 = -1
	    missing_services = ''
            if isokay:
		X = self.raw_data[-i-1,1:-1].astype(float)
                d_from_0 = np.sqrt(np.dot(X,X.T))
            else :
	        d_from_0=-1
		missing_services = self.raw_data[-i-1,-1]
	    analysis.append([time_stamp, label, n_cl, d_from_0, missing_services])
        return analysis
