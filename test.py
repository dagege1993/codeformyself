
import datetime
import json

import requests
from pymongo import MongoClient

str = 'https://bj.lianjia.com/ershoufang/101102997573.html'
import re
import time

# ls = re.findall('https://bj.lianjia.com/ershoufang/(\d+).html', str)
# print(ls)

# dict = {'a': 1, 'b': 2, 'b': '3'}

ll = {
	"data": {
		"orderList": [
			{
				"customerNum": "10021014679680366408447",
				"completeTime": "2016-07-12 15:43:13",
				"orderAmount": "0.01",
				"orderNum": "10021014683093339018474",
				"refundTime": "2016-07-12 15:43:13",
				"memberNum": "10001214641783052104486",
				"status": "REFUND"},
			{
				"customerNum": "10021014679680366408447",
				"completeTime": "2016-07-08 16:54:08",
				"orderAmount": "0.01",
				"orderNum": "10021014679680366408447",
				"requestNum": "1467968309017215",
				"memberNum": "10001214641783052104486",
				"status": "SUCCESS"
			},
			{
				"customerNum": "10021014679680366408447",
				"completeTime": "2016-07-08 16:54:08",
				"orderAmount": "0.01",
				"orderNum": "10021014679487197128438",
				"requestNum": "1467948989004654",
				"memberNum": "10001214641783052104486",
				"status": "INIT"
			}
		],
		"result": "success",
	}
}

dd = {
	"error": {
		"errorCode": "customerNumNotExist",
		"errorMsg": "customerNum not exist"
	},
	"result": "fail"
}
# order_list = ll.get('data').get('orderList')
# print(order_list)
# print(order_list)
dc = 'sfsf'
cc = '11111'
# client = MongoClient(host='192.168.107.37', port=27017)
# db = client['mao']['test1']
# startTime = '2016-04-23'
# for i in order_list:
#     i['shop_id'] = dc + '|' + cc
#     i['spider_time'] = startTime
#     db.insert(i)

# dd = [{'customerNum': '10021014679680366408447', 'completeTime': '2016-07-12 15:43:13', 'orderAmount': '0.01',
#        'orderNum': '10021014683093339018474', 'refundTime': '2016-07-12 15:43:13',
#        'memberNum': '10001214641783052104486', 'status': 'REFUND'},
#       {'customerNum': '10021014679680366408447', 'completeTime': '2016-07-08 16:54:08', 'orderAmount': '0.01',
#        'orderNum': '10021014679680366408447', 'requestNum': '1467968309017215', 'memberNum': '10001214641783052104486',
#        'status': 'SUCCESS'},
#       {'customerNum': '10021014679680366408447', 'completeTime': '2016-07-08 16:54:08', 'orderAmount': '0.01',
#        'orderNum': '10021014679487197128438', 'requestNum': '1467948989004654', 'memberNum': '10001214641783052104486',
#        'status': 'INIT'}]
#
# for i, ll in range(1, len(dd)), dd:
#     print(i, ll)

# a = 2
# ls = round(a, 2)
# print(ls)

# for i in range(2, 3 + 1):
# 	print(i)

# str = 'exception id : 5C9484FB38DD4F4D80DB7E6E5993F1C2,accessToken[f3f0597f-c8f2-4337-9c75-100] has expired'
# if 'accessToken'++' has expired' in str:
# 	print(1)


# client = MongoClient(host='192.168.107.38', port=27017)
# db_auth = client.seeker
# db_auth.authenticate("test", "test")
# # print(db_auth.authenticate("test", "test"))
# db = client['wyf']['test1']
# ll = db.find()
# print(ll)


url = 'http://192.168.108.30:8089/duolabao/refreshToken'

datas = {}
datas['refreshToken'] = '81ba0cc7-d835-494e-a028-b6cc91597b95'
datas['customerOpenId'] = 'c1852d65eec745d728a84de38b08293a'
datas['cooperatorId'] = '20000004'
headers = {}

response = requests.post(url, data=datas)

print(response.text)
data = json.loads(response.text).get('data')
print(data)

# ll = {"code": "0000", "message": "成功",
#       "data": "{\"expiresIn\":\"2591999\",\"accessToken\":\"019fafeb-5b59-41e4-bac6-c344b49c89bf\",\"refreshToken\":\"81ba0cc7-d835-494e-a028-b6cc91597b95\"}"}
# token = json.loads(ll.get('data')).get('accessToken')
# print(token)


# 插入数据库
# def find(parameter):
# 	client = MongoClient(host='192.168.107.38', port=27017)
# 	db_auth = client.admin
# 	db_auth.authenticate("spider", "spider")
# 	db = client['wyf']['text1']
# 	dc = parameter.get('customerOpenId')
# 	cc = parameter.get('riskId')
# 	results = []
# 	# start_time = int(time.time())
# 	count = db.find({'shop_id': dc + '|' + cc}).count()
# 	print(22, count)


# parameter = {"platformId": "20000004", "customerOpenId": "c1852d65eec745d728a84de38b08293a",
#              "riskId": "bcc2cde547fe4440b3c9d6cfbfa6d6f5", "entName": "灵宝市大旺副食商行", "creditCode": "92411282MA40L9CL1J",
#              "startDate": "2017-07-06", "endDate": "2018-07-07", "accessToken": "27a4fc81-4498-431c-b565-e17fdd66600e",
#              "refreshToken": "81ba0cc7-d835-494e-a028-b6cc91597b95"}
#
# print(find(parameter))


