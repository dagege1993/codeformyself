import json
import requests
import pandas as pd

path = r"C:\Users\Administrator.DESKTOP-DV7S27B\Desktop\需要维护的数据\流利说核心.xlsx"
data = pd.read_excel(path, sheetname='上传数据源')  # 读取数据
columns_name = data.columns  # 列名字
# print(columns_name)
names = data['时间'][2:]  # 根据列名取值
# print(names)
# 需要取到所有的列名取最后一个
Column_name_list = data.columns.values.tolist()  # 获取全部列名生成列表
last_column = Column_name_list[-1]  # 获取最后一列的名字,根据名字去获取数据
day_result = data[last_column]
insert_time = day_result[0]  # 插入时间
insert_time = insert_time.strftime("%Y-%m-%d")
# print(insert_time)
day_result = data[last_column][2:]  # 列表切片,把后续几个列表全部切除
# print(day_result)
dicts = dict(zip(names, day_result))  # 把两列对应为字典
# print(dicts)
data.dropna(axis=0, how='any')  # axis 指 轴，0是行，1是列，把一行的空值去掉
for key, value in dicts.items():
    if isinstance(key, str) is True:  # and '课程数,课程数' in key
        print(key, value)
        result = key.split(',')
        categorySub = result[0].strip()  # 去掉两边空格
        type = result[1].strip()
        url = "http://192.168.103.27:9702/idg/data/update"
        payload = {
            "param": {"company": "流利说", "category": "课程", "categorySub": "课程报名人次数差值", "type": "全部课程", "dtType": "月",
                      "start": "2018-12-23", "end": "2019-09-01"}, "data": {"2018-12-16": "41870772", }}
        payload["param"]['categorySub'] = categorySub
        payload["param"]['type'] = type
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

