import pika

hostname = '10.90.60.10'
port = 5672

virtual_host = '/'
# parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host)
parameters = pika.ConnectionParameters(host=hostname, virtual_host=virtual_host)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)  # 使用basic_qos方法，并设置prefetch_count=1。这样是告诉RabbitMQ，在同一时刻，不要发送超过1条消息给一个工作者worker 公平调度

# 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
channel.queue_declare(queue='loanRiskModel4Python', durable=True)


# 定义一个回调函数来处理，这边的回调函数就是将信息打印出来。
def callback(ch, method, properties, body):
	print('-->', ch, method, properties)
	print("[x] Received %s" % body)
	id = body
	print(id)


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(callback,
                      queue='loanRiskModel4Python',
                      no_ack=True  # no_ack=True表示在回调函数中不需要发送确认标识
                      )

print('[*]waitingfor messages.To exit press CTRL+C')

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
channel.start_consuming()
