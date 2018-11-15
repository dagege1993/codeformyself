import re

ll = '作者: 商丘中级人民法院 刘月霞'
# 需求: 商丘市中级人民法院
result = re.findall(': (\w+) 刘', ll)
print(result)
