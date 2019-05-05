import logging
from datetime import datetime


class Config():
    # 创建一个logger
    logger = logging.getLogger('statisticNew')
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.ERROR)

    # 创建一个handler，用于写入日志文件
    today = datetime.now()
    log_file_path = "logs/{}-{}-{}-{}.log".format(today.year, today.month, today.day, today.hour)
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    def getLog(self):
        return self.logger
