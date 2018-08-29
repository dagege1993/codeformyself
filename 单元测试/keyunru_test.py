import unittest

# 单元测试代码要非常简单，如果测试代码太复杂，那么测试代码本身就可能有bug。
from 单元测试.keruyun import send_mq, main


class TestDict(unittest.TestCase):  # 需要编写一个测试类，从unittest.TestCase继承。
	def test_init(self):  # 以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。
		self.assertEqual(send_mq("测试数据111"), 1)
	
	# def test_main(self):  # 以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。
	# 	self.assertEqual(main(), 1)


if __name__ == '__main__':
	unittest.main()
