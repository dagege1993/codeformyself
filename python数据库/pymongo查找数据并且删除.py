from pymongo import MongoClient

# 生产环境
client = MongoClient(host='192.168.111.39', port=27017)
db_auth = client.admin
db_auth.authenticate("jkspider", "adminadmin")
db = client['jkspider']['duolabao']

# queryArgs = {'entName': '苏州食永兴餐饮有限公司', 'shop_id': '374eba3e3206deef24ff05471c96286c|c7d5c6fb686c477486615e84410bfc1e'}
# queryArgs = {'entName': '北京竹悦阁美容服务有限公司', 'shop_id': '431202e219d1c1970a29e9e4709ac562|682d7b9cdb7c468ea6ab4fa297c1231d'}
queryArgs = {'entName': '北京豪仕强商贸有限公司', 'shop_id': '3c9f3bde48fd72b64f4b2adb4fbc1787|c39b539d1369416b9e7a4d60e4d5fb99'}
search_res = db.find(queryArgs)

# 统计数据用
i = 0
for result in search_res:
	print(result)
	i += 1
print(i)
# 本地
# client = MongoClient(host='localhost', port=27017)
# db_auth = client.admin
# db = client['localhost_duolabao']['jianfeng']
#
#
# queryArgs = {'entName': '苏州食永兴餐饮有限公司'}
# # queryArgs = {'entName': '北京竹悦阁美容服务有限公司'}
#
# search_res = db.find(queryArgs)
# print(search_res)
# for result in search_res:
# 	print(result)
# 	db.delete_one(result)  #逐条删除




