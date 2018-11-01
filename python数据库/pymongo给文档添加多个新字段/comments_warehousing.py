import json

from pymongo import MongoClient

# 38服务器
from python数据库.pymongo给文档添加多个新字段.get_comments import getcomments

client = MongoClient(host='192.168.107.38', port=27017)
db_auth = client.admin

# db = client['hlz']['meituan1030']
db = client['hlz']['test']
search_res = db.find()

for result in search_res:
	shopid = result.get('ShopID')
	response = getcomments(shopid)
	response_text = response.text
	response_text = json.loads(response_text)
	data = response_text.get('data')
	tags = data.get('tags')
	if tags is None:  # 如果没有标签，就为空
		tags = tags
	else:
		tags = json.dumps(tags, ensure_ascii=False)  # 如果有就转为字符串
	total = data.get('total')
	new_data = {}
	new_data['tags'] = tags
	new_data['total'] = total
	
	db.update({'_id': result['_id']}, {'$set': new_data})
	print(type(tags), total)
