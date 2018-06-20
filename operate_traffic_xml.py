try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from time import gmtime, strftime
import csv
import glob

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

date_zoom = ["2018_06_10", "2018_06_11", "2018_06_12", "2018_06_13", "2018_06_14", "2018_06_15", "2018_06_16", "2018_06_17", "2018_06_18"]

for date_zoom_item in date_zoom:
    fileList = glob.glob("../row_data/" + date_zoom_item + "/*.xml")

    for file_i in fileList:
        file_name = file_i
        file_i = file_i.split('/')

        FN = file_i[len(file_i) - 1]
        D = file_i[len(file_i) - 2].replace("_", ":")
        hour = '{0:02}'.format((int(FN[11:13]) + 8)%24) + ":00:00"

        # load xml file
        tree = ET.ElementTree(file=file_name)

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

        header = ["youbike_stop_num", "lat", "lng", "road_section_id", "road_avg_speed", "time"]
        insertList = []
        insertList.append(header)

        # operate time formate
        time_formate = D + " " + hour

        # itr section_id_list
        for idx, val in enumerate(section_id_list):
            for sdata in trafficInfoRoot.iter( vdPrefix + "SectionData"):
                section_id = sdata.find( vdPrefix + "SectionId").text
                if section_id == val:
                    avg_spd = sdata.find( vdPrefix + "AvgSpd").text
                    insertList.append(['{0:04}'.format(int(youbike_stop_list[idx])), lat_list[idx], lng_list[idx], section_id, avg_spd, time_formate])

        # write file

        fileName =  "result1/" + D + "_" + hour + "_roadinfo.csv"
        myFile = open(fileName, 'w')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(insertList)

print "Complete!"
