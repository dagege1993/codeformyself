import re

want_not = 'href="https://m.liepin.com/job/1914482215.shtml"'
want_to = 'href="https://www.liepin.com/job/1913168906.shtml"'
print(want_to)
result = re.findall(r"www\.liepin\.com/job/\d{10}.shtml", want_to)
print(result)
# 不知为啥这个正则用在LinkExtractor(allow)不行,
