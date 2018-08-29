# coding=utf-8
# 读取远程文件上传到hdfs
import json

import requests
from urllib import request
from hdfs import *
from hdfs import HdfsError
import re
import pika
from config_log import Config
from 单元测试.kerunyun_settings import send_message_queue

conf = Config()
logger = conf.getLog()
hostname = '10.90.60.10'
port = 5672
virtual_host = '/'
body = {}


def get_Water_bill(params):
	fliepath_name = []
	try:
		riskId = params.get('riskId')  # 批次号
		# print('批次号%s'% riskId)
		customerOpenId = params.get('customerOpenId')  # 商户id
		# print('商户id%s'% customerOpenId)
		platformId = params.get('platformId')  # 平台id
		# print('平台id%s'% platformId)
		creditCode = params.get('creditCode')  # 社会同意信用代码
		# print('社会同意信用代码%s' % creditCode)
		get_url = params.get('filesUrl')  # 获取到filesUrl列表
		# print('获取到filesUrl列表%s' % get_url)
		logger.info('提取到的参数riskId ,%s' % riskId)
		logger.debug('提取到的参数customerOpenId ,%s' % customerOpenId)
		logger.debug('提取到的参数platformId ,%s' % platformId)
		logger.debug('提取到的参数creditCode ,%s' % creditCode)
		logger.debug('提取到的参数get_url ,%s' % get_url)
		client = InsecureClient('http://192.168.107.33:50070', user='python')  # 连接hdfs
		for f in get_url:  # 遍历获取到所有字典
			get_urls = f
			logger.debug('遍历获取到的字典%s' % get_urls)
			for queue_keys, queue_url in get_urls.items():  # 遍历 拿到所有的keys和values
				code = requests.get(queue_url)  # 看看返回的状态码 判断 链接是否过期
				get_code = code.status_code
				logger.info('请求状态码是%s' % get_code)
				try:
					if get_code != 403:  # 如果不过期 就进去发送请求
						logger.info('遍历拿到所有的keys %s' % queue_keys)
						logger.info('遍历拿到所有的V %s' % queue_url)
						keys_path = queue_keys  # 拿到 keys
						b = re.findall('.*\..*\..*/.*/(.*)\..*\?.*\..*',
						               queue_url)  # 正则匹配名字不带.csv   #.*.*\..*\..*\..*/.*/(.*?)\?.*\..*
						logger.info('匹配出来的文件名%s' % b)
						name = b[0] + '.temp'  # 拼接成后缀为.temp的文件 意思为临时文件.temp文件
						# 匹配.csv
						cmm = re.findall('.*.*\..*\..*\..*/.*/(.*?)\?.*\..*', queue_url)  # 带.csv
						cong = cmm[0]
						logger.info('带csv的文件名%s' % cong)
						# 拼接.csv路径
						mingm = '/user/python/' + platformId + '/' + creditCode + '/' + riskId + '/' + keys_path + '/' + cong
						# print(mingm,'1111111k')
						fliepath = '/user/python/' + platformId + '/' + creditCode + '/' + riskId + '/' + keys_path + '/' + name  # 拼接路径# + name\
						logger.info('拼接的.temp路径%s' % fliepath)
						# print(mingm)
						flie_code = client.status(mingm, strict=False)  # 判断文件是否存在 如过不存在返回None
						# print(flie_code)
						logger.info('判断带csv的文件是否存在,不存在 返回None' % flie_code)
						# print(fliepath)
						csv_code = client.status(fliepath, strict=False)
						# print(csv_code)
						logger.info('判断带temp的文件是否存在,不存在 返回None' % csv_code)
						
						# if ((flie_code!= None) or (csv_code != None)): #如果文件存在 直接删除 然后重新创建路径文件上传
						u_temp = client.delete(fliepath)
						logger.info('删除以.temp为后缀的文件状态是,True为删除成功%s' % u_temp)
						c_csv = client.delete(mingm)
						logger.info('删除以.csv为后缀的文件状态是,True为删除成功%s' % c_csv)
						g = {
							queue_keys: '/user/python' + platformId + '/' + creditCode + '/' + riskId + '/' + keys_path + '/'}
						logger.info('返回的文件路径%s' % g)
						fliepath_name.append(g)
						with client.write(fliepath) as w:
							s = request.urlopen(queue_url).read()  # 读取数据串
							# print(s,"zhehis****")
							logger.info('请求返回的数据%s' % s)
							w.write(s)
							f = fliepath
							logger.info('需要重命名的路径及文件名%s' % f)
							# print(f,'?????')
							client.rename(f, mingm)  # 重命名成.csv
							logger.info('文件重命名完成,存入成功')
							body['requestStatus'] = 200
							body['errMsg'] = '上传hdfs成功'
					
					# else:    #如果文件不存在 直接重新创建路径文件上传
					#     g = {queue_keys: '/user/python' + platformId + '/' + creditCode + '/' + riskId + '/' + keys_path + '/'}
					#     logger.info('返回的文件路径%s' % g)
					#     fliepath_name.append(g)
					#     with client.write(fliepath) as w:
					#         s = request.urlopen(queue_url).read() # 读取数据串
					#         logger.info('请求返回的数据%s' % s)
					#         w.write(s)
					#         f = fliepath
					#         logger.info('需要重命名的路径及文件名%s'% f)
					#         client.rename(f,mingm)#文件重命名成.csv
					#         logger.info('重命名完成')
					#         body['requestStatus'] = 200
					#         body['errMsg'] = '上传hdfs成功'
					else:
						logger.info('链接过期请求状态码是%s' % get_code)
						body['requestStatus'] = 400
						body['errMsg'] = '上传hdfs失败,链接过期'
				
				except HdfsError as e:
					logger.info('hdfs上传失败的原因是%s' % e)
					body['requestStatus'] = 400
					body['errMsg'] = '上传hdfs解析失败'
	except Exception as e:
		logger.info('接收的数据异常%s' % e)
		body['requestStatus'] = 400
		body['errMsg'] = '上传hdfs失败数据异常'
	return fliepath_name


