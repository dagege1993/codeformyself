import datetime
import json
import time
import hashlib
import pika
from pymongo import MongoClient

from config_log import Config

# 日志模块
conf = Config()
logger = conf.getLog()
import requests

hostname = '10.90.60.10'
port = 5672
virtual_host = '/'

# 全局变量
body = {}
# 测试刷新accessToken只能尝试三次的参数
max_try = {}


def send_message(body, parameter):
	parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host)
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	
	# 声明queue,消息将在这个队列中进行传递,如果队列不存在,则创建
	channel.queue_declare(queue='loanRiskModelFromPython', durable=True)
	
	# exchange-- 它使我们能够确定指定消息应该到哪个队列去,
	# 向队列插入数值 rounting_key 是队列名,Body是要插入的内容
	
	body["riskId"] = parameter.get("riskId")
	
	body["customerOpenId"] = parameter.get("customerOpenId")
	body["platformId"] = parameter.get("platformId")
	body["refreshToken"] = parameter.get('refreshToken')
	if body['refreshToken'] is None:
		body["refreshToken"] = ' '
	body["accessToken"] = parameter.get('accessToken')
	if body['accessToken'] is None:
		body["accessToken"] = ' '
	
	body = str(body)
	channel.basic_publish(exchange='', routing_key='loanRiskModelFromPython', body=body)
	logger.info('发送消息')
	connection.close()


# 插入数据库
def insert(orderList, parameter):
	client = MongoClient(host='192.168.107.38', port=27017)
	db_auth = client.admin
	db_auth.authenticate("spider", "spider")
	db = client['wyf']['jianfengtest']
	dc = parameter.get('customerOpenId')
	cc = parameter.get('riskId')
	results = []
	# start_time = int(time.time())
	for index in orderList:
		index['shop_id'] = dc + '|' + cc
		index['entName'] = parameter.get('entName')
		index['creditCode'] = parameter.get('creditCode')
		index['platformId'] = parameter.get('platformId')
		st = time.localtime()
		index['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S', st)
		
		try:
			db.insert(index)
		except Exception as e:
			pass
			logger.info('插入数据库模块异常%s', e)
	
	logger.info('插入完成')


# 是否入库查询
def find(parameter):
	client = MongoClient(host='192.168.107.38', port=27017)
	db_auth = client.admin
	db_auth.authenticate("spider", "spider")
	db = client['wyf']['jianfengtest']
	dc = parameter.get('customerOpenId')
	cc = parameter.get('riskId')
	results = []
	# start_time = int(time.time())
	count = db.find({'shop_id': dc + '|' + cc}).count()
	return count


def refresh_token(parameter):
	# print(111, parameter)
	refreshToken = parameter.get('refreshToken')
	url = 'http://118.126.14.44:8109/duolabao/refreshToken'
	customerOpenId = parameter.get('customerOpenId')
	platformId = parameter.get('platformId')
	datas = {}
	datas['refreshToken'] = refreshToken
	datas['customerOpenId'] = customerOpenId
	datas['cooperatorId'] = platformId
	
	response = requests.post(url, data=datas)
	if response.status_code == 200:
		responseJson = json.loads(response.text)
		nev_accessToken = json.loads(responseJson.get('data')).get('accessToken')
		nev_refreshToken = json.loads(responseJson.get('data')).get('refreshToken')
		
		parameter['accessToken'] = nev_accessToken
		# parameter['accessToken'] = 'e8826456-01ab-4dca-95d9-30efbee8122d'
		parameter['refreshToken'] = nev_refreshToken
		# print(222, parameter)
		return parameter


def access_token_out(spider_data, parameter, json_parameter, k):
	parameter = refresh_token(parameter)
	# print('这里需要打印一下参数列表别的字段还有没', parameter)
	accessToken = str(parameter.get('accessToken'))
	json_parameter['accessToken'] = accessToken
	
	url = "https://openrealm.duolabao.com/v1/customer/order/batch/query"  # 请求post url
	k += 1
	logger.info('json_parameter%s', json_parameter)
	logger.info('spider_data%s', spider_data)
	logger.info('parameter%s', parameter)
	
	spider_data = json.loads(spider_data)


