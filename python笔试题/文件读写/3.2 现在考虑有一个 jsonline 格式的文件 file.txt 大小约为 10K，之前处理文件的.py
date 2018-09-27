'''

def get_lines():
	l = []
	
	with open('file.txt', 'rb') as f:
		for eachline in f:
			l.append(eachline)
		return l


if __name__ == '__main__':
	for e in get_lines():
		# process(e)  # 处理每一行数据
# 现在要处理一个大小为 10G 的文件，但是内存只有 4G，如果在只修改 get_lines 函数而其他代
# 码保持不变的情况下，应该如何实现？需要考虑的问题都有哪些？

# 把return l  改为yeild  l 就行

要考虑的问题,内存无法一次读入10G,需要分批次读取,
分批次读取数据的大小,太小就会读取操作浪费太多时间
'''

'''
read  读取整个文件
readline 读取下一行,使用生成器方法
readlines 读取整个文件到一个迭代器供遍历

'''


def print_directory_contents(sPath):
	"""
	3． 这个函数接收文件夹的名称作为输入参数
	4． 返回该文件夹中文件的路径
	5． 以及其包含文件夹中文件的路径
	6． """
	# 补充代码
	# ------------代码如下--------------------
	import os
	
	for sChild in os.listdir(sPath):  # os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
		sChildPath = os.path.join(sPath, sChild)  # 组合成新目录,
		print(sChildPath)
	if os.path.isdir(sChildPath):  # os.path.isdir()函数判断某一路径是否为目录
		print_directory_contents(sChildPath)
	# print(sChildPath)
	else:
		print('1', sChildPath)


print_directory_contents(r'C:\Users\Administrator.DESKTOP-5D2UUSC\Desktop\自己积累的代码')
