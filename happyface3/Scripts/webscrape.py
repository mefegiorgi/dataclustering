from bs4 import BeautifulSoup
import urllib
from time import localtime

outname = '/var/lib/HappyFace3/Scripts/pingdata.csv'
url = 'http://se-goegrid.gwdg.de:2288/webadmin/cellinfo?1'
html_source = urllib.urlopen(url).read()
soup = BeautifulSoup(html_source)
soup = soup.find_all('tbody')[0]
rows = soup.find_all('tr')

srt_dict = {}

for row in rows:
    columns = row.find_all('td')
    service_name = columns[0].get_text().replace('-','').replace('_','')

    srt = columns[4].get_text()
    try:
        srt = float(srt)
    except:
        srt = -1
        print 'SRT format error'
    srt_dict[service_name]=srt

if sum(1 for line in open(outname)) > 100000:
    data=[]
    with open(outname, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outname, 'w') as fout:
        fout.writelines(data[1:])

f_out = open(outname,'a')
time_stamp = str(localtime()[0])+'-'+str(localtime()[1])+'-'+str(localtime()[2])+' '+str(localtime()[3])+':'+str(localtime()[4])+':'+str(localtime()[5])

srt_line = ''
for key in srt_dict.keys():
    srt_line = srt_line +str(srt_dict[key])+ ','
srt_line = srt_line[:-1]
f_out.write('0'+','+time_stamp+','+srt_line+'\n')
f_out.close()
