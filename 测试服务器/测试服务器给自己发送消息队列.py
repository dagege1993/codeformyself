# coding=utf-8
import pika

# 生产者代码
# username = 'admin'  # 指定远程rabbitmq的用户名密码
# pwd = '123456'
# user_pwd = pika.PlainCredentials(username, pwd)
# s_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=user_pwd))  # 创建连接
# chan = s_conn.channel()  # 在连接上创建一个频道

# import pika

# 本地可以连接MQ
hostname = '10.90.60.10'
port = 5672
virtual_host = '/'
credentials = pika.PlainCredentials(username='bigdata', password='bigdata')
parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 测试服务器
# hostname = '192.168.109.22'
# port = 5672
# virtual_host = '/'
# credentials = pika.PlainCredentials(username='bigdata', password='bigdata')
# parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host, credentials=credentials)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()

# 声明queue,消息将在这个队列中进行传递,如果队列不存在,则创建
channel.queue_declare(queue='riskModel4PythonAddition', durable=True)

# exchange-- 它使我们能够确定指定消息应该到哪个队列去,
# 向队列插入数值 rounting_key 是队列名,Body是要插入的内容
body = {
	'platformId': '60000001',
	'customerOpenId': 'b75b14255acd18a05b60b71290478277',
	'riskId': 'fb358c7443644219948f06d9db8ca683',
	'entName': '洛阳市站区新大华超市',
	'creditCode': '92411282MA40L9CL1J',
	'startDate': '2018-08-21',
	'endDate': '2018-10-07',
	'accessType': '4',
	'accessToken': '5d9f8ad2-c088-4536-bce0-f3f51009a0d2'
}

channel.basic_publish(exchange='',
                      routing_key='riskModel4PythonAddition',
                      body=str(body))
print('[x] Sent ‘hello word!‘')
connection.close()
