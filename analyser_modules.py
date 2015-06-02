from scipy import signal
import ConfigParser
import numpy as np
import MySQLdb
import sklearn.cluster
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
#-----------------------------------------------------------------------------------
def fetch_data(dbname,tablename,username,password,column_name_list):
    db = MySQLdb.connect("localhost",username,password,dbname)
    cursor = db.cursor()
    data_dict={}
    for column_name in column_name_list:
        command="select %s from %s order by id asc;"%(column_name,tablename)
        cursor.execute(command)
        column = cursor.fetchall()
        data_dict[column_name]=[]
        for column_item in column:
            data_dict[column_name].append(str(column_item[0]))
    cursor.close()
    db.close()
    tmp_column_name=column_name_list[0]
    i=0
    n=len(data_dict[tmp_column_name])
    analysis_data_list=[]
    while i<n:
        line=""
        for key in data_dict.keys():
            line+=str(data_dict[key][i])+","
        line=line[:-1]
        if "none" not in line and "NULL" not in line:
            analysis_data_list.append(line)
        else:
            pass
        i+=1
    return analysis_data_list

def put_columns_together(source_data,output_file):
    data_dict={}
    data_dict=source_data
    data_dict_keys=[]
    data_dict_keys=data_dict.keys()
    list_of_data_lists=[]
    head_line=",".join(data_dict_keys)
    tmp_key=data_dict_keys[0]
    i=0
    n=len(data_dict[tmp_key])
    f=open(output_file,'w')
    f.write(head_line+"\n")
    list_of_data_lists.append(head_line.split(","))
    while i<n:
        line=""
        for key in data_dict_keys:
            line+=data_dict[key][i]+","
        f.write(line[:-1]+'\n')
        list_of_data_lists.append(line[:-1].split(","))
        i+=1
    f.close()    
    return list_of_data_lists    

def do_cumulative_data_cluster_analysis(all_data_dictionary):
    '''
    shualeduri procedura - dagluveba Gaussit
    1. unda daabrunos clusteris kodi, 1,2 an 3 monacemebis bolo xazistvis!
    2. unda daabrunos mteli monacemebistvis clusterebis kodis listi
    3. unda daabrunos kumulaciuri (jamuri) pingebis listi
    4. 
    '''
    #This is data smoothing which seems not to be required so far
    #window = signal.gaussian(80, std=16)
    ##std is calculated from the formula std=N/(2*alpha) where N is the size of the window i.e. 80, and the default value for alpha is 2.5
    #data_dict_keys=all_data_dictionary.keys()
    #smoothed_all_data_dictionary={}
    #for key in data_dict_keys:
    #    smoothed_all_data_dictionary[key]=[]
    #    tmp_array=np.asarray(all_data_dictionary[key])
    #    tmp_list=np.convolve(tmp_array,window,'same').tolist()
    #    smoothed_all_data_dictionary[key]=tmp_list
    #put_columns_together(smoothed_all_data_dictionary,"smoothed_se_ping_data.csv")
    #print all_data_dictionary
    init_cluster_codes_dict={}
    cluster_code_mapping_dict={}
    data_dict_keys=all_data_dictionary.keys()
    i=0
    n=len(all_data_dictionary[data_dict_keys[0]])
    all_data_list=[]
    while i<n:
        tmp_list=[]
        for key in data_dict_keys:
            tmp_list.append(all_data_dictionary[key][i])
        if "none" not in tmp_list:
            all_data_list.append(tmp_list)
        else:
            pass
        i+=1
    all_data_array=np.array(all_data_list)
    n_of_cluster_centers=3
    model=sklearn.cluster.k_means(all_data_array, n_of_cluster_centers)
    #print model
    #print model[0][0],sum(model[0][0]),'\n',model[0][1],sum(model[0][1]),'\n',model[0][2],sum(model[0][2])        
    current_data_list=[]
    for key in data_dict_keys:
        current_data_list.append(all_data_dictionary[key][n-1])
    if "none" in current_data_list:
        return "clusternone",0,0,0
    else:
        #print model[1]
        #print model[1][-1]
        j=0
        while j<n_of_cluster_centers:
            init_cluster_codes_dict[j]=sum(model[0][j])
            j+=1
        #print init_cluster_codes_dict
        max_value=init_cluster_codes_dict[0]
        max_code=0
        for key in init_cluster_codes_dict.keys():
            if init_cluster_codes_dict[key]>max_value:
                max_value=init_cluster_codes_dict[key]
                max_code=key
            else:
                continue
        cluster_code_mapping_dict[max_code]="cluster2"
        min_value=init_cluster_codes_dict[0]
        min_code=0
        for key in init_cluster_codes_dict.keys():
            if init_cluster_codes_dict[key]<min_value:
                min_value=init_cluster_codes_dict[key]
                min_code=key
            else:
                continue
        cluster_code_mapping_dict[min_code]="cluster0"    
        for key in init_cluster_codes_dict.keys():
            if key!=max_code and key!=min_code:
                mid_code=key
            else:
                continue
        cluster_code_mapping_dict[mid_code]="cluster1"
    #print cluster_code_mapping_dict    
    return cluster_code_mapping_dict,model[1],all_data_list,cluster_code_mapping_dict[model[1][-1]]

