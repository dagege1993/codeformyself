# coding: utf8
"""
Created by songww
"""

import base64
import logging

from typing import Dict, Any

from lxml import etree
from celery.exceptions import Ignore

from tasks.errors.parse_error import ParserNotFound

__all__ = [
    'OrderParser', 'HotelOrderParser', 'FlightOrderParser', 'RestOrderParser',
    'Parser'
]
_ORDER_PARSERS = set()


class OrderParserMetaclass(type):

    """Meta class for order parsers
    """

    def __new__(mcs, name, bases, attrs):
        abstract_parser = [
            'OrderParser', 'HotelOrderParser', 'FlightOrderParser',
            'RestOrderParser'
        ]
        new_class = super().__new__(mcs, name, bases, attrs)
        if name not in abstract_parser:
            _ORDER_PARSERS.add(new_class)
        return new_class


class OrderParser(object, metaclass=OrderParserMetaclass):  # noqa pylint: disable=R0902

    """Base parser
    """

    def __init__(self, html: str, message_id: str, headers: dict,
                 received_time: str, email: str, uid: str, subject: str,
                 sender: str, snippet: str) -> None:
        self._html = html
        self._message_id = message_id
        self._headers = headers
        self._uid = uid
        self._email = email
        self._etree = etree.HTML(self._html)  # noqa pylint: disable=E1101
        self.logger = logging.getLogger(self.__class__.__name__)
        self.received_time = received_time
        self._order = OrderResult({
            'category': 'hotel',
            'received_time': self.received_time,
            'message_id': message_id,
            'email': email,
            'uid': uid
        })  # type: OrderResult
        self.logger.info('%s', self._order)

    def _parse(self) -> bool:
        """do parse"""
        raise NotImplementedError()

    def parse(self) -> bool:
        """do parse"""
        return self._parse()

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        """validate if can be parsed"""
        raise NotImplementedError()

    def to_dict(self) -> dict:
        """dump to dict"""
        return dict(self._order)

    def to_json(self) -> str:
        """dump to json"""
        try:
            import ujson as json
        except ImportError:
            import json  # noqa
        return json.dumps(self.to_dict())


def _decode_body(message: Dict[str, Any]) -> str:
    """Base64decode for gmail message
    """

    data = []
    logger = logging.getLogger(__name__)

    if message['payload']['mimeType'].startswith('multipart'):
        for part in message['payload']['parts']:
            if part['body']['size'] == 0:
                for subpart in part['parts']:
                    data.append(base64_decode(subpart['body']['data']))
            else:
                data.append(base64_decode(part['body']['data']))
    elif 'data' in message['payload']['body']:
        data.append(base64_decode(message['payload']['body']['data']))
    else:
        logger.error('Data not found, %s', message['id'])
        raise Ignore(None)

    return ''.join(data)


def base64_decode(encoded: bytes) -> str:
    """base64 decode
    """
    return base64.urlsafe_b64decode(encoded) \
        .decode('utf8', 'ignore') \
        .strip()


def select_parser(message: Dict[str, Any], email: str,
                  uid: str) -> OrderParser:
    """choice parser"""

    headers = message['payload']['headers']
    message_id = message['id']
    received_at = message.get('internalDate')

    snippet = message.get('snippet')

    for header in headers:
        if header['name'] == 'From':
            sender = header['value'].strip()
        if header['name'] == 'Subject':
            subject = header['value'].strip()

    for parser_class in _ORDER_PARSERS:
        if parser_class.validate(sender, subject, snippet):
            decoded_body = _decode_body(message)
            return parser_class(
                html=decoded_body,
                message_id=message_id,
                headers=headers,
                received_time=received_at,
                email=email,
                uid=uid,
                subject=subject,
                sender=sender,
                snippet=snippet
            )

    raise ParserNotFound(message_id, sender, subject, snippet)


Parser = select_parser  # pylint: disable=C0103


class FlightOrderParser(OrderParser):  # pylint: disable=W0223

    """flight"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order['category'] = 'flight'


class RestOrderParser(OrderParser):  # pylint: disable=W0223

    """Restarant
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order['category'] = 'restaurant'


HotelOrderParser = OrderParser


class OrderResult(dict):

    def set(self, key, value, skip=True):
        if skip:
            if not value:
                return
        self[key] = value
        return value
