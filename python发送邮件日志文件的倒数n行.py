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


# a = tail(r'C:\Users\admin\Desktop\command.log', 1000, False)


def sed_email():
	import smtplib
	# smtplib这个模块是管发邮件
	from email.mime.text import MIMEText
	# 构造邮件内容
	from email.mime.multipart import MIMEMultipart
	
	# 发带附件的邮件用的
	email_host = 'smtp.163.com'  # 邮箱服务器地址
	email_user = '18273711329@163.com'  # 发送者账号
	email_pwd = 'hlz156350'
	# 发送者密码是邮箱的授权码，不是登录的密码
	# mail_list = '156350439@qq.com'
	mail_list = '18073258146@163.com'
	# 收件人邮箱，多个账号的话，用逗号隔开
	new_msg = MIMEMultipart()
	# 构建了一个能发附件的邮件对象
	new_msg.attach(MIMEText('日志发送模块'))
	# 邮件内容
	new_msg['Subject'] = 'Python测试邮件带附件'  # 邮件主题
	new_msg['From'] = email_user  # 发送者账号
	new_msg['To'] = mail_list  # 接收者账号列表
	att = MIMEText(tail('/home/spider/hlz/duolabao_console.log', 1000, False))
	att["Content-Type"] = 'application/octet-stream'
	att["Content-Disposition"] = 'attachment; filename="log.txt"'
	new_msg.attach(att)
	smtp = smtplib.SMTP(email_host, port=25)  # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
	smtp.ehlo()
	smtp.starttls()
	smtp.login(email_user, email_pwd)  # 发送者的邮箱账号，密码
	smtp.sendmail(email_user, mail_list, new_msg.as_string())
	# 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
	smtp.quit()  # 发送完毕后退出 smtp
	print('email send success.')


if __name__ == '__main__':
	sed_email()
