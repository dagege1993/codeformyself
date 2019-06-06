# coding: utf8

from .error_response import ErrorResponse


class HotelNotFound(Exception):
    pass


class RoomsxmlNotFound(HotelNotFound):
    pass


class JsetNotFound(HotelNotFound):
    pass
