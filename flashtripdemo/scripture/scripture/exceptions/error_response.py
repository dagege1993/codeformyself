# coding: utf8


class ErrorResponse(Exception):

    def __init__(self, response):
        super().__init__(response.text, response.url, response.status_code)
        self.message = response.text
        self.code = response.status_code
