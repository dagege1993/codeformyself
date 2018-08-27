# multiprocessing支持子进程、通信和共享数据、执行不同形式的同步，提供了Process、Queue、Pipe、Lock等组件。


# #process 类基本使用
# import multiprocessing
#
#
# def process(num):
# 	print('Process:', num)
#
#
# if __name__ == '__main__':
# 	for i in range(5):
# 		p = multiprocessing.Process(target=process, args=(i,))
# 		p.start()


# #通过 cpu_count() 方法还有 active_children() 方法获取当前机器的 CPU 核心数量以及得到目前所有的运行的进程。
# import multiprocessing
# import time
#
#
# def process(num):
# 	time.sleep(num)
# 	print('Process:', num)
#
#
# if __name__ == '__main__':
# 	for i in range(5):
# 		p = multiprocessing.Process(target=process, args=(i,))
# 		p.start()
#
# 	print('CPU number:' + str(multiprocessing.cpu_count()))  # cpu_count()  获取当前机器的 CPU 核心数量
# 	for p in multiprocessing.active_children():  # active_children() 得到目前所有的运行的进程。
# 		print('Child process name: ' + p.name + ' id: ' + str(p.pid))
#
# 	print('Process Ended')

# #deamon
# #在这里介绍一个属性，叫做deamon。每个线程都可以单独设置它的属性，如果设置为True，当父进程结束后，子进程会自动被终止。


# from multiprocessing import Process
# import time
#
#
# class MyProcess(Process):
# 	def __init__(self, loop):
# 		Process.__init__(self)
# 		self.loop = loop
#
# 	def run(self):
# 		for count in range(self.loop):
# 			time.sleep(1)
# 			print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))
#
#
# if __name__ == '__main__':
# 	for i in range(2, 5):
# 		p = MyProcess(i)
# 		p.daemon = True
# 		p.start()
#
# 	print('Main process Ended!')


# # join() 这样父进程（主进程）就会等待子进程执行完毕。
# from multiprocessing import Process
# import time
#
#
# class MyProcess(Process):
# 	def __init__(self, loop):
# 		Process.__init__(self)
# 		self.loop = loop
#
# 	def run(self):
# 		for count in range(self.loop):
# 			time.sleep(1)
# 			print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))
#
#
# if __name__ == '__main__':
# 	for i in range(2, 5):
# 		p = MyProcess(i)
# 		p.daemon = True
# 		p.start()
# 		p.join()
#
# 	print('Main process Ended!')


from multiprocessing import Process, Semaphore, Lock, Queue
import time
from random import random

buffer = Queue(10)
empty = Semaphore(2)
full = Semaphore(0)
lock = Lock()


class Consumer(Process):
	
	def run(self):
		global buffer, empty, full, lock
		while True:
			full.acquire()
			lock.acquire()
			print('Consumer get', buffer.get())
			time.sleep(1)
			lock.release()
			empty.release()


class Producer(Process):
	def run(self):
		global buffer, empty, full, lock
		while True:
			empty.acquire()
			lock.acquire()
			num = random()
			print('Producer put ', num)
			buffer.put(num)
			time.sleep(1)
			lock.release()
			full.release()


if __name__ == '__main__':
	p = Producer()
	c = Consumer()
	p.daemon = c.daemon = True
	p.start()
	c.start()
	p.join()
	c.join()
	print('Ended!')
