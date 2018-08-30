# -*- coding: utf-8 -*-
import time
from multiprocessing import Pool


def run(fn):
	# fn: 函数参数是数据列表的一个元素
	time.sleep(1)
	
	print(fn)


if __name__ == "__main__":
	testFL = [{"startTime": "2018-07-30 00:00:00", "endTime": "2018-07-30 23:59:59"},
	          {"startTime": "2018-07-29 00:00:00", "endTime": "2018-07-29 23:59:59"},
	          {"startTime": "2018-07-28 00:00:00", "endTime": "2018-07-28 23:59:59"},
	          {"startTime": "2018-07-27 00:00:00", "endTime": "2018-07-27 23:59:59"},
	          {"startTime": "2018-07-26 00:00:00", "endTime": "2018-07-26 23:59:59"}]
	print('shunxu:')  # 顺序执行(也就是串行执行，单进程)
	s = time.time()
	for fn in testFL:
		run(fn)
	t1 = time.time()
	print("顺序执行时间：", int(t1 - s))
	
	print('concurrent:')  # 创建多个进程，并行执行
	s1 = time.time()
	pool = Pool(10)  # 创建拥有10个进程数量的进程池
	# testFL:要处理的数据列表，run：处理testFL列表中数据的函数
	pool.map(run, testFL)  # 将“FUNC”应用于“迭代”中的每个元素，收集结果在返回的列表中。
	pool.close()  # 关闭进程池，不再接受新的进程
	pool.join()  # 主进程阻塞等待子进程的退出
	t2 = time.time()
	print("并行执行时间：", int(t2 - s1))
