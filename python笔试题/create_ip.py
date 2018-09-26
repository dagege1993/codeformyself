# ["192.168.1.2", "192.168.1.3", "192.168.1.3", "192.168.1.4", "192.168.1.2"]

with open('bigdata.txt', 'a', encoding='utf-8') as f:
	for i in range(100000):
		f.write("192.168.1." + str(i) + '\n')

with open('bigdata.txt', 'a', encoding='utf-8') as f:
	for i in range(10):
		f.write("192.168.1.1")
