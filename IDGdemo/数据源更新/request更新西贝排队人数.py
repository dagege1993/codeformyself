import json
import requests
import pandas as pd

path = r"C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\西贝排队人数.xlsx"
data = pd.read_excel(path, sheetname='Sheet1')  # 读取数据
columns_name = data.columns  # 列名字
# print(columns_name)

# 需要取到所有的列名取最后一个
Column_name_list = columns_name.values.tolist()  # 获取全部列名生成列表
for column_name in Column_name_list:
    if column_name == 'city':
        city_list = data[column_name].values.tolist()
    else:

        results = data[column_name].values.tolist()
        print(results)
        insert_time = column_name.strftime("%Y-%m-%d")
        dicts = dict(zip(city_list, results))  # 把两列对应为字典

        for key, value in dicts.items():
            if isinstance(key, str) is True:
                print(key, value)
                result = key
                url = "http://192.168.103.27:9702/idg/data/update"
                payload = {
                    "param": {"company": "西贝", "category": "排队人数", "categorySub": "城市等级", "type": "城市级别", "dtType": "日",
                              "start": "2018-12-23", "end": "2019-09-01"}, "data": {"2018-12-16": "41870772", }}
                payload["param"]['type'] = result
                payload["param"]['start'] = insert_time
                payload["data"] = {}
                payload["data"][insert_time] = value
                print(payload)
                payload = json.dumps(payload)
                headers = {
                    'header': "AqZoNwiHXyff4ZDr409DF45EUg=JbJRUmC5eYAVB",
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                    'Postman-Token': "eba75cf1-209e-4d96-925f-56604b316b71"
                }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text)
