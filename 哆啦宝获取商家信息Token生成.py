import hashlib
import time

spider_data = {"customerOpenId": "a4c7b3aa877daa922dce17bc90c5a131", "startTime": "2018-06-25 00:00:00",
               "endTime": "2018-06-25 23:59:59", "pageNum": "1"}
json_parameter = {'accessToken': 'd706a222-6aca-4b26-a43a-03dbd81fc4e8',
                  'accessKey': 'bf86280ad8f044b6b47b9bd634fdf2c10414873c', 'timestamp': '1541642124380',
                  'token': '400CF996BB22530B55378DE70BB959659A6BF376', 'Content-Type': 'application/json'}


def get_token(json_parameter, spider_data):
	timestamp = int(round(time.time() * 1000))
	print('时间戳是', timestamp)
	b = "secretKey=5ff00210d27a4db989b3de1228cae3995910fa5f&timestamp=" + str(
		timestamp) + "&path=/v1/customerinfo/a4c7b3aa877daa922dce17bc90c5a131"
	
	token = hashlib.sha1(b.encode('utf8')).hexdigest()  # 算法加密生成token
	token = token.upper()
	print('token', token)
	return token


get_token(json_parameter, spider_data)
