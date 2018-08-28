import re

import requests

# url = 'http://192.168.107.38:5555/sina/random'
# response = requests.get(url)
# print(response.status_code)


# ll = '''HTTPConnectionPool(host='1.85.72.195', port=4275): Max retries exceeded with url: http://guangzhou.11467.com/luogangqu/s752/
# (Caused by ProxyError('Cannot connect to proxy.', NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000262DAAECD68>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。',)))'''
#
# dd = re.findall("(host='.*', port=\d+)", ll)
#
# print(dd)


# ll = ["host='223.242.128.198', port=4251"]
# for i in ll:
# 	d = i.split('=')
# 	print(d)
# 	lc = d[1]
# 	print(lc.split(',')[0].strip("'") + ":" + d[-1])


# result = re.findall(r'//www.11467.com/[a-z]+/co/\d+.htm', tt)
# print(result)


# def decrease_proxy(ip):
# 	ip = ip.split('//')[1]
# 	print(ip)
# 	url = 'http://192.168.107.38:5555/shunqiwang/' + ip + '/decrease'
# 	response = requests.get(url)
# 	# print(response.text)
# 	proxy = 'http://' + response.text
# 	return proxy
#
#
# ip = 'http://119.5.210.238:7684'
#
# decrease_proxy(ip)


# f = open('shunqiwangspider.log', 'rb')
# f_read = f.read()
# f_read_decode = f_read.decode('utf-8')
# print(f_read_decode)
'2018-08-27 10:41:45 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)'

with open('shunqiwangspider.log', 'rb') as f:
	logs = f.read().decode('utf-8')

ll = re.findall('2018-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2} \[scrapy.extensions.logstats\] INFO: Crawled .*', logs)
# time_list = []
page_rate = []
str_ll = str(ll)
time_list = re.findall('[\d]{2}:[\d]{2}:[\d]{2}', str_ll)
# print(time_list)
pages_min_list = re.findall('at' + ' \d+ ' + 'pages/min', logs)
print(pages_min_list)
pages_min_lists = []
for page in pages_min_list:
	page_rate = page.split(' ')[1]
	pages_min_lists.append(page_rate)
print(pages_min_lists)
print(len(pages_min_lists), len(time_list))
