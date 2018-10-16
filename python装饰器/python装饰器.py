# python装饰器
'''
用于扩展原函数功能的一种函数
'''
# import time
#
#
# def deco(func):
# 	def wrapper(a, b):
# 		start_time = time.time()
# 		func(a, b)
# 		end_time = time.time()
# 		msecs = (end_time - start_time) * 1000
# 		print('time is %d' % msecs)
#
# 	return wrapper
#
#
# @deco  # 最原始的装饰器,它是一个函数,然后返回值也是一个函数.
# # 其中作为参数的这个函数func()就在返回函数wrapper()的内部执行.然后再函数func()前面加上@deco,
# # func()函数就相当于被注入了计时功能,现在只需要调用func(),它已经变身为新的功能更多的函数
#
# def func(a, b):
# 	print('hello ')
# 	time.sleep(1)
# 	print('result is %d' % (a + b))
#
#
# def deco(func):
# 	def wrapper(*args, **kwargs):
# 		start_time = time.time()
# 		func(*args, **kwargs)
# 		end_time = time.time()
# 		msecs = (end_time - start_time) * 1000
# 		print('time is %d' % msecs)
#
# 	return wrapper
#
#
# @deco
# def func(a, b):
# 	print("hello，here is a func for add :")
# 	time.sleep(1)
# 	print("result is %d" % (a + b))
#
#
# @deco
# def func2(a, b, c):
# 	print("hello，here is a func for add :")
# 	time.sleep(1)
# 	print("result is %d" % (a + b + c))
#
#
# if __name__ == '__main__':
# 	# f = func  # f被赋值为func,执行f()就是执行func()
# 	# f(3, 4)
#
# 	func2(3, 4, 5)
# 	func(3, 4)
import functools
import time

'''
import time


def deco01(func):
	def wrapper(*args, **kwargs):
		print('this is deco01')
		start_time = time.time()
		func(*args, **kwargs)
		end_time = time.time()
		msecs = (end_time - start_time) * 1000
		print('time is %d' % msecs)

	return wrapper


def deco02(func):
	def wrapper(*args, **kwargs):
		print('this is deco02')
		func(*args, **kwargs)
		print('deco02 end here')

	return wrapper


@deco01
@deco02
def func(a, b):
	print("hello，here is a func for add :")
	time.sleep(1)
	print("result is %d" % (a + b))


if __name__ == '__main__':
	f = func
	f(3, 4)

'''
'''
def dec1(func):
	print("dec1")

	def one():
		print("2222")
		func()
		print("3333")

	return one


def dec2(func):
	print("dec2")

	def two():
		print("bbbb")
		func()
		print("cccc")

	return two


@dec1
@dec2
def test():
	print("test test")


test()
'''


# 大部分涉及多个装饰器装饰的函数调用顺序时都会说明它们是自上而下的，比如下面这个例子:
# 最后一个装饰器开始，执行到第一个装饰器，再执行函数本身。
def decorator_a(func):
	print('Get in decorator_a')
	
	def inner_a(*args, **kwargs):
		print('Get in inner_a')
		return func(*args, **kwargs)
	
	return inner_a


def decorator_b(func):
	print('Get in decorator_b')
	
	def inner_b(*args, **kwargs):
		print('Get in inner_b')
		return func(*args, **kwargs)
	
	return inner_b


@decorator_b
@decorator_a
def f(x):
	print('Get in f')
	return x * 2


# f(1)

'''
def timing(status='Train'):
	print('this is timing')
	
	def dec(func):
		print('this is dec in timing')
		
		@functools.wraps(func)  # 加这句是为了防止装饰器对被装饰函数的影响
		def wrapper(*args, **kwargs):
			start = time.time()
			func1 = func(*args, **kwargs)
			print('[%s] time: %.3f s ' % (status, time.time() - start))
			return func1
		
		return wrapper
	
	return dec


@timing(status='Train')
def Training():
	time.sleep(3)


Training()
'''


def timing(status='Train'):
	print('this is timing')
	
	def dec(func):
		print('this is dec in timing')
		@functools.wraps(func)
		def wrapper3(*args, **kwargs):
			start = time.time()
			func1 = func(*args, **kwargs)
			print('[%s] time: %.3f s ' % (status, time.time() - start))
			return func1
		return wrapper3
	return dec


def dec1(func):
	print('this is dec1')
	@functools.wraps(func)
	def wrapper1(*args, **kwargs):
		print('this is a wrapper in dec1')
		return func(*args, **kwargs)
	return wrapper1


def dec2(func):
	print('this is dec2')
	@functools.wraps(func)
	def wrapper2(*args, **kwargs):
		print('this is a wrapper in dec2')
		return func(*args, **kwargs)
	return wrapper2


@dec1
@dec2
@timing(status='Test')
def fun():
	time.sleep(2)

fun()