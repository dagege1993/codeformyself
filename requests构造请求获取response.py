import re

import requests

url = 'http://b2b.11467.com/search/752.htm'
kv = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
	
}
headers = kv
# requests.get(url, )
resp = requests.get(url)
print(resp.encoding, dir(resp))
print(resp.text.encode(resp.encoding).decode(
	'utf-8'))  # encode() 方法以 encoding 指定的编码格式编码字符串。  decode() 方法以 encoding 指定的编码格式解码字符串

response_text = resp.text.encode(resp.encoding).decode('utf-8')
result = re.findall(r'//www.11467.com/[a-z]+/co/\d+.htm', resp.text)
print(result)
