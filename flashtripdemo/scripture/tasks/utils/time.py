from tasks import settings
import arrow
from arrow.parser import ParserError
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
import logging

logger = logging.getLogger(__name__)


class DateTime:

    def __init__(self, raw_datetime, datetime_format):
        self.raw_datetime = raw_datetime
        self.datetime_format = datetime_format

    def tz_to_datetime(self, tz):
        if not tz:
            return
        try:
            return arrow.get(
                self.raw_datetime, self.datetime_format, tzinfo=tz
            ).datetime
        except ParserError as e:
            logger.exception(e)

    def received_time_to_year(self, received_time):
        try:
            date_raw = arrow.get(self.raw_datetime, self.datetime_format).date()
            date_received = arrow.get(received_time).date()
            if date_raw.month < date_received.month:
                return date_received.year + 1
            return date_received.year
        except ParserError as e:
            logger.exception(e)

    def year_to_datetime(self, year, tz):
        dt = self.tz_to_datetime(tz)
        if dt and year:
            try:
                return dt.replace(year=year)
            except ValueError as e:
                logger.exception(e)

    def to_time(self):
        try:
            return arrow.get(self.raw_datetime, self.datetime_format).time()
        except ParserError as e:
            logger.exception(e)


def to_timezone(address):
    if address:
        try:
            geo = GoogleV3(
                api_key=settings.GOOGLE_GEO_KEY,
                timeout=30,
                proxies=settings.PROXIES
            )
            g = geo.geocode(address)
            return geo.timezone(g.point).zone
        except GeocoderTimedOut as e:
            logger.exception(e)
