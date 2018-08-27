INSERT_NUMS = 0  # 给全局变量赋值


def insert_time():
	for i in range(1, 10):
		global INSERT_NUMS
		INSERT_NUMS += 1
	print(INSERT_NUMS)
	return INSERT_NUMS


if __name__ == '__main__':
	print(INSERT_NUMS)
	time = insert_time()
