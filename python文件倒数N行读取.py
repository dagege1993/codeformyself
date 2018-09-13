def tail(file, taillines=500, return_str=True, avg_line_length=None):
	"""avg_line_length:每行字符平均数,
	return_str:返回类型，默认为字符串，False为列表。
	offset:每次循环相对文件末尾指针偏移数"""
	with open(file, errors='ignore') as f:
		if not avg_line_length:
			f.seek(0, 2)
			f.seek(f.tell() - 3000)
			avg_line_length = int(3000 / len(f.readlines())) + 10
		f.seek(0, 2)
		end_pointer = f.tell()
		offset = taillines * avg_line_length
		if offset > end_pointer:
			f.seek(0, 0)
			lines = f.readlines()[-taillines:]
			return "".join(lines) if return_str else lines
		offset_init = offset
		i = 1
		while len(f.readlines()) < taillines:
			location = f.tell() - offset
			f.seek(location)
			i += 1
			offset = i * offset_init
			if f.tell() - offset < 0:
				f.seek(0, 0)
				break
		else:
			f.seek(end_pointer - offset)
		lines = f.readlines()
		if len(lines) >= taillines:
			lines = lines[-taillines:]
		
		return "".join(lines) if return_str else lines


a = tail(r'C:\Users\Administrator.DESKTOP-5D2UUSC\Desktop\duolabao_console.log', 1000, True)
print(a)
