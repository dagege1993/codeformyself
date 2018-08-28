# coding:utf-8
import re

from flask import Flask, render_template, url_for

# import pymysql
import json

# 生成Flask实例
app = Flask(__name__)


@app.route('/')
def hello():
	return render_template('flask+Ajax实现Echarts异步更新.html')


# /test路由 接收前端的ajax请求
@app.route('/test', methods=['POST'])
def my_echart():
	# 连接数据库
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='test')
	# cur = conn.cursor()
	# sql = 'SELECT t.id,t.tdsvalue FROM tvalues t'
	# cur.execute(sql)
	# u = cur.fetchall()
	
	# 转换成JSON数据格式
	jsonData = {}
	xdays = []
	yvalues = []
	
	with open('shunqiwangspider.log', 'rb') as f:
		logs = f.read().decode('utf-8')
	
	ll = re.findall('2018-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2} \[scrapy.extensions.logstats\] INFO: Crawled .*',
	                logs)
	str_ll = str(ll)
	time_list = re.findall('[\d]{2}:[\d]{2}:[\d]{2}', str_ll)
	pages_min_list = re.findall('at' + ' \d+ ' + 'pages/min', logs)
	print(pages_min_list)
	pages_min_lists = []
	for page in pages_min_list:
		page_rate = page.split(' ')[1]
		pages_min_lists.append(page_rate)
	print(pages_min_lists)
	print(len(pages_min_lists), len(time_list))
	
	jsonData['xdays'] = time_list
	jsonData['yvalues'] = pages_min_lists
	# json.dumps()用于将dict类型的数据转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
	j = json.dumps(jsonData)
	
	# cur.close()
	# conn.close()
	
	# 在浏览器上渲染my_template.html模板（为了查看输出的数据）
	return (j)


if __name__ == '__main__':
	# 运行项目
	app.run(debug=True)
