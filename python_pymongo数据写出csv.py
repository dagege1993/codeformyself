from pymongo import MongoClient

# 生产环境
# client = MongoClient(host='192.168.111.39', port=27017)
# db_auth = client.admin
# db_auth.authenticate("jkspider", "adminadmin")
# db = client['jkspider']['duolabao']
# 本地
client = MongoClient(host='localhost', port=27017)
db_auth = client.admin
# db_auth.authenticate("jkspider", "adminadmin")
db = client['duolabao']['jianfeng']

queryArgs = {'entName': '郑州市金水区董氏兄弟水果超市'}
search_res = db.find(queryArgs)

import csv

csvFile2 = open('lipeipei.csv', 'a', newline='', encoding='utf-8')  # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile2)
insert_time = []
status = []
entName = []
creditCode = []
orderAmount = []
customerNum = []
platformId = []
completeTime = []
orderNum = []
import pandas as pd

insert_time_list = []
name = []
for record in search_res:
	insert_time.append(record.get('insert_time'))
	insert_time.append(record.get('status'))
	insert_time.append(record.get('entName'))
	insert_time.append(record.get('creditCode'))
	insert_time.append(record.get('orderAmount'))
	insert_time.append(record.get('customerNum'))
	insert_time.append(record.get('platformId'))
	insert_time.append(record.get('completeTime'))
	insert_time.append(record.get('orderNum'))
	insert_time_list.append(insert_time)
	insert_time = []
print(insert_time_list[0:1])

names = ["insert_time", "status", "entName", "creditCode", "orderAmount", "customerNum", "platformId", "completeTime",
         "orderNum"]

test = pd.DataFrame(columns=names, data=insert_time_list)
test.to_csv('shuiguochaoshi.csv')
#
# df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['c1', 'c2', 'c3'])
# print(df)


# ll = [[1, 2, 3], [1, 5, 6], [2, 5, 6], [3, 5, 6]]
# print(ll[0:2])
