# coding: utf8

# Standard Library
import os
import time
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler as TRFHandler


class TimedRotatingFileHandler(TRFHandler):

    def __init__(self, filename: str, when: str = 'h', interval: int = 1,  # noqa
                 backupCount: int = 0, encoding: str = None,
                 delay: bool = False, utc: bool = False,
                 atTime: datetime = None) -> None:
        super().__init__(filename, when, interval, backupCount, encoding,
                         delay, utc, atTime)
        self.suffix = '%Y-%m-%d.log'  # type: str

    def doRollover(self) -> None:
        if self.stream:  # noqa
            self.stream.close()  # noqa
            self.stream = None
        currentTime = int(time.time())  # noqa
        dstNow = time.localtime(currentTime)[-1]  # noqa
        t = self.rolloverAt - self.interval  # noqa
        if self.utc:  # noqa
            timeTuple = time.gmtime(t)  # noqa
        else:
            timeTuple = time.localtime(t)  # noqa
            dstThen = timeTuple[-1]  # noqa
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)  # noqa
        dfn = self.rotation_filename(self.baseFilename[:-4] + "." +  # noqa
                                     time.strftime(self.suffix, timeTuple))
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:  # noqa
            for s in self.getFilesToDelete():  # noqa
                os.remove(s)
        if not self.delay:
            self.stream = self._open()  # noqa
        newRolloverAt = self.computeRollover(currentTime)  # noqa
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval  # noqa
        if ((self.when == 'MIDNIGHT' or self.when.startswith('W'))  # noqa
                and not self.utc):  # noqa
            dstAtRollover = time.localtime(newRolloverAt)[-1]  # noqa
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class Filter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.msg == "KeepAlive Timeout. Closing connection.":
            return False
        return True
