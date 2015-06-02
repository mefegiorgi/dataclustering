from modules import content_parser,srt_extractor, db_check_on_updates,db_insert
from bs4 import BeautifulSoup
import ConfigParser

##Reading of the basic configuration information
config = ConfigParser.ConfigParser()

try:
    config.read("/storage/service_status_identifier/config.cfg")
except IOError:
    print "file /storage/scripts/config.cfg not available please check if it exists"

source_address=config.get('main','cell_info_source')
html_source_code=content_parser(source_address)
soup = BeautifulSoup(html_source_code)

cell_service_name_list=config.get('main','cell_service_name').split(",")
srt_dict={}
srt_dict=srt_extractor(cell_service_name_list,soup.tbody)

db_name=config.get('dbconfig','db_name')
table_name=config.get('dbconfig','table_name')
username=config.get('dbconfig','username')
password=config.get('dbconfig','password')

#This function should be used to check if all cell services listed in the configuration file have the corresponding columns in the database
updates_number,db_cell_service_name_list=db_check_on_updates(db_name,table_name,username,password,cell_service_name_list)
if updates_number==0:
    print "THE DATABASE %s, TABLE %s, IS UP TO DATE"%(db_name,table_name)
else:
    print updates_number," COLUMNS HAS BEEN ADD TO THE DATABASE %s, TABLE %s"%(db_name,table_name)
#This is function to insert data in the database
db_insert(db_name, table_name, username, password, srt_dict, db_cell_service_name_list)


