# coding: utf8

import json
import logging
import requests
import smtplib
import imghdr
import os

from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import List

from tasks.errors import NotifyFailed


class Notifier:
    """ 通知者

    Attributes:
        req: 如果通过http请求，则为ClientSession实例，否则为传入的inject_client
        _logger: 日志对象
    """

    def __init__(self, overhttp=True, inject_client=None):
        if overhttp:
            self.req = requests.session()
        elif inject_client:
            self.req = inject_client
        clsname = ".".join(
            [self.__class__.__module__, self.__class__.__qualname__]
        )
        self._logger = logging.getLogger(clsname)

    def send(self, message, receiver):
        """ 发送通知

        Args:
            message: 消息对象
            receiver: 接收者

        Raises:
            NotImplementedError: 不执行
        """

        raise NotImplementedError()


class DingtalkMessage:
    """ 钉钉消息

    Attributes:
        type: 消息类型
        title: 首屏会话透出的展示内容
        text: 消息内容
        at_mobiles：被@人的手机号
        is_at_all: 是否@所有人
    """

    def __init__(
        self,
        msgtype: str = "markdown",
        title: str = "",
        text: str = "",
        at_mobiles: List = None,
        is_at_all: bool = False,
    ):
        self.type = msgtype
        self.title = title
        self.text = text
        if at_mobiles is None:
            self.at_mobiles = []
        else:
            self.at_mobiles = at_mobiles
        self.is_at_all = is_at_all

    @property
    def format(self):
        """ 格式化消息

        Returns:
            可发送的格式化消息

        Raises:
            ValueError: msgtype不合法
        """

        if self.type == "markdown":
            return {
                "msgtype": self.type,
                "markdown": {"title": self.title, "text": self.text},
                "at": {
                    "atMobiles": self.at_mobiles,  # 在text内容里要有@手机号
                    "isAtAll": self.is_at_all,
                },
            }

        raise ValueError(f"{self.type} is not valid message type")


class DingtalkNotifier(Notifier):
    """ 钉钉机器人 """

    def send(self, message: DingtalkMessage, receiver: str):
        """ 发送通知

        Args:
            message: 消息对象
            receiver: 钉钉机器人token

        Returns::
            钉钉返回的响应
        """
        try:
            resp = self.req.post(
                "https://oapi.dingtalk.com/robot/send",
                params={"access_token": receiver},
                json=message.format,
            )
            status = resp.status_code
            text = resp.text
        except Exception as exc:
            raise NotifyFailed(f"Payload: {message.format}") from exc
        if status != 200:
            raise NotifyFailed(
                f"Reason: <{status}>{text}\n " f"Payload: {message.format}"
            )
        try:
            body = json.loads(text)
            if body.get("errcode") != 0:
                raise NotifyFailed(
                    f"Reason: {text}\n " f"Payload: {message.format}"
                )
        except ValueError:
            raise NotifyFailed(
                f"Reason: {text}\n " f"Payload: {message.format}"
            )
        return {"status": status, "body": text}


class EmailNotifier(Notifier):
    """ 邮件通知 """

    def __init__(self, host, port, user, password):
        super().__init__(False)

        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def format_attach_message(
        self, subject: str, file_path: str, receiver: str, from_addr: str, preamble=""
    ):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = receiver
        msg.preamble = preamble

        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(file_path, "rb").read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(file_path)}"',
        )
        msg.attach(part)

        return msg

    def send(self, message: any):
        with smtplib.SMTP_SSL(host=self.host, port=self.port) as s:
            s.ehlo()
            s.login(self.user, self.password)
            s.sendmail(
                message["From"], message["To"].split(","), message.as_string()
            )