# 异常处理模块
def attempt(spider_data, parameter, json_parameter, url, k):
	logger.info('异常处理模块当前爬取参数为%s', spider_data)
	logger.info('异常处理模块当前请求的头参数%s', json_parameter)
	logger.info('异常处理模块当前请求的url%s', url)
	json_parameter["Content-Type"] = "application/json"
	
	response = requests.post(url, headers=json_parameter, data=spider_data)
	# 查询的当天有数据
	responseJson = json.loads(response.text)
	if responseJson.get('data') is not None:
		result = responseJson.get('result')
		if result == 'success':
			logger.info('异常处理模块正常拿到数据', )
			orderList = responseJson.get('data').get('orderList')
			totalPages = responseJson.get('data').get('totalPages')
			test = insert(orderList, parameter)
			return orderList, totalPages, k
	# 查询的当天没有数据
	result = responseJson.get('result')
	if result == 'success' or result == 'fail':
		orderList = 1
		totalPages = 1
		return orderList, totalPages, k
	else:
		logger.info('异常处理模块爬取数据返回错误')


# 爬取模块
def spider(json_parameter, spider_data, url, parameter, k):
	json_parameter['token'] = get_token(json_parameter, spider_data)  # 固定值
	
	customerOpenId = spider_data.get('customerOpenId')
	startTime = spider_data.get('startTime')
	endTime = spider_data.get('endTime')
	pageNum = str(spider_data.get('pageNum'))
	
	spider_data = "{\"customerOpenId\":\"" + customerOpenId + "\",\"startTime\":\"" + startTime + "\",\"endTime\":\"" + endTime + "\",\"pageNum\":\"" + pageNum + "\"}"
	logger.info('当前爬取参数为%s', spider_data)
	logger.info('当前请求的头参数%s', json_parameter)
	logger.info('parameter%s', parameter)
	logger.info('当前请求的url%s', url)
	json_parameter["Content-Type"] = "application/json"
	try:
		response = requests.post(url, headers=json_parameter, data=spider_data)
		responseJson = json.loads(response.text)
		print(response.text)
		# 查询的当天有数据
		if responseJson.get('data') is not None:
			result = responseJson.get('result')
			if result == 'success':
				logger.info('正常爬取模块拿到数据')
				orderList = responseJson.get('data').get('orderList')
				totalPages = responseJson.get('data').get('totalPages')
				insert(orderList, parameter)
				return orderList, totalPages, k
		# 查询的当天没有数据
		result = responseJson.get('result')
		if result == 'success':
			logger.info('%s当天没有流水数据', startTime)
			orderList = 1
			totalPages = 1
			errorMsg = '1'
			return orderList, totalPages, k,
		else:
			error = responseJson.get('error')  # 按照文档应该是这个获取方式,到时候再测
			errorMsg = error.get('errorMsg')
			errorCode = error.get('errorCode')
			logger.info('errorMsg信息%s,%s', errorMsg, errorCode)
			
			# 一次爬取accessToken最多更新三次
			# if k == 3:
			# 	body['errMsg'] = '一天爬取中accessToken三次过期'
			# 	i = 'break'
			# 	totalPages = 1
			# 	k = 1
			# 	# max_try['time'] ='no'
			# 	return i, totalPages, k
			
			# 这儿是accessToken更新模块
			if errorCode == 'accessTokenExpired':
				access_token_out(spider_data, parameter, json_parameter, k)
				i = '1'
				totalPages = 1
				k = 1
				return i, totalPages, k
			
			if errorMsg == 'customerNum must be specified':
				body['errMsg'] = errorMsg
				i = 'break'
				totalPages = 1
				k = 1
				return i, totalPages, k
			if errorMsg == '1':
				i = '1'
				totalPages = 1
				k = 1
				return i, totalPages, k
			else:
				logger.info('爬虫爬到错误信息尝试三次')
				for i in range(1, 4):
					logger.info('爬虫爬取到错误信息尝试第%s次', i)
					orderList, totalPages, k = attempt(spider_data, parameter, json_parameter, url, k)
					
					if isinstance(orderList, list) is True:
						return orderList, totalPages, k
					elif i == 3:
						i = 'break'
						totalPages = 1
						k = 1
						return i, totalPages, k
	
	
	except Exception as e:
		logger.info(e)
		logger.info('爬虫程序异常开始尝试三次')
		for i in range(1, 4):
			orderList, totalPages, k = attempt(spider_data, parameter, json_parameter, url, k)
			
			logger.info('爬虫异常尝试第%s次', i)
			
			if isinstance(orderList, list) is True:
				return orderList, totalPages, k
			elif i == 3:
				i = 'break'
				totalPages = 1
				k = 1
				return i, totalPages, k


