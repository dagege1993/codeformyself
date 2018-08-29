import json

import pika

# 测试环境mq参数
# hostname = '192.168.109.22'
# port = 5672
# virtual_host = '/'
# credentials = pika.PlainCredentials(username='bigdata', password='bigdata')
# parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host, credentials=credentials)
# connection = pika.BlockingConnection(parameters)


# 本地可以连接的mq消息


parameters = pika.ConnectionParameters('10.90.60.10', 5672, virtual_host='/')
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
# 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
channel.queue_declare(queue='kryRiskModelFromPythons', durable=True)


# 定义一个回调函数来处理，这边的回调函数就是将信息打印出来。
def callback(ch, method, properties, body):
	print('-->', ch, method, properties)
	print("[x] Received %s" % body)
	str_param = str(body, encoding="utf-8")
	print('mq消息转字符串', str_param)


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(callback, queue='kryRiskModelFromPythons', no_ack=True)  # no_ack=True表示在回调函数中不需要发送确认标识

print('[*]waitingfor messages.To exit press CTRL+C')

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
channel.start_consuming()
