import zipfile
import os
import json
import csv
import xml.etree.ElementTree as ET
import shutil


zipDir = '..\data\zip'
jsonDir = '..\data\json'
csvDir = '..\data\csv'
xmlDir = r'..\data\xml'

def jsontocsv(input_json_path, output_csv_path):
    with open(input_json_path) as json_file:
        data = json.load(json_file)
    vehicle_data = data['vehicles']
    with open(output_csv_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(list(vehicle_data[0].keys()))
        for vehicle in vehicle_data:
            csv_writer.writerow(vehicle.values())

# using ElementTree; for better performance should use lxml library
def csvtoxml(input_csv_path, output_xml_path):
    with open(input_csv_path,'r') as csv_file:
        data = csv.reader(csv_file)
        xmlData = ET.Element('vehicles')
        keys = []
        count = 0
        for row in data:
            if count == 0:
                keys = row
                #print('keys: '+' ,'.join(keys))
                count += 1
            else:
                vehicleTag = ET.SubElement(xmlData,'vehicle')
                for j in range(len(row)):
                    itemElem = ET.SubElement(vehicleTag,keys[j])
                    itemElem.text = row[j]
                    #print('key: '+keys[j]+' value: '+row[j])
        b_xml = ET.tostring(xmlData)
        with open(output_xml_path,'wb') as xml_file:
            xml_file.write(b_xml)


# decompressing input zip file in to csv folder
with zipfile.ZipFile('..\data\zip\input.zip','r') as my_zip:
    my_zip.extractall('..\data\json')
print('decompressing input.zip into json folder completed')

with os.scandir(jsonDir) as it:
    for entry in it:
        if entry.is_file() and entry.name.endswith(".json"):
            jsontocsv(os.path.join(jsonDir,entry.name),os.path.join(csvDir,entry.name[:-5]+".csv"))
            print(entry.name[:-5]+".csv is created")

with os.scandir(csvDir) as it:
    for entry in it:
        if entry.is_file() and entry.name.endswith(".csv"):
            csvtoxml(os.path.join(csvDir,entry.name),os.path.join(xmlDir,entry.name[:-4]+".xml"))
            print(entry.name[:-4]+".xml is created")

shutil.make_archive('output','zip',xmlDir)
print('compressing xml folder into output.zip completed')
shutil.move('output.zip', os.path.join(zipDir,'output.zip'))
