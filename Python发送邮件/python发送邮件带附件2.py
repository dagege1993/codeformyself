# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.header import Header
# from email.utils import parseaddr, formataddr
#
#
# def _format_addr(s):
# 	name, addr = parseaddr(s)
# 	return formataddr((Header(name, 'utf-8').encode(), addr))
#
#
# # 邮件对象:
# msg = MIMEMultipart()
# msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
# msg['To'] = _format_addr('管理员 <%s>' % to_addr)
# msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
#
# # 邮件正文是MIMEText:
# msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
#
# # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
# with open('/Users/michael/Downloads/test.png', 'rb') as f:
# 	# 设置附件的MIME和文件名，这里是png类型:
# 	mime = MIMEBase('image', 'png', filename='test.png')
# 	# 加上必要的头信息:
# 	mime.add_header('Content-Disposition', 'attachment', filename='test.png')
# 	mime.add_header('Content-ID', '<0>')
# 	mime.add_header('X-Attachment-Id', '0')
# 	# 把附件的内容读进来:
# 	mime.set_payload(f.read())
# 	# 用Base64编码:
# 	encoders.encode_base64(mime)
# 	# 添加到MIMEMultipart:
# 	msg.attach(mime)


# from email.mime.text import MIMEText
#
# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
#
# # 输入Email地址和口令:
# from_addr = input('From: ')
# password = input('Password: ')
# # 输入收件人地址:
# to_addr = input('To: ')
# # 输入SMTP服务器地址:
# smtp_server = input('SMTP server: ')
#
# import smtplib
#
# server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
# server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'from@runoob.com'
receivers = ['156350439@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')  # 发送者
message['To'] = Header("测试", 'utf-8')  # 接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(sender, receivers, message.as_string())
	print("邮件发送成功")
except smtplib.SMTPException:
	print("Error: 无法发送邮件")
