# 写python程序时，经常碰到如：发送邮件、配置账号信息。难免需要在python程序中明文填写敏感信息，这个时候可以将敏感信息写入系统环境变量，通过python自带os模块去获取变量。


# Linux下：

# root@KaKa:~# export USERNAME=cctv
# root@KaKa:~#
# root@KaKa:~# python
# Python 2.7.3 (default, Mar 14 2014, 11:57:14)
# [GCC 4.7.2] on linux2
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import os
# >>> USERNAME = os.environ.get(‘USERNAME‘)
# >>> USERNAME
# ‘cctv‘


# Windows下：
#
# (env) F:\PythonClass>set USERNAME=CCTV
# (env) F:\PythonClass>python
# Python 2.7.10 (default, May 23 2015, 09:44:00) [MSC v.1500 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import os
# >>> use = os.environ.get(‘USERNAME‘)
# >>> use
# ‘CCTV‘
#
#
# 如上，使用os.environ.get(‘需要获取的变量名‘)方法就可以获取你想要的变量值。这样写程序就可以不用担心敏感信息泄露了。


# 信息太多还是弄个脚本比较好, 试试脚本

