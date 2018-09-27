# a = “abbbccc” ，用正则匹配为 abccc,不管有多少 b，就出现一次？

a = "abbbccc"
import re

d = re.findall('a(bbb)ccc', a)
print(d)
# 这里的思路不能是还是匹配了,应该用替换

d = re.sub('b+', 'c', a)

print(d)
'''
re.sub(pattern, repl, string, count=0, flags=0)

pattern：表示正则表达式中的模式字符串；

repl：替换的字符串（既可以是字符串，也可以是函数）；

string：要被处理的，要被替换的字符串；

count：匹配的次数, 默认是全部替换
'''

'''
python2和3的区别
print()和 print
input和 raw_input
python3对unicode字符原生支持
python2使用ASC11码
'''

'''
多线程交互,访问数据,如果访问不了就不访问了,怎么避免重读
'''
# 维护一个列表,只要访问过一次数据,就把用户添加到列表里,
# 每次请求前先看有没有这条记录,再加上互斥锁
# 互斥锁为资源引入一个状态：锁定/非锁定。某个线程要更改共享数据时，先将其锁定，此时资源的状态为“锁定”，其他线程不能更改；
# 直到该线程释放资源，将资源的状态变成“非锁定”，其他的线程才能再次锁定该资源。
# 互斥锁保证了每次只有一个线程进行写入操作，从而保证了多线程情况下数据的正确性
# threading模块中定义了Lock类，可以方便的处理锁定：

# 创建锁
# mutex = threading.Lock()
# 锁定
# mutex.acquire([timeout])
# 释放
# mutex.release()



