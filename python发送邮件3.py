import time


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
	att = MIMEText(open('requirements.txt').read())
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


SECOND_DAY = 24 * 60 * 60


def delta_seconds():
	from datetime import datetime
	cur_time = datetime.now()
	des_time = cur_time.replace(hour=9, minute=20, second=0, microsecond=0)
	# 这里添加时间 replace()= Return a new datetime with new values for the specified fields.返回一个替换指定日期字段的新date对象
	delta = des_time - cur_time
	skip_seconds = delta.total_seconds() % SECOND_DAY  # total_seconds()是获取两个时间之间的总差
	print("Must sleep %d seconds" % skip_seconds)
	return skip_seconds


while True:
	s = delta_seconds()
	time.sleep(s)
	print("work it!")  # 这里可以替换成作业
	sed_email()
