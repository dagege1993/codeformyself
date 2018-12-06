registered_capital = ['16.4541 万人民币', '10.769 万人民币', '1.2546 万人民币', '0.9873 万人民币', '46.1538 万人民币', '23.077 万人民币',
                      '1.2546 万人民币', '4.615 万人民币', '11.3122 万人民币', '1.2546 万人民币']
registered_capital = sum([float(capital.replace('万人民币', '').strip()) for capital in registered_capital])
# print(registered_capital)
test = list(set(['-', '-', '-', '-']))
for capital in test:
    if '-' == capital:
        test.remove(capital)  # 列表按值去掉元素
# print(test)

# 万一运到['30 万人民币人民币', '95 万人民币人民币', '25 万人民币人民币', '255 万人民币人民币', '125 万人民币人民币', '70 万人民币人民币'] 就解析不了了
# filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。

# 该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。

# str.filter:如果字符串只包含数字则返回 True 否则返回 False。

import re

registered_capital = ['16.4541 万人民币', '95 万人民币人民币', '25 万人民币人民币', '-', '331.4754 万人民币']
registered_capital = list(set(registered_capital))  # 为了去重重复的'-'元素
for capital in registered_capital:
    if '-' == capital:
        registered_capital.remove(capital)  # 列表按值去掉元素
print(sum([int(re.findall("\d+", capital)[0]) for capital in registered_capital]))
