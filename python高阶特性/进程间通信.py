from multiprocessing import Process, Queue
import os, time, random


# 写数据进程执行的代码
def write(q):
    print('Process to write %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)


# 读数据进程执行的代码
def read(q):
    print('Process to read:%s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


if __name__ == '__main__':
    # 父进程创建Queue,并且传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程Pw,写入
    pw.start()
    # 启动子进程pr读取
    pr.start()
    # 等待
    pw.join()
