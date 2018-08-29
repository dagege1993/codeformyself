from multiprocessing import Pool

time_list = [{"startTime": "2018-07-30 00:00:00", "endTime": "2018-07-30 23:59:59"},
             {"startTime": "2018-07-29 00:00:00", "endTime": "2018-07-29 23:59:59"},
             {"startTime": "2018-07-28 00:00:00", "endTime": "2018-07-28 23:59:59"},
             {"startTime": "2018-07-27 00:00:00", "endTime": "2018-07-27 23:59:59"},
             {"startTime": "2018-07-26 00:00:00", "endTime": "2018-07-26 23:59:59"}]


def uu(i):
	print(i)


# for i in time_list:
# print('当前的进程是%s' % i)


if __name__ == '__main__':
	p = Pool(10)
	p.map(uu, time_list)
	p.close()
	p.join()
