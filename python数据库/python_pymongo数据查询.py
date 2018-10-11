from pymongo import MongoClient

# 生产环境
# client = MongoClient(host='192.168.111.39', port=27017)
# db_auth = client.admin
# db_auth.authenticate("jkspider", "adminadmin")
# db = client['jkspider']['duolabao']
# 本地
client = MongoClient(host='localhost', port=27017)
db_auth = client.admin

db = client['duolabao']['jianfeng']

queryArgs = {'entName': '郑州市金水区董氏兄弟水果超市'}
temp = '2018-10-02 15:55:59'
# search_res = db.find({"entName": "郑州市金水区董氏兄弟水果超市"}).sort([{"completeTime": -1}])
search_res = db.find(queryArgs)
# print(search_res)
# for result in search_res:
# 	print(result)
