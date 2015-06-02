from analyser_modules import *
import ConfigParser
import MySQLdb

config = ConfigParser.ConfigParser()

try:
    config.read("/storage/service_status_identifier/config.cfg")
except IOError:
    print "file /storage/scripts/config.cfg not available please check if it exists"

cell_name_list=config.get('main','cell_service_name').split(",")
column_name_list=[]
for cell_name in cell_name_list:
    tmp_cell_name=""
    if "_" in cell_name and "-" in cell_name:
        tmp_cell_name=cell_name.replace("_",'')
        tmp_cell_name=tmp_cell_name.replace("-",'')
        column_name_list.append(tmp_cell_name)
    elif "_" in cell_name and "-" not in cell_name:
        tmp_cell_name=cell_name.replace("_",'')
        column_name_list.append(tmp_cell_name)
    elif "-" in cell_name and "_" not in cell_name:
        tmp_cell_name=cell_name.replace("-",'')
        column_name_list.append(tmp_cell_name)
    else:
        column_name_list.append(cell_name)

db_name=config.get('dbconfig','db_name')
table_name=config.get('dbconfig','table_name')
username=config.get('dbconfig','username')
password=config.get('dbconfig','password')

number_of_clusters=config.get('analysis','number_of_clusters')
num_of_components=int(config.get('analysis','optimal_n_of_dimmensions'))

#data_dict=fetch_data(db_name,table_name,username,password,column_name_list)
#output_file="se_ping_data.csv"
#se_ping_data=put_columns_together(data_dict,output_file)
#cluster_code_mapping_dict,cluster_codes,cleaned_data_list,current_cluster_code=do_cumulative_data_cluster_analysis(data_dict)

data_for_analysis=[]
last_entry_dict={}
cluster_code_mapping_dict={}
last_entry_check_code,last_entry_dict=check_last_db_entry(db_name,username,password,table_name,column_name_list)
if last_entry_check_code==1:
    data_for_analysis=fetch_data(db_name,table_name,username,password,column_name_list)
    #print data_for_analysis
    #print get_optimal_number_of_PCA_components(data_for_analysis)
    #input_data=reduce_data_dimension(data_for_analysis,num_of_components)
    input_data=get_data_for_clustering(data_for_analysis)
    cluster_code,cluster_codes_array,cluster_code_mapping_dict=get_cluster_code(input_data,number_of_clusters)
    if cluster_code==0:
        print cluster_code
        print "STATUS OK"
    elif cluster_code==1:
        print cluster_code
        print "STATUS WARNING"
    else:
        print cluster_code
        print "STATUS CRITICAL"
    if cumulative_plot_generator(data_for_analysis,cluster_code_mapping_dict,cluster_codes_array)==0:
        print "PLOT HAS BEEN GENERATED"
    else:
        print "PROBLEMS DURING PLOT GENERATION"
else:
    cluster_code=3
    output_line=""
    for key in last_entry_dict.keys():
        if "none" in str(last_entry_dict[key]) or "NULL" in str(last_entry_dict[key]) or "-1" in str(last_entry_dict[key]):
            output_line+="%s, "%str(key)
        else:
            continue
    output_line="SERVICE/S %sIS/ARE NOT AVAILABLE"%output_line    
    output_line=output_line[:-2]
    print cluster_code
    print output_line