def do_single_datacolumn_cluster_analysis(single_data_dictionary):
    '''
    shualeduri procedura - dagluveba gausit
    unda daaspiralos monacemebi II gradienti, I gradienti da tviton monacemi
    unda daabrunos bolo monacembis clusteris kodi
    unda daabrunos mteli monacemebis siistvis clusterebis kodebis sia
    '''
    return 0

def cumulative_plot_generator(data_list,cluster_code_mapping_dict,cluster_codes):
    cumulative_data_list=[]
    mapped_cluster_codes_for_plotting=[]
    m=float(len(data_list[0].split(",")))
    ##data_list=data_list[-1001:-1]
    ##cluster_codes=cluster_codes.tolist()[-1001:-1]
    ##cluster_codes=np.array(cluster_codes)
    ###num_of_pc_s=2
    ###data_list=reduce_data_dimension(data_list,num_of_pc_s)
    ###x_=[]
    ###y_=[]
    ###for data_list_item in data_list:
    ###    x_.append(float(data_list_item[0]))
    ###    y_.append(float(data_list_item[1]))
    ###x_array=np.array(x_)
    ###y_array=np.array(y_)
    #data_array=np.array(data_list)
    for data_line in data_list:
        summ=0.0
        for data_line_itm in data_line.split(","):
            summ+=float(data_line_itm)
        cumulative_data_list.append(summ/m)
    #print cumulative_data_list, len(data_list), len(cumulative_data_list)    
    cumulative_data_array=np.array(cumulative_data_list)
    for cluster_code in cluster_codes:
        mapped_cluster_codes_for_plotting.append(int(cluster_code_mapping_dict[cluster_code][-1]))
    mapped_cluster_codes_array=np.array(mapped_cluster_codes_for_plotting)
    x=np.array(range(0,len(cumulative_data_array)))
    #print x,'\n',cumulative_data_array,'\n',mapped_cluster_codes_array,'\n',len(cumulative_data_array),len(mapped_cluster_codes_array)
    colormap=np.array(['g','y','r'])
    ##plt.plot(x,cumulative_data_array,'b-')
    ###plt.plot(x_array,y_array,'b-')
    #plt.scatter(x,cumulative_data_array, s=5, c=colormap[mapped_cluster_codes_array])
    fig=plt.figure(figsize=(24,18))
    plt.scatter(x,cumulative_data_array, alpha=1, c=colormap[mapped_cluster_codes_array])
    ###plt.scatter(x_array,y_array, c=colormap[mapped_cluster_codes_array])
    #plt.scatter(x[0:30],cumulative_data_array[-31:-1], c=colormap[mapped_cluster_codes_array[-31:-1]])
    plt.axis([min(x), max(x)+100, min(cumulative_data_array),max(cumulative_data_array)+100],rotation=45)
    plt.ylabel('Ping msc.')
    plt.xlabel('Time Series 2 min. interval')
    plt.savefig("cumulativeplot_last1000points.png",dpi=500)
    plt.close()
    return 0

