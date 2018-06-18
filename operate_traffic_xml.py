try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from time import gmtime, strftime
import csv

section_id_list = []
youbike_stop_list = []
lat_list = []
lng_list = []
with open('section_id_with_youbike_info.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        section_id_list.append(row['road_section_id'])
        youbike_stop_list.append(row['youbike_stop_num'])
        lat_list.append(row['lat'])
        lng_list.append(row['lng'])

# make list unique
#section_id_list = list(set(section_id_list))

# load xml file
tree = ET.ElementTree(file='GetVD.xml')

# xml prefix of tag
vdPrefix = "{http://www.iii.org.tw/dax/vd}"

# find root
root = tree.getroot()

# find roor traffic info child
trafficInfoRoot = {}

# iter traffic info
for child_of_root in root:
    if child_of_root.tag == vdPrefix + "SectionDataSet":
        trafficInfoRoot = child_of_root

header = ["youbike_stop_num", "lat", "lng", "road_section_id", "road_avg_speed"]
insertList = []
insertList.append(header)

# itr section_id_list
for idx, val in enumerate(section_id_list):
    for sdata in trafficInfoRoot.iter( vdPrefix + "SectionData"):
        section_id = sdata.find( vdPrefix + "SectionId").text
        if section_id == val:
            avg_spd = sdata.find( vdPrefix + "AvgSpd").text
            insertList.append(['{0:04}'.format(int(youbike_stop_list[idx])), lat_list[idx], lng_list[idx], section_id, avg_spd])

# write file

fileName = strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + "_roadinfo.csv"
myFile = open(fileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(insertList)

print "Complete!"
