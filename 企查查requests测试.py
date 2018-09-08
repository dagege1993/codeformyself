import re

import requests
import scrapy
import faker

f = faker.Faker(locale='zh_CN')
headers = {
	"accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	"accept-encoding": 'gzip, deflate, br',
	"accept-language": 'zh-CN,zh;q=0.9,en;q=0.8',
	"cache-control": 'max-age=0',
	"upgrade-insecure-requests": '1',
	"user-agent": f.chrome(),
}

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
	# "https": proxyMeta,
}

url = 'https://www.qichacha.com/firm_b8a464c037c5baa56f63badc2f07737d.html'

# proxies = {
# 	'http': 'http://1.29.109.111:4226',
#
# }
# response = requests.get(url, headers=headers, proxies=proxies)
# print(response.text)
# page_sel = scrapy.Selector(text=response.text)
# result = page_sel.xpath("//ul[contains(@class,'list-group no-bg auto')]//a").extract()

# result = re.findall('firm_d1390dbdde4e866dd7b76d80c513c17c', response.text)
# print(result)


ll = ['/g_AH.html', '/g_BJ.html']
for i in ll:
	# print(i)
	i = i.replace('.html', '')
	print(i)
# tt = '/g_AH.html'
# print(tt.split('/'))
