# coding: utf8


class NotifyFailed(Exception):
    """ 钉钉报警异常 """
    pass


class UploadFailed(Exception):
    """ 上传图片失败 """
    def __init__(self, url: str, reason: str = ''):
        self.url = url
        self.reason = reason

    def __repr__(self):
        text = f'[图片链接] {self.url}'
        if self.reason:
            text += f'\n[原因] {self.reason}'
        return text

    def __str__(self):
        return self.__repr__()
