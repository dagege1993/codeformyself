# 海量日志数据,提取出某日访问次数最多的IP


from collections import Counter

if __name__ == '__main__':
	ip_list = ["192.168.1.2", "192.168.1.3", "192.168.1.3", "192.168.1.4", "192.168.1.2"]
	ip_counter = Counter(ip_list)  # python内置计数函数,进行统计
	print(ip_counter.most_common()[0][0])  # most_common([n])：返回最常用的元素及其计数的列表。默认返回所有元素。

# 采取大而化小的做法。
#    假设海量的数据的大小是100G，我们的可用内存是1G.我们可以把数据分成1000份（这里只要大于100都是可以的），每次内存读入100M
#    再去处理。但是问题的关键是怎么将这100G数据分成1000分呢。这里我们以前学过的hash函数就派上用场了。
#    Hash函数的定义：对于输入的字符串，返回一个固定长度的整数，hash函数的巧妙之处在于对于相同的字符串，那么经过hash计算，
#    得出来的结果肯定是相同的，不同的值，经过hash，结果可能相同（这种可能性一般都很小）或者不同。那么有了hash函数，
#    那么这道题就豁然开朗了，思路如下：
#    1.对于海量数据中的每一个ip，使用hash函数计算hash(ip)%1000,输出到1000个文件中
#    2.对于这1000个文件，分别找出出现最多的ip。这里就可以用上面提到的Counter类的most_common()方法了（这里方法很多，不一一列举）
#    3.使用外部排序，对找出来的1000个ip在进行排序。（这里数据量小，神马排序方法都行，影响不大）
import os
import heapq
import operator
from collections import Counter

source_file = 'bigdata.txt'  # 原始的海量数据ip
temp_files = 'temp/'  # 把经过hash映射过后的数据存到相应的文件中
top_1000ip = []  # 存放1000个文件的出现频率最高的ip和出现的次数


def hash_file():
	"""
	 this function is map a query to a new file
	"""
	temp_path_list = []
	if not os.path.exists(temp_files):
		os.makedirs(temp_files)
	for i in range(0, 1000):
		temp_path_list.append(open(temp_files + str(i) + '.txt', mode='w'))
	with open(source_file) as f:
		for line in f:
			temp_path_list[hash(str(line)) % 1000].write(line)  # %返回除法的余数
	# hash() 用于获取取一个对象（字符串或者数值等）的哈希值
	# hash()函数可以应用于数字、字符串和对象，不能直接应用于 list、set、dictionary
	# print hash(line)%1000
	# print(line)
	for i in range(1000):
		temp_path_list[i].close()


def cal_query_frequency():
	for root, dirs, files in os.walk(temp_files):
		# os.walk 便利文件夹地址,返回返回的是一个三元组(root,dirs,files)。
		# root 所指的是当前正在遍历的这个文件夹的本身的地址
		# dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
		# files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
		for file in files:
			real_path = os.path.join(root, file)
			ip_list = []
			with open(real_path) as f:
				for line in f:
					ip_list.append(line.replace('\n', ''))
			try:
				top_1000ip.append(Counter(ip_list).most_common()[0])
			except:
				pass


# print(top_1000ip)


def get_ip():
	return (sorted(top_1000ip, key=lambda a: a[1], reverse=True)[0])[0]


if __name__ == '__main__':
	hash_file()
	cal_query_frequency()
	print(get_ip())
	
	# 假如a是一个由元组构成的列表，这时候就麻烦了，我们需要用到参数key，也就是关键词，看下面这句命令，
	# lambda是一个隐函数，是固定写法，不要写成别的单词；x表示列表中的一个元素，在这里，表示一个元组，x只是临时起的一个名字，你可以使用任意的名字；
	# x[0]表示元组里的第一个元素，当然第二个元素就是x[1]；所以这句命令的意思就是按照列表中第一个元素排序
	a = [('a', 4), ('b', 3), ('c', 2), ('d', 1), ]
	print(sorted(a, key=lambda x: x[0]))
	# 按照第二个元素排序：
	print(sorted(a, key=lambda x: x[1]))
#