def main(bodys):
	bodys = json.loads(bodys)
	params = bodys
	logger.info('从mq读取到的数据%s' % params)
	riskId = ''
	customerOpenId = ''
	platformId = ''
	creditCode = ''
	try:
		file_path = get_Water_bill(params)  # file_path
		
		riskId = params.get('riskId')  # 批次号
		print('批次号%s' % riskId)
		customerOpenId = params.get('customerOpenId')  # 商户id
		print('商户id%s' % customerOpenId)
		platformId = params.get('platformId')  # 平台id
		print('平台id%s' % platformId)
		creditCode = params.get('creditCode')
		print('社会统一信用代码%s' % creditCode)
		
		body['creditCode'] = creditCode  # 社会统一信用代码
		body['riskId'] = riskId  # 批次号
		body['customerOpenId'] = customerOpenId  # 商户id
		body['platformId'] = platformId  # 平台id
		body['filesUrl'] = file_path
		logger.info('上传hdfs成功%s' % body)
		send_mq(body)
	except Exception as e:  # 数据异常返回的数据
		body['creditCode'] = creditCode  # 社会统一信用代码
		body['riskId'] = riskId  # 批次号
		body['customerOpenId'] = customerOpenId  # 商户id
		body['platformId'] = platformId  # 平台id
		send_mq(body)


def send_mq(body):
	credentials = pika.PlainCredentials('bigdata', 'bigdata')
	# 这里可以连接远程IP，请记得打开远程端口
	parameters = pika.ConnectionParameters('10.90.60.10', 5672, virtual_host='/')  # , credentials=credentials
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()
	channel.queue_declare(queue=send_message_queue, durable=True)
	body = str(body)
	# logger.info('返回mq的body体 %s' % body)
	print(body)
	channel.basic_publish(exchange='', routing_key=send_message_queue, body=body)
	print('发送消息成功')
	logger.info('发送消息成功')
	connection.close()
	return 1


if __name__ == '__main__':
	main(bytes)
