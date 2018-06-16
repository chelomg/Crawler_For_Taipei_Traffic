try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from time import gmtime, strftime
import csv

section_id_list = []
youbike_stop_list = []
with open('road_section_ids.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        section_id_list.append(row['road_section_id'])
        youbike_stop_list.append(row['youbike_stop_num'])

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

header = ["youbike_stop_num", "road_section_id", "road_total_vol"]
insertList = []
insertList.append(header)

# itr section_id_list
for idx, val in enumerate(section_id_list):
    for sdata in trafficInfoRoot.iter( vdPrefix + "SectionData"):
        section_id = sdata.find( vdPrefix + "SectionId").text
        if section_id == val:
            total_vol = sdata.find( vdPrefix + "TotalVol").text
            insertList.append(['{0:04}'.format(int(youbike_stop_list[idx])), section_id, total_vol])

# write file

fileName = strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + "_roadinfo.csv"
myFile = open(fileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(insertList)

print "Complete!"
