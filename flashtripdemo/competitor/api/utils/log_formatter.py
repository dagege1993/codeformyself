'''
This library is provided to allow standard python logging
to output log data as JSON formatted strings
'''
# Standard Library
import os
import json
import time
import logging
import datetime
import traceback
from inspect import istraceback

try:
    from collections import OrderedDict
except ImportError:
    pass

# skip natural LogRecord attributes
# http://docs.python.org/library/logging.html#logrecord-attributes
RESERVED_ATTRS = (
    'args',
    'asctime',
    'created',
    'exc_info',
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName'
)

RESERVED_ATTR_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))


def merge_extra(record, target, reserved=RESERVED_ATTR_HASH):
    """
    Merges extra attributes from LogRecord object into target dictionary
    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.__dict__.items():
        # this allows to have numeric keys
        if (key not in reserved
            and not (hasattr(key, "startswith")
                     and key.startswith('_'))):
            target[key] = value
    return target


class JsonFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as json strings.
    extra values will be formatted as str() if nor supported by
    json default encoder
    """
    tz_beijing = datetime.timezone(
        datetime.timedelta(hours=8),
        'Asia/Beijing'
    )

    def __init__(self, *args, **kwargs):
        """
        :param default: a function for encoding non-standard objects
            as outlined in http://docs.python.org/2/library/json.html
        :param encoder: optional custom encoder
        :param serializer: a :meth:`json.dumps`-compatible callable
            that will be used to serialize the log record.
        :param prefix: an optional string prefix added at the beginning of
            the formatted string
        """
        self.prefix = kwargs.pop("prefix", "")
        self.indent = kwargs.pop("indent", None)
        self.default = kwargs.pop("default", None)
        self.encoder = kwargs.pop("encoder", None)
        self.serializer = kwargs.pop("serializer", json.dumps)

        super().__init__(*args, **kwargs)

        os.putenv('TZ', 'Asia/Shanghai')
        time.tzset()

        if not self.encoder and not self.default:
            def _default_handler(obj):
                '''Prints dates in ISO format'''
                datetimes = (datetime.date, datetime.time, datetime.datetime)
                if isinstance(obj, datetimes):
                    return obj.astimezone(self.tz_beijing) \
                        .strftime(self.datefmt)
                elif istraceback(obj):
                    tb = ''.join(traceback.format_tb(obj))
                    return tb.strip()
                elif isinstance(obj, Exception):
                    return "Exception: %s" % str(obj)
                return str(obj)
            self.default = _default_handler
        self._required_fields = self.parse()
        self._skip_fields = dict(
            zip(
                self._required_fields,
                self._required_fields
            )
        )
        self._skip_fields.update(RESERVED_ATTR_HASH)

    def parse(self):
        """
        Parses format string looking for substitutions
        This method is responsible for returning a list of fields (as strings)
        to include in all log messages.
        """
        return [key.strip() for key in self._fmt.split(',')]

    def add_fields(self, log_record, record, message_dict):
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)

        if self.prefix:
            log_record['prefix'] = self.prefix
        log_record.update(message_dict)
        merge_extra(record, log_record, reserved=self._skip_fields)

    def process(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def jsonify(self, log_record):
        """Returns a json string of the log record."""
        return self.serializer(
            log_record,
            default=self.default,
            cls=self.encoder,
            indent=self.indent
        )

    def format(self, record):
        """Formats a log record and serializes to json"""
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = None
            if record.args:
                message_dict['args'], record.args = record.args, None
        else:
            record.message = record.getMessage()
        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get('exc_info'):
            message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info') and record.exc_text:
            message_dict['exc_info'] = record.exc_text

        try:
            log_record = OrderedDict()
        except NameError:
            log_record = {}

        self.add_fields(log_record, record, message_dict)
        log_record = self.process(log_record)

        return self.jsonify(log_record)
