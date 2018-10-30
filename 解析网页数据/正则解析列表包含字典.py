# encoding=utf-8
import json
import re

lists = [
	'{"title":"临沂美团","url":"http://linyi.meituan.com/"},{"title":"临沂美食","url":"http://linyi.meituan.com/meishi/"},{"title":"临沂临沂市人民医院大店分院美食","url":"http://linyi.meituan.com/meishi/b28366/"}']

work = lists[-1]
# result = json.loads(work)
tt = re.findall('"title":"(.*?)",',work)
print(tt[-1])
# print(result)
