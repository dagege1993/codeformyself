import pika

# 生产者代码
# username = 'admin'  # 指定远程rabbitmq的用户名密码
# pwd = '123456'
# user_pwd = pika.PlainCredentials(username, pwd)
# s_conn = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=user_pwd))  # 创建连接
# chan = s_conn.channel()  # 在连接上创建一个频道

# import pika
hostname = '10.90.60.10'
port = 5672
virtual_host = '/'
credentials = pika.PlainCredentials(username='bigdata', password='bigdata')
parameters = pika.ConnectionParameters(host=hostname, port=port, virtual_host=virtual_host)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

# 声明queue,消息将在这个队列中进行传递,如果队列不存在,则创建
channel.queue_declare(queue='loanRiskModelFromPython', durable=True)

# exchange-- 它使我们能够确定指定消息应该到哪个队列去,
# 向队列插入数值 rounting_key 是队列名,Body是要插入的内容
body = {'platformId': '20000004', 'customerOpenId': 'c1852d65eec745d728a84de38b08293a', 'riskId': '123',
        'entName': '灵宝市大旺副食商行', 'creditCode': '92411282MA40L9CL1J', 'startDate': '2018-07-06', 'endDate': '2018-07-07',
        'accessToken': 'f3f0597f-c8f2-4337-9c75-1006dac19924', 'refreshToken': '81ba0cc7-d835-494e-a028-b6cc91597b95'}

channel.basic_publish(exchange='',
                      routing_key='loanRiskModel4Python',
                      body=str(body))
print("[x] Sent ‘hello word!‘")
connection.close()
