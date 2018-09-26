import os
import re
import time

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

# '2018-08-27 10:41:45 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)'
#
# with open('shunqiwangspider.log', 'rb') as f:
# 	logs = f.read().decode('utf-8')
#
# ll = re.findall('2018-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2} \[scrapy.extensions.logstats\] INFO: Crawled .*', logs)
# # time_list = []
# page_rate = []
# str_ll = str(ll)
# time_list = re.findall('[\d]{2}:[\d]{2}:[\d]{2}', str_ll)
# # print(time_list)
# pages_min_list = re.findall('at' + ' \d+ ' + 'pages/min', logs)
# print(pages_min_list)
# pages_min_lists = []
# for page in pages_min_list:
# 	page_rate = page.split(' ')[1]
# 	pages_min_lists.append(page_rate)
# print(pages_min_lists)
# print(len(pages_min_lists), len(time_list))

# 就是a和b同时在 a在的时候b不在 a不在的时候b在 a和b都不在


# import requests
#
# s = time.time()
# url = 'http://192.168.107.38:5555/shunqiwangs/random'
# response = requests.get(url)
# t1 = time.time()
# print("顺序执行时间：", int(t1 - s))
# print(response)
# proxy = 'http://' + response.text
# if proxy == ''
# 	return proxy


ll = {'company': '',
      'company_address': '',
      'company_finance': '',
      'company_license_number': '',
      'company_office': '',
      'company_phone_manager': '',
      'company_product': '',
      'company_state': '',
      'company_tel': '',
      'company_type': '',
      'company_year': ''}

# print(type(ll.values()))
# print(dir(ll.values()))
# print(ll.get('company_address'))
# print(type(ll.get('company_address')))


# def values(ll):
# 	k = 0
# 	for i in ll:
# 		if i == '':
# 			k += 1
# 	print('k', k)
# 	print(len(ll))


# ll = ll.values()
# values(ll)
# info = {}
# info['company'] = 0
# print(info.values())
# info.keys() == '':


# print(os.getpid())  # 获取当前进程id

# import redis
#
# host = '192.168.107.38'
# port = '6379'
# result = redis.StrictRedis(host=host, port=port, decode_responses=True)
# counts = result.keys()
# print(type(len(counts)))
# while:
#       len(counts) != 5
#       print()


# import time
# while True:
#         time.sleep(2)
#         print(int(time.time()))


# import urllib.request
#
# response = urllib.request.urlopen("https://www.baidu.com")
# print(response.read().decode("utf-8"))


# bytes 和str 的转换
# a = "李璐"
# b1 = bytes(a, encoding='utf-8')
# print(b1)
# newa1 = str(b1, encoding='utf-8')
# print(newa1)


# ll = '\u9352\u55d7\u57c6\u701b\u6a3a\u504d\u0074\u006f\u006b\u0065\u006e\u935c\u5bc0\u0061\u93c1\u7248\u5d41'
# print(ll)

# import faker
#
# init = faker.Faker(locale='zh-cn')
#
# print(init.ip())


hash_value = hash(str('192.168.1.1')) % 1000
print(type(hash_value))
print(hash_value)
