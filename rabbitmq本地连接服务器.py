import pika

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='localhost'))
channel = connection.channel()

# 定义队列
channel.queue_declare(queue='compute_queue')
print(' [*] Waiting for n')
