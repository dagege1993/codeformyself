from pymongo import MongoClient

# 生产环境
# client = MongoClient(host='192.168.111.39', port=27017)
# db_auth = client.admin
# db_auth.authenticate("jkspider", "adminadmin")
# db = client['jkspider']['duolabao']
# 本地
client = MongoClient(host='localhost', port=27017)
db_auth = client.admin

db = client['localhost_duolabao']['jianfeng']

queryArgs = {'entName': '洛阳市站区新大华超市'}
search_res = db.find(queryArgs)

for result in search_res:
	print(result)
