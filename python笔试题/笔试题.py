# 北京号外科技爬虫面试题
# 单引号,双引号,三引号区别
# 三引号表示字符串,并且可以表示多行,而且可以表示多行注释


# yield  使用场景
# 生成器, 当有多个返回值的时候,用return全部一起返回了,需要单个逐一返回可以用yield


# 首信python 研发面试题
# python List,tuple,dict,set 有什么区别,主要用于什么场景
'''
# list,tuple有序列表;dict,set无序列表
# list 元素可变,tuple元素不可变
# dict和set的key不可变,唯一性
set只有去重,并集,交集等
list,tuple 索引,切片,检查成员
dict 查询效率高,但消耗内存多
list,tuple查询效率低,但是消耗内存小


应用场景:
list: 简单的数据集合,可以使用索引
tuple: 吧一些数据当做一个整体去使用,不能更改
dict: 使用键值对进行关联的数据
set 数据只出现一次,只关心数据是否出现.不关心其位置
'''

# 斯沃创智
# python is和==的区别

'''
python对象包含三要素,id,type,value
id是用来标识一个对象的,type标识对象类型,value是对象的值
is是判断a对象是否是b对象,是通过ID来判断的
== 是判断a对象的值是否和b对象的值相等是通过value来判断的

'''


# Python 字典 fromkeys() 函数用于创建一个新字典，以序列 seq 中元素做字典的键，value 为字典所有键对应的初始值。
# 是利用 map 的 fromkeys 来自动过滤重复值，map 是基于 hash 的，大数组的时候应该会比排序快点。
def distFunc1():
    a = [1, 2, 4, 2, 4, 5, 6, 5, 7, 8, 9, 0]
    b = {}
    b = b.fromkeys(a)
    print(b)
    print(b.keys())
    a = list(b.keys())
    print(a)


# if __name__ == '__main__':
#     distFunc1()


# 天广汇通
# 解释一下 并行和并发的区别
'''
并行是指同一时刻,两个或者两个以上时间同时发生
并发 同一时间间隔,两个或两个以上时间同时发生
'''

# 如果一个程序需要进行大量IO操作,应当使用并行还是并发
'''
并发
'''

# 写一个装饰器
# 装饰器 被用于有切面需求,最为经典的是插入日志,性能测试,事物处理,装饰器是解决这类问题的绝佳设计
import time


def timeit(func):
    def wrapper(a):
        start = time.clock()
        func(1, 2)
        end = time.clock()
        print('used', end - start)
        print(a)

    return wrapper


# foo = timeit(foo) 完全等价
# 使用之后,foo函数就变了,相当于wrapper了
@timeit
def foo(a, b):
    pass
# 不带参数的装饰器
# wrapper将fn进行装饰,return wraper,返回的wraper就是装饰后的fn
