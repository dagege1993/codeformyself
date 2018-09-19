# 在Unicode和普通如ANSI编码之间转化

ustr = u'abc'
ustr2 = u'abc中国'
print(type(ustr2))
# 一 unicode 转换为普通字符串
print(ustr.encode('ascii'))
# print ustr2.encode('ascii')  # 这个失败  包含ascii表示不了的字符
print(type(ustr2.encode('utf-8')))

# python 内部字符串一般是Unincode编码
# 编码转换要以unicode作为中间编码进行转换,
# 现将其他编码的字符串decode 成unicode ,再从unincode encode另一种编码