# 根据算法拿token
def get_token(json_parameter, spider_data):
	timestamp = int(round(time.time() * 1000))
	startTime = spider_data.get('startTime')
	endTime = spider_data.get('endTime')
	customerOpenId = spider_data.get('customerOpenId')
	pageNum = str(spider_data.get('pageNum'))
	json_parameter['timestamp'] = str(timestamp)
	b = "secretKey=5ff00210d27a4db989b3de1228cae3995910fa5f&timestamp=" + str(
		timestamp) + "&path=/v1/customer/order/batch/query&body={\"customerOpenId\":\"" + customerOpenId + "\",\"startTime\":\"" + startTime + "\",\"endTime\":\"" + endTime + "\",\"pageNum\":\"" + pageNum + "\"}"
	
	token = hashlib.sha1(b.encode('utf8')).hexdigest()  # 算法加密生成token
	token = token.upper()
	
	return token


def json_datalist(parameter):
	Stime = parameter.get('startDate')  # 获取mq传过来的开始的时间
	Etime = parameter.get('endDate')  # 获取mq传过来的结束的时间
	starttime = datetime.datetime.strptime(Stime, '%Y-%m-%d')  # 格式化时间
	endtime = datetime.datetime.strptime(Etime, '%Y-%m-%d')
	result = (endtime - starttime).days
	if result < 0:
		print('时间传入不正确')
		
		body["errMsg"] = "起止时间不正确"
		body["requestStatus"] = "404"
		body["refreshToken"] = parameter.get('refreshToken')
		send_message(body, parameter)
	if result >= 0:
		time_list = []
		for i in range(0, result + 1):
			time_dict = {}
			time_dict['startTime'] = starttime.strftime("%Y-%m-%d 00:00:00")  # 开始时间
			time_dict['endTime'] = starttime.strftime('%Y-%m-%d 23:59:59')  # 结束时间
			time_dict['customerOpenId'] = parameter.get('customerOpenId')
			time_dict['pageNum'] = 1
			time_list.append(time_dict)
			starttime = starttime + datetime.timedelta(days=1)  # 天数循环加一
		
		return time_list


def main(id):
	# 参数格式转换
	parameter = json.loads(str(id, encoding="utf-8"))
	
	json_data_list = json_datalist(parameter)
	
	# 凑齐爬虫接口参数
	accessToken = parameter.get('accessToken')  # 可能会过期,这个值剑锋会给我
	accessKey = 'bf86280ad8f044b6b47b9bd634fdf2c10414873c'  # 固定值
	json_parameter = {}  # 请求头参数列表
	
	json_parameter['accessToken'] = accessToken
	json_parameter['accessKey'] = accessKey
	
	pageNum = 1
	# i是判断是否循环次数和参数列表的长度一样
	i = 0
	# j是用来判断这个循环有没有进入到break里,一旦进入到,就发送失败的消息
	j = 1
	# k用来判断小贷接口返回的acceseToken最多出错三次
	k = 1
	for spider_data in json_data_list:
		i += 1
		print(i, spider_data)
		
		url = "https://openrealm.duolabao.com/v1/customer/order/batch/query"  # 请求post url
		# url = "http://192.168.107.26:18888/v1/customer/order/batch/query"  # 请求post url
		orderList, totalPages, k = spider(json_parameter, spider_data, url, parameter, k)
		print(totalPages)
		if orderList == 'break':
			# print('测试会不会打破这个循环')
			logger.info('爬取的第一页,返回break,打破这个循环')
			j = 0
			break
		if k == 3:
			logger.info('一次爬取过程中,accessToken超过三次刷新')
			j = 0
			break
		
		if totalPages > 1:
			# l 用来记录页数
			for l in range(2, totalPages + 1):
				pageNum = l
				spider_data['pageNum'] = pageNum
				orderList, totalPages, k = spider(json_parameter, spider_data, url, parameter, k)
				if orderList == 'break':
					logger.info('页数增加的死循环里,返回break,打破这个循环')
					j = 0
					break
				
				if len(orderList) == 1000:
					continue
				if len(orderList) != 1000:
					pageNum = 1
					break
	
	if i == len(json_data_list) and j == 1:
		if find(parameter) == 0:
			body["errMsg"] = "当前批次无新增数据"
			body["requestStatus"] = "201"
			send_message(body, parameter)
		else:
			body["errMsg"] = "正确"
			body["requestStatus"] = "200"
			logger.info('抓取成功')
			send_message(body, parameter)
	else:
		errMsg = body.get('errMsg')
		if errMsg is None:
			body["errMsg"] = "错误"
		body["requestStatus"] = "404"
		logger.info('抓取失败')
		send_message(body, parameter)


if __name__ == "__main__":
	main(id)
