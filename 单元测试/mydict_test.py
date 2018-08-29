import unittest

from 单元测试.mydict import Dict


# 单元测试代码要非常简单，如果测试代码太复杂，那么测试代码本身就可能有bug。

class TestDict(unittest.TestCase):  # 需要编写一个测试类，从unittest.TestCase继承。
	
	def test_init(self):  # 以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行。
		d = Dict(a=1, b='test')
		self.assertEqual(d.a, 1)
		self.assertEqual(d.b, 'test')
		self.assertTrue(isinstance(d, dict))
	
	def test_key(self):
		d = Dict()
		d['key'] = 'value'
		self.assertEqual(d.key, 'value')  # 最常用的断言就是assertEqual()：
	
	def test_attr(self):
		d = Dict()
		d.key = 'value'
		self.assertTrue('key' in d)
		self.assertEqual(d['key'], 'value')
	
	def test_keyerror(self):
		d = Dict()
		with self.assertRaises(KeyError):  # 另一种重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError：
			value = d['empty']
	
	def test_attrerror(self):
		d = Dict()
		with self.assertRaises(AttributeError):
			value = d.empty


if __name__ == '__main__':
	unittest.main()
