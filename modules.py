import urllib
import socket
import MySQLdb
from MySQLdb import *

def content_parser(source_url):
    html_source_code=""
    try:
        f = urllib.urlopen(source_url)
    except urllib2.URLError:
        pass
        return 2
    else:
        html_source_code = f.read()
    return html_source_code

def srt_extractor(cell_service_name_list,html_source):
    srt_dict={}
    cell_service_name_dict_list=[]
    for cell_service_name in cell_service_name_list:
        if "_" in cell_service_name and "-" in cell_service_name:
            cell_service_dict_name =cell_service_name.replace("_",'')
            cell_service_dict_name=cell_service_dict_name.replace("-",'')
            srt_dict[cell_service_dict_name]=-1
        elif "_" in cell_service_name and "-" not in cell_service_name:
            cell_service_dict_name=cell_service_name.replace("_",'')
            srt_dict[cell_service_dict_name]=-1
        elif "-" in cell_service_name and "_" not in cell_service_name:
            cell_service_dict_name=cell_service_name.replace("-",'')
            srt_dict[cell_service_dict_name]=-1
        else:
            srt_dict[cell_service_name]=-1
            pass
    for line in html_source:
        if len(line)>1:
            srt_string=""
            srt_value=0.0
            for cell_service_name in cell_service_name_list:
                if cell_service_name in str(line) and "OFFLINE" not in str(line):
                    tmp_cell_service_name=""
                    if "_" in cell_service_name and "-" in cell_service_name:
                        tmp_cell_service_name=cell_service_name.replace("_",'')
                        tmp_cell_service_name=tmp_cell_service_name.replace("-",'')
                        srt_string=str(line).split("</td>")[4]
                        srt_dict[tmp_cell_service_name]=float(srt_string[srt_string.index('>')+1:len(srt_string)-5])
                        #print "srt_extractor -- and --> ",tmp_cell_service_name
                    elif "_" in cell_service_name and "-" not in cell_service_name:
                        tmp_cell_service_name=cell_service_name.replace("_",'')
                        srt_string=str(line).split("</td>")[4]
                        srt_dict[tmp_cell_service_name]=float(srt_string[srt_string.index('>')+1:len(srt_string)-5])
                        #print "srt_extractor -- _ in and - not in --> ",tmp_cell_service_name
                    elif "-" in cell_service_name and "_" not in cell_service_name:
                        tmp_cell_service_name=cell_service_name.replace("-",'')
                        srt_string=str(line).split("</td>")[4]
                        srt_dict[tmp_cell_service_name]=float(srt_string[srt_string.index('>')+1:len(srt_string)-5])
                        #print "srt_extractor -- - in and _ not in --> ",tmp_cell_service_name
                    else:
                        srt_string=str(line).split("</td>")[4]
                        srt_dict[cell_service_name]=float(srt_string[srt_string.index('>')+1:len(srt_string)-5])
                        #print "srt_extractor -- else --> ",cell_service_name
                        continue
                else:
                    continue
        else:
            continue
    #print srt_dict    
    return srt_dict

def db_check_on_updates(db_name,table_name,username,password,cell_service_name_list):
    update=0
    db=MySQLdb.connect("localhost",username,password,db_name)
    cursor=db.cursor()
    sql_command = "SELECT column_name FROM information_schema.columns WHERE table_name='%s';"%table_name
    cursor.execute(sql_command)
    alist = cursor.fetchall()
    column_names=tuple(i[0] for i in alist)[1:]
    #print column_names
    db_cell_service_name_list=[]
    for cell_service_name in cell_service_name_list:
        #tmp_cell_service_name=cell_service_name.replace("-","_")
        tmp_cell_service_name=""
        if "_" in cell_service_name and "-" in cell_service_name:
            tmp_cell_service_name=cell_service_name.replace("_",'')
            tmp_cell_service_name=tmp_cell_service_name.replace("-",'')
            db_cell_service_name_list.append(tmp_cell_service_name)
            #print "db_check_on_update ------ and -------> ",tmp_cell_service_name
        elif "_" in cell_service_name and "-" not in cell_service_name:
            tmp_cell_service_name=cell_service_name.replace("_",'')
            db_cell_service_name_list.append(tmp_cell_service_name)
            #print "db_check_on_update ------ _ in and - not in -------> ",tmp_cell_service_name
        elif "-" in cell_service_name and "_" not in cell_service_name:
            tmp_cell_service_name=cell_service_name.replace("-",'')
            db_cell_service_name_list.append(tmp_cell_service_name)
            #print "db_check_on_update ------ - in and _ not in -------> ",tmp_cell_service_name
        else:
            db_cell_service_name_list.append(cell_service_name)
            #print "db_check_on_update ------ else -------> ",cell_service_name
            continue
    for db_cell_service_name in db_cell_service_name_list:
        if db_cell_service_name not in column_names:
            add_column_command="ALTER TABLE %s ADD %s VARCHAR(20) NOT NULL DEFAULT 'none';"%(table_name,db_cell_service_name)
            #print add_column_command
            cursor.execute(add_column_command)
            db.commit()
            update+=1
        else:
            continue
    db.close()    
    return update,db_cell_service_name_list

def db_insert(db_name, tablenm, username, password, data, db_cell_service_name_list):
    db = MySQLdb.connect("localhost",username,password,db_name)
    cursor = db.cursor()
    column_name_string=""
    values_string=""
    for db_cell_service_name in db_cell_service_name_list:
        column_name_string+="%s, "%(db_cell_service_name)
        values_string+="%s,"%str(data[db_cell_service_name])
    column_name_string=column_name_string[:-2]    
    values_string=values_string[:-1]
    command='''INSERT INTO %s (%s) VALUES(%s)'''%(tablenm, column_name_string, values_string)
    #print command,len(column_name_string.split(",")),len(values_string.split(","))
    cursor.execute(command)
    #Commit your changes in the database
    db.commit()
    #Disconnect from server
    db.close()
    return 0
