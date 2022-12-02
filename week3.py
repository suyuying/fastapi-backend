import csv
import json
import re
import sys

import requests
response=requests.get("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json")
if response.status_code == 200:
    pass
else:
    print(f'something wrong {response.status_code}')
    sys.exit(1)
response_json=response.json()
# with open('data.csv','w',encoding='utf-8') as f:
# print(response_json['result']['results'][0])
# print([ response_json['result']['results'][0][key] for key in ["stitle","longitude","latitude","address", "file"] ])
clean_datas=[]
for result in response_json['result']['results']:
    single_data = {}
    for key in ["stitle","longitude","latitude","address", "file"]:
        if key == "address":
            try:
                address_pattern = re.compile(r'中正區|萬華區|中山區|大同區|大安區|松山區|信義區|士林區|文山區|北投區|內湖區|南港區')
                address = address_pattern.search(result[key]).group(0)
            except:
                address="none"
            finally:
                single_data[key] = address
                continue
        if key =="file":
            try:
                print(result[key])
                jpg_pattern=re.compile(r'https://.*?jpg',flags=re.I)
                jpg=jpg_pattern.match(result[key]).group(0)
                single_data[key] = jpg
            except:
                jpg='none'
            finally:
                single_data[key] = jpg
                continue
        single_data[key]=result[key]
    clean_datas.append(single_data)
with open('data.csv','w') as f:
    write_csv = csv.DictWriter(f,["stitle","longitude","latitude","address", "file"])
    write_csv.writerows(clean_datas)
# try:


#
# print(address,jpg)
# stitle longitude latitude address file


