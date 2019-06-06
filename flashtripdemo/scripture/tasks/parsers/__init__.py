# coding: utf8
"""Module parses
"""

__all__ = [
    'OrderParser', 'HotelOrderParser', 'select_parser', 'Parser',
    'FlightOrderParser', 'RestOrderParser'
]

from .order_parser import (
    Parser, OrderParser, HotelOrderParser, FlightOrderParser, RestOrderParser,
    select_parser
)

from .accor import Accor
from .americanairline import AmericanAirline
from .booking import BookingParser
from .britishairways import BritishAirwaysParser
from .delta import DeltaParser
from .expedia import ExpediaHotelParser
from .expedia_flight import ExpediaFlightParser
from .hilton import HiltonParser
from .hotels import HCOMParser
from .hyatt import HYATTParser
from .ihg import IHGParser
from .marriott import MarriottParser
from .opentable import OpenTableParser
from .priceline import PricelineParser
from .priceline_flight import PricelineFlightParser
from .spg import SPGPaser
from .travelzoo import TravelzooParser
from .united import UnitedParser
from .wyndham import WyndhamParser
