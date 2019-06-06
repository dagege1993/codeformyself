# coding: utf8
"""
Created by songww
"""


class ParseError(Exception):
    """Base Error"""
    pass


class ParserNotFound(ParseError):
    """Parse not found"""

    def __init__(self, message_id, sender, subject, snippet):  # noqa pylint: disable=W0231
        self.message_id = message_id
        self.sender = sender
        self.subject = subject
        self.snippet = snippet

    def __str__(self):
        return (f'Parser not found! Id of message is {self.message_id!r}, '
                f'message is from {self.sender!r}, '
                f'with subject {self.subject!r}, {self.snippet!r}')

    __repr__ = __str__


class MissingColumnError(ParseError):
    """Column which must exist is missing.
    """

    def __init__(self, column, message_id):
        super().__init__(column, message_id)
        self.message_id = message_id
        self.column = column

    def __str__(self):
        return (f'Column<{self.column}> must exist, but not found.'
                f'{self.message_id}')

    __repr__ = __str__
