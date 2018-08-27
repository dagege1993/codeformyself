# 根据算法拿token
import hashlib
import time

ll = 'customer_open_id：55583b2deea92bed977eaf2cb2a147ce，accesstoken：e351037b-8592-44db-beb4-e575af3eb551，refreshtoken：aadc23f9-3b71-4fce-aea6-30d338c68ad5，crreditcode：92370786MA3DFE4F25'


def get_token():
	timestamp = int(round(time.time() * 1000))
	b = "secretKey=5ff00210d27a4db989b3de1228cae3995910fa5f&timestamp=" + str(
		timestamp) + "&path=/v1/customerinfo/55583b2deea92bed977eaf2cb2a147ce"
	
	token = hashlib.sha1(b.encode('utf8')).hexdigest()  # 算法加密生成token
	token = token.upper()
	print(timestamp, '时间戳')
	return token


if __name__ == '__main__':
	print(get_token())
