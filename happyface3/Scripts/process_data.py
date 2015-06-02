import numpy as np
from bs4 import BeautifulSoup
import urllib
import time

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

def get_data(html):
	soup = BeautifulSoup(html)
	soup.prettify()
	ping_data = {}
	for row in soup.find_all('tr'):
		cell_name=''
		for col in row.find_all('td'):
			print col.get('class')
			if col.get('class') == ['cell']:
				cell_name = col.get_text()
			if cell_name != '' and col.get('class')==['ping']:
				ping_data[cell_name]=float(col.get_text().replace('msec', ''))

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


url = 'http://10.255.1.13:2288/cellInfo'
service_name_list = 'DCap-se5-goegrid,DCap-se7-goegrid,DCap-se8-goegrid,DCap-se9-goegrid,DCap-se10-goegrid,DCap-se11-goegrid,DCap-se12-goegrid,DCap-se13-goegrid,DCap-se14-goegrid,DCap-se15,DCap-se16-goegrid,GFTP-se-goegrid,LoginBroker,PnfsManager,PoolManager,SRM-se-goegrid,WebDAV-se-goegrid,Xrootd-se5-goegrid,gPlazma,srm-LoginBroker,pool-dteam2,pool-k5-1-data,pool-o9-1-cache,pool-o9-1-data,pool-o9-10-data-ops,pool-o9-2-cache,pool-o9-2-data,pool-o9-3-cache,pool-o9-3-data,pool-o9-4-cache,pool-o9-4-data,pool-o9-5-cache,pool-o9-5-data,pool-o9-6-cache,pool-o9-6-data,pool-p1-1-cache,pool-p1-1-data,pool-p1-2-cache,pool-p1-2-data,pool-p1-3-cache,pool-p1-3-data,pool-p1-5-data,pool-p1-6-data,pool-p1-7-data,pool-p2-1-cache,pool-p2-1-data,pool-p2-2-cache,pool-p2-2-data,pool-p2-3-cache,pool-p2-3-data,pool-p2-4-cache,pool-p2-4-data,pool-p5-1-cache,pool-p5-1-data,pool-p5-1-data-ops,pool-p5-10-cache,pool-p5-10-data,pool-p5-2-cache,pool-p5-2-data,pool-p5-3-cache,pool-p5-3-data,pool-p5-4-cache,pool-p5-4-data,pool-p5-5-cache,pool-p5-5-data,pool-p5-6-cache,pool-p5-6-data,pool-p5-7-cache,pool-p5-7-data,pool-p5-8-cache,pool-p5-8-data,pool-p5-9-cache,pool-p5-9-data,pool-p6-1-cache,pool-p6-1-data,pool-p6-10-cache,pool-p6-10-data,pool-p6-11-cache,pool-p6-11-data,pool-p6-12-cache,pool-p6-12-data,pool-p6-13-cache,pool-p6-13-data,pool-p6-14-cache,pool-p6-14-data,pool-p6-15-cache,pool-p6-15-data,pool-p6-16-cache,pool-p6-16-data,pool-p6-2-cache,pool-p6-2-data,pool-p6-3-cache,pool-p6-3-data,pool-p6-4-cache,pool-p6-4-data,pool-p6-5-cache,pool-p6-5-data,pool-p6-6-cache,pool-p6-6-data,pool-p6-7-cache,pool-p6-7-data,pool-p6-8-cache,pool-p6-8-data,pool-p6-9-cache,pool-p6-9-data,pool-p7-1-cache,pool-p7-1-data,pool-p7-10-cache,pool-p7-10-data,pool-p7-11-cache,pool-p7-11-data,pool-p7-12-cache,pool-p7-12-data,pool-p7-13-cache,pool-p7-13-data,pool-p7-14-cache,pool-p7-14-data,pool-p7-15-cache,pool-p7-15-data,pool-p7-16-cache,pool-p7-16-data,pool-p7-2-cache,pool-p7-2-data,pool-p7-3-cache,pool-p7-3-data,pool-p7-4-cache,pool-p7-4-data,pool-p7-5-cache,pool-p7-5-data,pool-p7-6-cache,pool-p7-6-data,pool-p7-7-cache,pool-p7-7-data,pool-p7-8-cache,pool-p7-8-data,pool-p7-9-cache,pool-p7-9-data,se2-goegrid_2,se2-goegrid_3,se2-goegrid_6,se2-goegrid_7'.split(",")

html = content_parser(url)
soup = BeautifulSoup(html)
ping_dict = srt_extractor(service_name_list, soup.tbody)

#print ping_dict
with open('/var/lib/HappyFace3/Scripts/pingdata.csv', 'r') as fin:
    data = fin.read().splitlines(True)
with open('/var/lib/HappyFace3/Scripts/pingdata.csv', 'w') as fout:
    fout.writelines(data[1:])

f_out = open('/var/lib/HappyFace3/Scripts/pingdata.csv','a')
line = '42,'
line = line + str(time.localtime()[0]) +'-'+ str(time.localtime()[1])+'-'+str(time.localtime()[2])+' '+str(time.localtime()[3])+':'+str(time.localtime()[4])+':'+str(time.localtime()[5])+','
for key in ping_dict:
	line = line+ str(ping_dict[key]) + ',' 
line = line[:-1]
line = line +'\n'
f_out.write(line)
f_out.close()

