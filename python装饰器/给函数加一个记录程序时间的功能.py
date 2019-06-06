import time


def time_it(method):
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        time.sleep(1)
        end_time = time.time()
        print("自己测试的方法")
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, end_time - start_time))
        return result

    return timed


@time_it
def fast():
    print(1)
    # pass


fast()


# import datetime
#
#
# def count_time(func):
#     def int_time(*args, **kwargs):
#         start_time = datetime.datetime.now()  # 程序开始时间
#         func()
#         over_time = datetime.datetime.now()  # 程序结束时间
#         total_time = (over_time - start_time).total_seconds()
#         print('程序共计%s秒' % total_time)
#
#     return int_time
#
#
# @count_time
# def main():
#     print('>>>>开始计算函数运行时间')
#     for i in range(1, 1000):
#         for j in range(i):
#             print(j)
#
#
# if __name__ == '__main__':
#     main()


def quick_sort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [i for i in array[1:] if i < pivot]
        greater = [j for j in array[1:] if j > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)


print(quick_sort([5, 2, 6, 9, 3]))
