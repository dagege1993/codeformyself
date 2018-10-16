# 生成一个斐波那契数列
# []列表实现
def fibonacci(num):
	fibs = [0, 1]
	for i in range(num - 2):
		fibs.append(fibs[-2] + fibs[-1])  # 倒数第二个+倒数第一个数的结果，追加到列表
	print(fibs)


fibonacci(5)


# def fibonacci(num):
# 	fibs = [0, 1]
# 	for i in range(num - 2):
# 		fibs.append(fibs[-2] + fibs[-1])
# 		print(fibs)


# fibonacci(5)
