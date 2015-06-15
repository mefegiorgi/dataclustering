from bs4 import BeautifulSoup
import urllib
from time import localtime
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/var/lib/HappyFace3/Scripts/scrape_config.cfg')

outname = config.get('main','output_name')
url = config.get('main', 'source_url')
service_list = config.get('main','service_list')
service_list = service_list.split('/')[:-1]

html_source = urllib.urlopen(url).read()
soup = BeautifulSoup(html_source)
soup = soup.find_all('tbody')[0]
rows = soup.find_all('tr')

srt_dict = {}

act_list = []

for row in rows:
    columns = row.find_all('td')
    service_name = columns[0].get_text()
    if service_name in service_list:
	act_list.append(str(columns[0].get_text()))
	srt = columns[4].get_text()
	try:
		srt = float(srt)
	except:
		srt = -1
		print service_name
		print 'SRT format error'
	srt_dict[service_name]=srt

missing_list=[]
for s in service_list:
    is_missing = True
    for t in act_list:
        if s == t:
	    is_missing = False
    if is_missing:
	missing_list.append(s)
	print s
	srt_dict[s]=-1

msg_lst = ''
for s in missing_list:
	msg_lst = msg_lst+s+'/'
msg_lst=msg_lst[:-1]


if sum(1 for line in open(outname)) > 100000:
    data=[]
    with open(outname, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outname, 'w') as fout:
        fout.writelines(data[1:])

f_out = open(outname,'a')
time_stamp = str(localtime()[0])+'-'+str(localtime()[1])+'-'+str(localtime()[2])+' '+str(localtime()[3])+':'+str(localtime()[4])+':'+str(localtime()[5])

srt_line = ''
for key in service_list:
    srt_line = srt_line +str(srt_dict[key])+ ','
srt_line = srt_line[:-1]
f_out.write('0'+','+time_stamp+','+srt_line+','+msg_lst+'\n')
f_out.close()
