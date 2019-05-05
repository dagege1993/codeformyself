ll = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=1&tag=%E8%B4%AD%E7%89%A9&tag2=%E5%95%86%E5%9F%8E;%E7%94%B5%E5%95%86&order=weekpure&label=zuire&prepage=categorysoft&curpage=categorysoft_%E8%B4%AD%E7%89%A9_%E5%95%86%E5%9F%8E&page=1&os=19&vc=300070071'
import re

result = re.findall('(page=\d+)', ll)
replace_page = result.pop()
l2 = ll.replace(replace_page, 'page=' + str(2))
print(l2)

old_url = 'http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=1&tag=生活服务&tag2=营业厅&order=weekpure&prepage=categorysoft&curpage=categorysoft_%E8%B4%AD%E7%89%A9_%E5%95%86%E5%9F%8E&page=1&os=19&vc=300070071'
sub = re.findall('order=', old_url)

response_url = '<200 http://openbox.mobilem.360.cn/app/getTagAppList?s_stream_app=1&cid=1&tag=%E8%B4%AD%E7%89%A9&tag2=%E5%95%86%E5%9F%8E;%E7%94%B5%E5%95%86&order=weekpure&prepage=categorysoft&curpage=categorysoft_%E8%B4%AD%E7%89%A9_%E5%95%86%E5%9F%8E&page=1&os=19&vc=300070071>'
sub2 = re.findall('(tag2=.*?)&', response_url)
print(sub2)
