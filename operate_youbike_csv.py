from time import gmtime, strftime
import csv

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

file_name = '2018_06_10_19_00_01.csv'

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
b_time = file_name[0:10].replace("_", "-")
s_time = file_name[11:16].replace("_", ":")
time_formate = b_time + " " + s_time + ":00"

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

fileName = time_formate + "_youbikeinfo.csv"
myFile = open(fileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(insertList)

print "Complete!"
