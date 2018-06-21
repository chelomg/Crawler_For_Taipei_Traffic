import csv
import glob

with open('youbike_updated_result.csv' ,'w') as outFile:
    fileWriter = csv.writer(outFile)
    with open('youbike_result.csv','r') as inFile:
        fileReader = csv.reader(inFile)
        for idx, row in enumerate(fileReader):
            if idx != 0:
                time = row[len(row) - 1]
                time_array = time.split( )
                time_array[0] = time_array[0].replace(":", "-")
                row[len(row) - 1] = time_array[0] + " " + time_array[1]
            fileWriter.writerow(row)
