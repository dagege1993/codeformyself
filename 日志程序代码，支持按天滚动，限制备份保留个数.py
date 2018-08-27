import logging
import time

from logging.handlers import TimedRotatingFileHandler

# ----------------------------------------------------------------------
if __name__ == "__main__":
	logFilePath = "test.log"
	logger = logging.getLogger("YouLoggerName")
	# getLogger = Return a logger with the specified name, creating it if necessary.
	# If no name is specified, return the root logger. 创建一个logger
	
	logger.setLevel(logging.INFO)
	
	handler = TimedRotatingFileHandler(logFilePath, when="m", interval=1, backupCount=7)
	
	# TimedRotatingFileHandler这个模块是满足文件名按时间自动更换的需求，这样就可以保证日志单个文件不会太大。
	# backupCount 是保留日志个数。默认的0是不会自动删除掉日志。若设10，则在文件的创建过程中库会判断是否有超过这个10，若超过，则会从最先创建的开始删除。
	# interval 是指等待多少个单位when的时间后，Logger会自动重建文件
	# 参数when决定了时间间隔的类型，参数interval决定了多少的时间间隔。如when=‘D’，interval=2，就是指两天的时间间隔，backupCount决定了能留几个日志文件。超过数量就会丢弃掉老的日志文件。
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	
	handler.setFormatter(formatter)
	
	logger.addHandler(handler)
	
	for i in range(1000000):
		logger.info("This is a test!%s", i)
		time.sleep(61)
