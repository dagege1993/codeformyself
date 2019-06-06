import os
import logging
import re
import imaplib
import email
import base64
import binascii

from sys import argv

import coloredlogs


LOGGER = logging.getLogger(__name__)
LEVEL_STYLE = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'}
}
coloredlogs.install(
    level='DEBUG', isatty=True, level_styles=LEVEL_STYLE,
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)
IMAP_SERVER = 'imap.mxhichina.com'
ROOT = './tmp'


class LoginError(Exception):
    pass


class FetchFailure(Exception):
    pass


class UnexpectedData(Exception):
    pass


def backup_email(user, password, root=ROOT, server=IMAP_SERVER, ssl=True):
    # 连接服务器并登陆
    if ssl:
        conn = imaplib.IMAP4_SSL(server)
    else:
        conn = imaplib.IMAP4(server)
    try:
        conn.login(user, password)
    except imaplib.IMAP4.error as exc:
        raise LoginError from exc
    LOGGER.debug('Login succeed')

    # 创建用户目录
    path = os.path.join(root, user)
    if not os.path.exists(path):
        os.mkdir(path)

    # 获得文件夹列表
    res, folders = conn.list()
    if res != 'OK':
        raise FetchFailure('List folders failed')

    # 遍历文件夹
    list_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    for folder in folders:
        '''
        匹配目录名称。
        folder中包含名称属性、层级分隔符、名称，后序用作命令如SELECT的参数时，名称必须是正确的；
        原始数据 b'(\\Trash) "/" "Trash"'，处理后的名称为Trash。
        '''
        folder_name = list_pattern.match(str(folder, encoding='utf-8')).group('name')
        # 创建相应文件夹目录
        f_path = os.path.join(
            path,
            folder_name.strip("\"").replace('&', '+').encode('utf-8').decode('utf-7')
        )
        if not os.path.exists(f_path):
            os.mkdir(f_path)
            LOGGER.info('Make dir: %s', f_path)

        # 选中文件夹
        res, data = conn.select(folder_name)
        if res != 'OK':
            LOGGER.error('Not found %s', folder_name)
            continue

        # 获得所有邮件
        res, msg_ids = conn.search(None, 'ALL')
        # conn.utf8_enabled时charset必须设为None，
        # 'ALL'查询参数
        # msg_ids列表中每个元素对应一个查询参数，每个元素为邮件序列号组成的字符串
        if res != 'OK':
            LOGGER.error('Search %s failed', folder_name)
            continue

        if len(msg_ids) != 1:
            raise UnexpectedData(
                f'Length of msg_ids({msg_ids}) is expected to be one'
            )

        msg_ids = msg_ids[0].split(b' ')
        # 遍历邮件id，获取内容
        for msg_id in msg_ids:
            if not msg_id:
                continue

            # 通过邮件id获取邮件内容
            try:
                res, msg_data = conn.fetch(message_set=msg_id, message_parts='(RFC822)')
            except imaplib.IMAP4.abort as exc:
                raise FetchFailure(f'{exc}({folder_name} {msg_id})')
            # RFC822: 功能上等同于BODY[]。返回邮件体文本格式和大小的摘要信息。
            # IMAP客户机可以识别这些信息，并向用户显示详细的关于邮件的信息。
            # msg_data为[('(message_parts)', 'message_data'), ')']格式
            if res != 'OK':
                LOGGER.error('Fetch %s %s failed', folder_name, msg_id)
                continue
            data = msg_data[0]
            if not isinstance(data, tuple):
                continue
            if len(data) != 2:
                LOGGER.error('Unexpected msg data: %s', data)
                continue
            msg = data[1]

            # 存储邮件正文
            msg_path = os.path.join(f_path, msg_id.decode('utf-8'))
            if not os.path.exists(msg_path):
                os.mkdir(msg_path)
            filename = os.path.join(msg_path, 'body.eml')
            with open(filename, 'wb') as f:
                f.write(msg)
            LOGGER.info('Stored %s', filename)

            # 解析邮件，存储附件
            parsed_msg = email.message_from_bytes(msg)
            for part in parsed_msg.walk():
                name = part.get_filename()
                if not name:
                    continue
                if part.get('Content-Type') == 'application/octet-stream':
                    try:
                        name = base64.b64decode(name.replace('=?UTF-8?B?', ''))\
                            .decode('utf-8')
                    except (binascii.Error, UnicodeDecodeError) as exc:
                        LOGGER.error('%s: %s/%s', exc, msg_id.decode('utf-8'), name)
                        continue
                    except Exception as exc:
                        LOGGER.error('', exc_info=True)
                        continue
                attachment_name = os.path.join(msg_path, f'attachment-{name}')
                with open(attachment_name, 'wb') as attachment:
                    attachment.write(part.get_payload(decode=True))
                    # decode=True：会对Content-Transfer-Encoding为base64的part解码
                LOGGER.info('Stored %s', attachment_name)

    conn.close()


if __name__ == '__main__':
    try:
        backup_email(argv[1], argv[2])
    except IndexError:
        LOGGER.warning('Please provide username and password!')
    except (LoginError, FetchFailure, UnexpectedData) as exc:
        LOGGER.error('%s: %s' % (exc, argv[1]))
    except Exception as exc:
        LOGGER.critical('', exc_info=True)