def check_last_db_entry(db_name,username,password,tablename,column_name_list):
    exit_code=1
    db = MySQLdb.connect("localhost",username,password,db_name)
    cursor = db.cursor()
    data_dict={}
    for column_name in column_name_list:
        command="SELECT %s FROM %s order by id desc limit 1;"%(column_name,tablename)
        cursor.execute(command)
        service_ping_value = cursor.fetchall()
        data_dict[column_name]=service_ping_value[0][0]
    cursor.close()
    db.close()
    for key in data_dict.keys():
        if "none" in str(data_dict[key]) or "NULL" in str(data_dict[key]) or "-1" in str(data_dict[key]):
            exit_code=0
        else:
            continue
    return exit_code,data_dict

def get_optimal_number_of_PCA_components(data_for_analysis):
    list_for_analysis=[]
    for line in data_for_analysis:
        tmp_list=[]
        for item in line.split(","):
            tmp_list.append(float(item))
        list_for_analysis.append(tmp_list)
    analysis_data_array=np.array(list_for_analysis)
    pca = PCA(n_components='mle')
    pca.fit(analysis_data_array)
    return np.array(output)

def reduce_data_dimension(data_for_analysis,num_of_components):
    list_for_analysis=[]
    for line in data_for_analysis:
        tmp_list=[]
        for item in line.split(","):
            tmp_list.append(float(item))
        list_for_analysis.append(tmp_list)
    analysis_data_array=np.array(list_for_analysis)
    pca=PCA(n_components=num_of_components)
    pca.fit(analysis_data_array)
    data_with_reduced_dimmension=pca.components_
    output=[]
    i=0
    n=len(data_with_reduced_dimmension[0])
    while i<n:
        tmp_list=[]
        j=0
        m=len(data_with_reduced_dimmension)
        while j<m:
            tmp_list.append(float(data_with_reduced_dimmension[j][i]))
            j+=1
        output.append(tmp_list)    
        i+=1
    return output

def get_data_for_clustering(data_for_analysis):
    list_for_analysis=[]
    for line in data_for_analysis:
        tmp_list=[]
        for item in line.split(","):
            tmp_list.append(float(item))
        list_for_analysis.append(tmp_list)
    analysis_data_array=np.array(list_for_analysis)
    return analysis_data_array

def get_cluster_code(input_data,n_of_cluster_centers):
    model=sklearn.cluster.k_means(input_data, int(n_of_cluster_centers))
    init_cluster_codes_dict={}
    cluster_code_mapping_dict={}
    j=0
    while j < int(n_of_cluster_centers):
        #init_cluster_codes_dict[j]=sum(model[0][j]) #This is option to compare values of cluster centers
        init_cluster_codes_dict[j]=np.sum((model[0][j])**2)
        j+=1
    max_value=init_cluster_codes_dict[0]
    max_code=0
    for key in init_cluster_codes_dict.keys():
        if init_cluster_codes_dict[key]>max_value:
            max_value=init_cluster_codes_dict[key]
            max_code=key
        else:
            continue
    cluster_code_mapping_dict[max_code]="cluster2"
    min_value=init_cluster_codes_dict[0]
    min_code=0
    for key in init_cluster_codes_dict.keys():
        if init_cluster_codes_dict[key]<min_value:
            min_value=init_cluster_codes_dict[key]
            min_code=key
        else:
            continue
    cluster_code_mapping_dict[min_code]="cluster0"
    for key in init_cluster_codes_dict.keys():
        if key!=max_code and key!=min_code:
            mid_code=key
        else:
            continue
    cluster_code_mapping_dict[mid_code]="cluster1"
    #print model
    #print model[1]
    #print cluster_code_mapping_dict,cluster_code_mapping_dict[model[1][-1]]
    np.savetxt("foo.csv", input_data, delimiter=",")
    return int(cluster_code_mapping_dict[model[1][-1]][-1]),model[1],cluster_code_mapping_dict

