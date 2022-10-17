import os
import csv
import pandas as pd

headers = ['class','name','sex','height','year']

rows_list = [
        [1,'xiaoming','male',168,23],
        [1,'xiaohong','female',162,22],
        [2,'xiaozhang','female',163,21],
        [2,'xiaoli','male',158,21]
    ]

rows_dict = [
        {'class':1,'name':'xiaoming','sex':'male','height':168,'year':23},
        {'class':1,'name':'xiaohong','sex':'female','height':162,'year':22},
        {'class':2,'name':'xiaozhang','sex':'female','height':163,'year':21},
        {'class':2,'name':'xiaoli','sex':'male','height':158,'year':21},
    ]

def read(fileName):
    with open(fileName, 'r+') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def write(fileName):
    with open(fileName, 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows_list)

def dictRead(fileName):
    with open(fileName, 'r+') as f:
       dictReader = csv.DictReader(f)
       for row in dictReader:
           print(row)

def dictWrite(fileName):
    with open(fileName, 'w+', newline='') as f:
        dictWriter = csv.DictWriter(f,headers)
        dictWriter.writeheader()
        dictWriter.writerows(rows_dict)


if __name__ == "__main__":
    csvFile = "out.csv"
    print("try csv read/write:")
    write(csvFile)
    read(csvFile)
    os.remove(csvFile)
    print("try dict read/write:")
    dictWrite(csvFile)
    dictRead(csvFile)
    os.remove(csvFile)
    print("try pandas write:")
    df = pd.DataFrame(rows_dict)
    df.to_csv("out.csv", index=False,sep=',')
    read(csvFile)
    os.remove(csvFile)