with open('ll.text', 'rb') as f:
    content = f.read().decode('utf-8')

from lxml.html import clean

cleaner = clean.Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False,
                        safe_attrs_only=False)
content = cleaner.clean_html(content)
print(content)

import re

# * 号代表字符可以不出现，也可以出现一次或者多次
reg = re.compile("<[^>]*>")  # re的一般步骤是先使用re.compile()函数，将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果
content = reg.sub('', content)
print(111, type(content))
f = open('cleaned.txt', 'wb+')
content = str.encode(content)  # 字符串转bites类型
f.write(content)
f.close()

# 文件读取
with open('cleaned.txt', 'rb') as f:
    content = f.read().decode('utf-8')

lines = content.split('\n')
indexes = range(0, len(lines))  # 创建一个整数列表
counts = []
for line in lines:
    counts.append(len(line))

import pylab

pylab.plot(indexes, counts, linewidth=1.0)  # plot(x,y)
pylab.xlabel(u"横轴")  # 传递的字符串一定要是Unicode编码
pylab.ylabel(u"纵轴")
pylab.legend()  # 让图例生效
pylab.savefig('word_count.png')
pylab.show()
