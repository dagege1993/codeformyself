from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv

# # seeker是创建的数据库账号
# client = MongoClient(host='192.168.107.38', port=27017)
# db_auth = client.admin
# db_auth.authenticate("spider", "spider")
# db = client['wyf']['test1']
# ll = db.find()
# print(ll)

# 链接虚拟试试
client = MongoClient(host='192.168.160.131', port=27017)
db_auth = client.admin
# db_auth.authenticate("spider", "spider")
# print(db_auth.authenticate("test", "test"))
db = client['wyf']['test1']
ll = db.find()
print(ll)
