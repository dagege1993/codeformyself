# python 文件读写,然后插入mongodb
import time
import json
from pymongo import MongoClient

# JSON到字典转化：
# dictinfo = json.loads(json_str) # 输出dict类型
# 字典到JSON转化：
# jsoninfo = json.dumps(dict) # 输出str类型

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now)
client = MongoClient(host='192.168.107.37', port=27017)
db = client['mao']['test']

# 读取1.5G写入pymongo 花了两个小时,迭代器写入
# with open(r'C:\Users\Administrator.DESKTOP-5D2UUSC\Desktop\student.txt', 'r') as file:
#     for line in file:
#         line = json.loads(line)
#         line['shop_id'] = 111
#         db.insert_many(line)
# print(line)


f = open(r'C:\Users\Administrator.DESKTOP-5D2UUSC\Desktop\student.txt', 'r')
lines = f.readlines()
# print(type(lines), len(lines))  # <class 'list'> 21604956
# lines['shop_id'] = 111
n = 100
lines_list = [lines[i:i + n] for i in range(0, len(lines), n)]
# print(len(lines_list))
ll = 111
for line in lines_list:
    result = [json.loads(index) for index in line]
    results = []
    for index in result:
        index['shop_id'] = ll
        results.append(index)
    db.insert_many(results)

end = time.strftime("%Y-%m-%d %H:%M:%S")
print(end)

# python 列表切分
# l = [i for i in range(15)]
# n = 3  # 大列表中几个数据组成一个小列表
# print([l[i:i + n] for i in range(0, len(l), n)])



