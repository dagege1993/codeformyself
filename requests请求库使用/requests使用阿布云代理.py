import requests

# 要访问的目标页面
# targetUrl = "https://baijiahao.baidu.com/s?id=1587104143792286681&wfr=spider&for=pcm"
# targetUrl = "http://www.dianping.com/shop/4013473"
targetUrl = "https://www.meituan.com/meishi/42081214/"

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
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
}

resp = requests.get(targetUrl, proxies=proxies, headers=headers)

print(resp.status_code)
print(resp.text)
