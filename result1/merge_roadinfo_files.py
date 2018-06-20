import csv
import glob

fileList = glob.glob("*.csv")

with open('roadinfo_result.csv' ,'w') as outFile:
    fileWriter = csv.writer(outFile)
    for idx, file_name in enumerate(fileList):
        with open(file_name,'r') as inFile:
            fileReader = csv.reader(inFile)
            for child_idx, row in enumerate(fileReader):
                if idx == 0 or (idx != 0 and child_idx != 0):
                    fileWriter.writerow(row)
