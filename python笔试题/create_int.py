with open('bigdata_int.txt', 'a', encoding='utf-8') as f:
	for i in range(100000):
		f.write(str(i) + '\n')

with open('bigdata_int.txt', 'a', encoding='utf-8') as f:
	for i in range(10):
		f.write("192" + '\n')
