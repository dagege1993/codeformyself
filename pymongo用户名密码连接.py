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
# client = MongoClient(host='192.168.160.131', port=27017)
client = MongoClient(host='192.168.107.37', port=27017)
db_auth = client.admin
# db_auth.authenticate("spider", "spider")
# print(db_auth.authenticate("test", "test"))
# db = client['hlz']['test']

result = {"company": "深圳万国食尚餐饮管理有限公司333",
          "company_year": "2016年04月22日333",
          "company_type": "有限责任公司（法人独资）333",
          "company_address": "珠市口东大街333",
          "company_license_number": "333"
	
          }
# for i in range(10):
db = client['hlz']['test']
db.insert(result)
# ll = db.find()
# print(ll)
