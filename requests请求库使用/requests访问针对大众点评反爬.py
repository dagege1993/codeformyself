import requests

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "HKBM34BTB938682D"
proxyPass = "FAD3D31001A13C74"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
	"host": proxyHost,
	"port": proxyPort,
	"user": proxyUser,
	"pass": proxyPass,
}
proxies = {
	"http": proxyMeta,
	"https": proxyMeta,
}
url = "http://www.dianping.com/shop/4013473"
headers = {
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	'Accept-Encoding': "gzip, deflate",
	'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
	'Connection': "keep-alive",
	'Host': "www.dianping.com",
	'Upgrade-Insecure-Requests': "1",
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
	'Cache-Control': "no-cache",
	'Postman-Token': "04c38857-523c-878b-7ddf-67202fff905b"
}
response = requests.request("GET", url, headers=headers, proxies=proxies)  #
print(response.text)
