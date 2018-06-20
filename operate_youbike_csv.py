from time import gmtime, strftime
import csv
import glob

section_id_list = []
youbike_stop_list = []
lat_list = []
lng_list = []
max_rental_num_list = []
with open('section_id_with_youbike_info.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        section_id_list.append(row['road_section_id'])
        youbike_stop_list.append(row['youbike_stop_num'])
        lat_list.append(row['lat'])
        lng_list.append(row['lng'])
        max_rental_num_list.append(row['max_rental_num'])

date_zoom = ["2018_06_10", "2018_06_11", "2018_06_12", "2018_06_13", "2018_06_14", "2018_06_15", "2018_06_16", "2018_06_17", "2018_06_18"]
for date_zoom_item in date_zoom:
    fileList = glob.glob("../row_data/" + date_zoom_item + "/*.csv")

    for file_i in fileList:
        file_name = file_i
        file_i = file_i.split('/')

        FN = file_i[len(file_i) - 1]
        D = file_i[len(file_i) - 2].replace("_", ":")
        hour = '{0:02}'.format((int(FN[11:13]) + 8)%24) + ":00:00"

        number_list = []
        stop_name_list = []
        can_be_rented_num_list = []
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                number_list.append(row['number'])
                stop_name_list.append(row['stop_name'])
                can_be_rented_num_list.append(row['can be rented num'])



        header = ["youbike_stop_num", "lat", "lng", "max_rental_num", "can_be_rented_num", "rental_per", "time"]
        insertList = []
        insertList.append(header)

        # operate time formate
        time_formate = D + " " + hour

        # itr section_id_list
        for idx, val in enumerate(youbike_stop_list):
            for n_idx, n_val in enumerate(number_list):
                n_val = '{0:04}'.format(int(n_val))
                if n_val == val:
                    max_num = int(max_rental_num_list[idx])
                    can_rented_num = int(can_be_rented_num_list[n_idx])
                    rental_per = float(max_num - can_rented_num)/float(max_num)
                    insertList.append([youbike_stop_list[idx], lat_list[idx], lng_list[idx], max_rental_num_list[idx], can_be_rented_num_list[n_idx], rental_per, time_formate])

        # write file

        fileName = "result/" + D + "_" + hour + "_youbikeinfo.csv"
        myFile = open(fileName, 'w')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(insertList)

print "Complete!"
