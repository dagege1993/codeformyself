import pika

# 生产者代码
# username = 'admin'  # 指定远程rabbitmq的用户名密码
# pwd = '123456'
# user_pwd = pika.PlainCredentials(username, pwd)
# s_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=user_pwd))  # 创建连接
# chan = s_conn.channel()  # 在连接上创建一个频道

# import pika
hostname = '192.168.109.22'
port = 5672
virtual_host = '/'
credentials = pika.PlainCredentials(username='bigdata', password='bigdata')
parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host)
# connection = pika.BlockingConnection(parameters)


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
