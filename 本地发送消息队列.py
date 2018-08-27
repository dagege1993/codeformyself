import pika

hostname = 'http://10.90.60.10'
port = 5672
# virtual_host = '/'
credentials = pika.PlainCredentials(username='guest', password='guest')
parameters = pika.ConnectionParameters(host=hostname, port=port)
connection = pika.BlockingConnection(parameters)
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 声明queue,消息将在这个队列中进行传递,如果队列不存在,则创建
channel.queue_declare(queue='hello')

# exchange-- 它使我们能够确定指定消息应该到哪个队列去,
# 向队列插入数值 rounting_key 是队列名,Body是要插入的内容
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='helloword')
print("[x] Sent ‘hello word!‘")
connection.close()
