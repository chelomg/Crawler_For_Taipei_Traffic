import urllib
import gzip
import json
from time import gmtime, strftime
import csv
import os

# Roadspeed
gzName = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".gz"
url = "https://tcgbusfs.blob.core.windows.net/blobtisv/GetVD.xml.gz"
urllib.urlretrieve(url, gzName)
fullfilename = os.path.join("/", gzName)

# Youbike
url = "http://data.taipei/youbike"
urllib.urlretrieve(url, "data.gz")
f = gzip.open("data.gz", 'r')
jdata = f.read()
f.close()
data = json.loads(jdata)

my_list = ["0001", "0006", "0007", "0011", "0088", "0132", "0163", "0030", "0036", "0083", "0176", "0162", "0121", "0210", "0240", "0021", "0015", "0050", "0175", "0170", "0179", "0046", "0279", "0201", "0026", "0115", "0186", "0288", "0082", "0313", "0080", "0275", "0208", "0120", "0090", "0143", "0144", "0142", "0094", "0098", "0215", "0078", "0079", "0140", "0099", "0134", "0188", "0097", "0167", "0375", "0122", "0129", "0191", "0214", "0158", "0148", "0149", "0202", "0165", "0117"]

header = ["number", "stop_name", "can be rented num", "time"]
insertList = []
insertList.append(header)

for key,value in data["retVal"].iteritems():
    sno = value["sno"]
    snaen = value["snaen"]
    mday = value["mday"]
    sbi = value["sbi"]
    if sno in my_list:
        insertList.append([sno, snaen.encode('ascii', 'ignore').decode('ascii'), sbi, mday])
        print "NO." + sno + " " + snaen + " Time: " + mday + " can rent: " + sbi

# write file

fileName = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ".csv"
myFile = open(fileName, 'w')

with myFile:
    writer = csv.writer(myFile)
    writer.writerows(insertList)

print "Complete!"
