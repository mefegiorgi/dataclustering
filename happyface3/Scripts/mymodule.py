# Copyright YEAR Institute - Institution
 # Author: Your Name (your e-mail address)
 #
 #   Licensed under the Apache License, Version 2.0 (the "License");
 #   you may not use this file except in compliance with the License.
 #   You may obtain a copy of the License at
 #
 #       http://www.apache.org/licenses/LICENSE-2.0
 #
 #   Unless required by applicable law or agreed to in writing, software
 #   distributed under the License is distributed on an "AS IS" BASIS,
 #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 #   See the License for the specific language governing permissions and
 #   limitations under the License.


import hf
from sqlalchemy import *


class mymodule(hf.module.ModuleBase):
  config_keys = {
  'key': ('Path to Pingdata', '/var/lib/HappyFace3/Scripts/cluster_log.csv')
  }

  config_hint = 'Give a config hint here.'
  table_columns = [
  Column('time_stamp', TEXT),
  Column('datetime', INT),
  Column('cluster_code', INT),
  Column('total_number', INT)
  ], []

  subtable_columns = {
  'subtable_name':([
  Column('Time Stamp',TEXT),
  Column('year', INT),
  Column('month',INT),
  Column('day',INT),
  Column('hour',INT),
  Column('minute',INT),
  Column('second',INT), 
  Column('Cluster Code',TEXT),
  Column('Total Number of Clusters', INT),
  Column('Distance',FLOAT)
  ], [])}
  
  

  def prepareAcquisition(self):
    #url = self.config['key']
    #self.source = hf.downloadService.addDownload(url)
    self.subtable_name_db_value_list = []

  def extractData(self):
    data = {'time_stamp':'HH.MM.SS DD/MM/YY', 
    'Cluster Code': 0,
    'Total Number of Clusters': 0,
    'datetime':0
    }
   
    f_in = open(self.config_keys['key'][1])
    subdata = []
    for line in f_in.readlines():
      tmp = line.split(',')
      ttime=[]
      time_cut = tmp[0].split(' ')
      date = time_cut[0].split('-')
      time = time_cut[1].split(':')
      ttime = [int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2])]
      subdata.append({'Time Stamp':tmp[0], 'year':ttime[0], 'month':ttime[1],'day':ttime[2],'hour':ttime[3],'minute':ttime[4],'second':ttime[5], 'Cluster Code':tmp[1], 'Total Number of Clusters':int(tmp[2]), 'Distance':float(tmp[3])})
    
    self.subtable_name_db_value_list = subdata
    '''
    self.subtable_name_db_value_list = [
    {'Time Stamp':'14.11.1992', 
    'Cluster Code':3,
    'Total Number of Clusters': 4
    },
    {'Time Stamp':'14.11.1992', 
    'Cluster Code':2,
    'Total Number of Clusters': 4
    }]
    ''' 
    return data

  def fillSubtables(self, parent_id):
    self.subtables['subtable_name'].insert().execute([dict(parent_id=parent_id, **row) for row in self.subtable_name_db_value_list])

  def getTemplateData(self):
    data = hf.module.ModuleBase.getTemplateData(self)
    details = self.subtables['subtable_name'].select().where(self.subtables['subtable_name'].c.parent_id==self.dataset['id']).execute().fetchall()
    data['details'] = map(dict, details)
    return data



