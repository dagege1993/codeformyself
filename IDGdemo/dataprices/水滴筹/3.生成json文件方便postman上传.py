# encoding=utf8
import csv
import json
import re

year_list = []
data = {}
# csv_reader = csv.reader(open("fill_null_result.csv", ))
# csv_reader = csv.reader(open("fill_null_result1231.csv", ))
# csv_reader = csv.reader(open("fill_null_result0114.csv", ))
csv_reader = csv.reader(open("fill_null_result0218.csv", ))
for i, row in enumerate(csv_reader):
    # print(row)
    if i == 0:
        # 把时间进行切割
        times = row[1:]
        for time in times:
            years = re.findall('(.*)年', time)[0]
            months = re.findall('/(.*)月', time)[0]
            number = re.findall('第(.*)次公示', time)[0]
            if int(months) < 10:
                months = '0' + months
            if int(number) < 10:
                number = '0' + number
            year_list.append(years + "-" + months + "-" + number)
            # print(years, months, number)
            # print(year_list)
    else:
        print(row)
        data = dict(zip(year_list, row[1:]))
        # print(data)
        # data = json.dumps(data)
        # print(data)
        import requests

        url = "http://192.168.103.27:9702/idg/data/update"
        payload = {
            "param": {"company": "水滴筹", "category": "保险计划", "categorySub": "参与人数", "type": "综合意外互助计划", "dtType": "月",
                      "start": "2016-11-1", "end": "2019-11-30"},
            "data": {"2016-11-01": "227229", "2016-12-01": "227229", "2016-12-02": "245051", "2017-01-01": "245051",
                     "2017-01-02": "290215", "2017-02-01": "290215", "2017-03-01": "357876", "2017-03-02": "374315",
                     "2017-04-02": "404808", "2017-05-01": "416719", "2017-05-02": "405828", "2017-06-01": "443475",
                     "2017-07-01": "457993", "2017-08-01": "474018", "2017-08-02": "486388", "2017-09-01": "492730",
                     "2017-09-02": "509945", "2017-10-01": "519506", "2017-10-02": "530139", "2017-11-01": "539599",
                     "2017-11-02": "548727", "2017-12-01": "556823", "2017-12-02": "566947", "2018-01-01": "578641",
                     "2018-01-02": "593838", "2018-01-03": "610886", "2018-03-01": "639932", "2018-03-02": "659877",
                     "2018-04-01": "658787", "2018-04-02": "672730", "2018-05-01": "688923", "2018-05-02": "696917",
                     "2018-05-03": "709089", "2018-06-01": "714657", "2018-06-02": "722549", "2018-07-01": "728857",
                     "2018-07-02": "739156", "2018-08-01": "750713", "2018-08-02": "757274", "2018-09-01": "765602",
                     "2018-09-02": "773800", "2018-10-01": "780156", "2018-10-02": "784909", "2018-11-01": "791940",
                     "2018-11-02": "792941", "2018-11-03": "800257", "2018-11-04": "799648", "2018-12-01": "805054"}}
        headers = {
            'header': "AqZoNwiHXyff4ZDr409DF45EUg=JbJRUmC5eYAVB",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "63f6a64e-2905-4c21-a575-e961dd468443"
        }
        payload['param']['type'] = row[0]  # 拿到保险计划的名字
        payload['data'] = data  # 拿到一一对应的数据
        print(payload)
        payload = json.dumps(payload)  # 转化为字符串的格式
        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
