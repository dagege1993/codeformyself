from pymongo import MongoClient

# 查询到的数据库
client = MongoClient(host='192.168.107.38', port=27017)
db_auth = client.admin

db = client['hlz']['meituan1030']
search_res = db.find()

# 复制的地址
client_copy = MongoClient(host='192.168.107.38', port=27017)
db_copy = client['hlz']['test']

for result in search_res:
	db_copy.insert(result)
