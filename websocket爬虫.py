# encoding=utf-8
'''
股票数据为了追求数据的实时更新,很多时候采用websocket方式
websocket 的方式 用户浏览器和服务端首先进行握手,握手成功就建立连接
websocket爬虫步骤
建立连接-发布消息订阅数据-不断接收数据-定时回应心跳检测
'''
# import websocket
#
# if __name__ == '__main__':
# 	ws = websocket.create_connection('wss://ws.bitforex.com/mkapi/coinGroup1/ws', timeout=10)
# 	ws.send(
# 		'[{"type": "subHq", "event": "trade", "param": {"businessType": "coin-usdt-btc", "dType": 0, "size": 100}}]')  # 订阅交易数据
# 	for i in range(5):
# 		content = ws.recv()
# 		print(content)
# 	ws.close()
# encoding=utf-8

import websocket

if __name__ == '__main__':
	ws = websocket.create_connection('wss://ws.bitforex.com/mkapi/coinGroup1/ws', timeout=10)
	ws.send(
		'[{"type": "subHq", "event": "trade", "param": {"businessType": "coin-usdt-btc", "dType": 0, "size": 100}}]')  # 订阅交易数据
	for i in range(5):
		content = ws.recv()
		print (content)
	ws.close()
