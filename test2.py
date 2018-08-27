import pika

hostname = '10.90.60.10'
port = 5672
# virtual_host = '/api'
# virtual_host=virtual_host
parameters = pika.ConnectionParameters(host=hostname, port=port, )
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
channel.queue_declare(queue='loanRiskModelFromPython1', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))

    # 告诉rabbitmq使用callback来接收信息


channel.basic_consume(callback, queue='loanRiskModelFromPython1', no_ack=True)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
