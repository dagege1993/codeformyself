import re

from flask import Flask, render_template, url_for

# 生成Flask实例
app = Flask(__name__)


@app.route('/')
def my_echart():
	# 在浏览器上渲染my_templaces.html模板
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
	# return render_template('my_template.html', pages_min_lists=pages_min_lists, time_list=time_list)
	return render_template('my_template_test.html', pages_min_lists=pages_min_lists, time_list=time_list)


if __name__ == "__main__":
	# 运行项目
	app.run(debug=True)
