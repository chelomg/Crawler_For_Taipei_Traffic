import urllib
import gzip
import json
from time import gmtime, strftime
import csv
import os
section_id_list = []
youbike_stop_list = []
with open('road_section_ids.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['road_section_id'] != '':
            section_id_list.append(row['road_section_id'])
            youbike_stop_list.append(row['youbike_stop_num'])

print section_id_list

# Youbike
url = "http://data.taipei/youbike"
urllib.urlretrieve(url, "data.gz")
f = gzip.open("data.gz", 'r')
jdata = f.read()
f.close()
data = json.loads(jdata)


header = ["road_section_id", "youbike_stop_num", "lat", "lng"]
insertList = []
insertList.append(header)

# itr section_id_list
for idx, val in enumerate(section_id_list):
    u_val = '{0:04}'.format(int(youbike_stop_list[idx]))
    for key,value in data["retVal"].iteritems():
        sno = value["sno"]
        if sno == u_val:
            insertList.append([val, u_val, value["lat"], value["lng"]])

# write file

fileName = strftime("section_id_with_youbike_info.csv")
myFile = open(fileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(insertList)

print "Complete!"
