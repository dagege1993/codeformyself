# 反转字符串
old_str = 'abcd'
new_str = old_str[::-1]
print(new_str)
# 列表的reverse
l = list(old_str)
result = "".join(l.reverse())
"""
 [start:end:step]

• [:] 提取从开头（默认位置0）到结尾（默认位置-1）的整个字符串
• [start:] 从start 提取到结尾
• [:end] 从开头提取到end - 1
• [start:end] 从start 提取到end - 1
• [start:end:step] 从start 提取到end - 1，每step 个字符提取一个
• 左侧第一个字符的位置/偏移量为0，右侧最后一个字符的位置/偏移量为-1

"""

# 用 select 语句输出每个城市中心距离 市中心 大于20km酒店数？
# select count(hotel) i from hotel where distance > 20 ;



