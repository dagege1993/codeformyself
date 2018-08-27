import hashlib
import time
import requests

tt = int(time.time() * 1000)  # 时间戳
# 拼接待加密字符串
b = "secretKey=5ff00210d27a4db989b3de1228cae3995910fa5f&timestamp=" + str(
	tt) + "&path=/v1/customer/order/batch/query&body={\"customerOpenId\":\"c1852d65eec745d728a84de38b08293a\",\"startTime\":\"2018-07-07 00:00:00\",\"endTime\":\"2018-07-07 23:59:59\",\"pageNum\":\"1\"}"
token = hashlib.sha1(b.encode('utf8')).hexdigest()  # 算法加密生成token
tokens = token.upper()
# 请求参数
post_data = "{\"customerOpenId\":\"c1852d65eec745d728a84de38b08293a\",\"startTime\":\"2018-07-07 00:00:00\",\"endTime\":\"2018-07-07 23:59:59\",\"pageNum\":\"1\"}"
# 请求头
post_headers = {
	"timestamp": str(tt),
	"token": str(tokens),
	"accessToken": "f3f0597f-c8f2-4337-9c75-1006dac19924",
	"accessKey": "bf86280ad8f044b6b47b9bd634fdf2c10414873c",
	"Content-Type": "application/json",
}
url = "https://openrealm.duolabao.com/v1/customer/order/batch/query"  # 请求poost url
print('头', post_headers)
print('body', post_data)
resp = requests.post(url=url, headers=post_headers, data=post_data)
print(resp.text)

