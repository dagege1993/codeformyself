# coding: utf-8
"""Created by LiuHao"""
import re

from lxml import etree
from w3lib.html import remove_tags
from tasks.utils.html import take_first
from tasks.utils.html import filter_dict_value
from tasks.utils.html import to_dict
from tasks.utils.html import remove_space
from tasks.utils.html import unpack
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.html import take_last
from tasks.utils.time import DateTime
from tasks.utils.time import to_timezone
from tasks.xpath import priceline_flight_xp as plf_xp

from tasks.parsers import FlightOrderParser


class PricelineFlightParser(FlightOrderParser):

    """priceline.com"""

    sender_re = re.compile('<([a-zA-Z]+)@trans.priceline.com>')

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        matched = cls.sender_re.search(sender)
        if not matched or matched.group(1) != 'ItineraryAir':
            return False
        if not subject.startswith('Your priceline itinerary'):
            return False
        if 'Thank you for booking with priceline.com' not in snippet:
            return False
        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        stations = self._etree.xpath(plf_xp.STATION)
        if stations:
            result['stations'] = [remove_space(i) for i in stations]
        else:
            self.logger.error('stations is empty %s', self._message_id)

        flight_date = strip_str(take_first(self._etree, plf_xp.DATE))
        if flight_date:
            flight_date = flight_date.split(' - ')
            if len(flight_date) == 2:
                result['depart_date'], result['arrive_date'] = flight_date
        else:
            self.logger.error('flight_date is empty %s', self._message_id)
        flight_time = strip_str(take_first(self._etree, plf_xp.TIME))
        if flight_time:
            flight_time = flight_time.split(' - ')
            if len(flight_time) == 2:
                result['depart_time'], result['arrive_time'] = flight_time
        else:
            self.logger.error('flight_time is empty %s', self._message_id)

        de_date, ar_date = result.get('depart_date'), result.get('arrive_date')
        de_time, ar_time = result.get('depart_time'), result.get('arrive_time')
        de_datetime = de_date and de_time and ' '.join([de_date, de_time])
        ar_datetime = ar_date and ar_time and ' '.join([ar_date, ar_time])
        depart, arrive = unpack(stations)
        tz_depart, tz_arrive = to_timezone(depart), to_timezone(arrive)
        if tz_arrive and tz_depart and de_datetime and ar_datetime:
            depart_datetime_formatted = DateTime(
                de_datetime, 'MMM DD YYYY hh:mm A'
            ).tz_to_datetime(tz_depart)  # D
            if depart_datetime_formatted:
                result['depart_datetime_formatted'] = depart_datetime_formatted
            else:
                self.logger.error(
                    'depart_datetime_formatted is empty %s', self._message_id
                )

            arrive_datetime_formatted = DateTime(
                ar_datetime, 'MMM DD YYYY hh:mm A'
            ).tz_to_datetime(tz_arrive)
            if arrive_datetime_formatted:
                result['arrive_datetime_formatted'] = arrive_datetime_formatted
            else:
                self.logger.error(
                    'arrive_datetime_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'datetime formatted is empty %s', self._message_id
            )

        plane_model = strip_str(take_last(self._etree, plf_xp.TIME))
        if plane_model:
            result['plane_model'] = plane_model
        else:
            self.logger.warning('plane_model is empty %s', self._message_id)

        mileage = strip_str(take_first(self._etree, plf_xp.MILES))
        if mileage:
            result['flight_duration'] = mileage
        else:
            self.logger.warning('mileage is empty %s', mileage)

        confirm_num = take_last(self._etree, plf_xp.CONFIRM_NUM)
        if confirm_num:
            confirm_num = confirm_num.split(':')[-1].strip()
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)
        ticket = take_first(self._etree, plf_xp.TICKET)
        if ticket:
            ticket = ticket.split(':')[-1].strip()
            result['ticket_number'] = ticket
        else:
            self.logger.error('ticket_number is empty %s', self._message_id)

        depart_station = strip_str(take_first(self._etree, plf_xp.DEPART))
        if depart_station:
            result['depart_city'] = depart_station.split(', ')[-1]
            result['depart_station'] = depart_station
        else:
            self.logger.error('depart_station is empty %s', self._message_id)
        arrive_station = strip_str(take_first(self._etree, plf_xp.ARRIVE))
        if arrive_station:
            result['arrive_city'] = arrive_station.split(', ')[-1]
            result['arrive_station'] = arrive_station
        else:
            self.logger.error('arrive_station is empty %s', self._message_id)

        tel = take_first(self._etree, plf_xp.PHONE_PRICELINE)
        if tel:
            result['telephone'] = tel.split(':')[-1].strip()
        else:
            self.logger.error(
                'service telephone is empty %s', self._message_id
            )

        help_keys = self._etree.xpath(plf_xp.HELP_KEYS)
        help_values = self._etree.xpath(plf_xp.HELP_VALUES)
        contact = filter_dict_value(to_dict(help_keys, help_values))
        if contact:
            result['contact_information'] = contact
        else:
            self.logger.warning(
                'contact_information is empty %s', self._message_id
            )

        user_tel = take_first(self._etree, plf_xp.PHONE_USER)
        if user_tel:
            result['guest_telephone'] = user_tel.split(':')[-1].strip()
        else:
            self.logger.warning(
                'guest_telephone is empty %s', self._message_id
            )

        price_keys = strip_list(self._etree.xpath(plf_xp.PRICE_KEYS))
        price_values = strip_list(self._etree.xpath(plf_xp.PRICE_VALUES))
        name_dict = {
            'Billing Name': 'guest_name',
            'Ticket Cost': 'ticket_cost',
            'Taxes & Fees': 'taxes_fee',
            'Tickets': 'number_of_tickets',
            'Total Price': 'total_cost',
            'Bonus': 'bonus'
        }
        if price_keys and price_values:
            for i, j in zip(price_keys, price_values):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('price_details is empty %s', self._message_id)

        notice = self._etree.xpath(plf_xp.NOTICE)
        if notice:
            notice = remove_tags(etree.tostring(notice[0])) \
                .replace('&#13;\n', ' ')
            result['notice'] = strip_list(notice.split('\n\n'))
        else:
            self.logger.error('notice is empty %s', self._message_id)

        related_link_text = self._etree.xpath(plf_xp.RELATED_LINK_TEXT)
        related_link = self._etree.xpath(plf_xp.RELATED_LINK)
        related_links = filter_dict_value(
            to_dict(related_link_text, related_link)
        )
        if related_links:
            result['related_links'] = related_links
        else:
            self.logger.warning('related_links is empty %s', self._message_id)
        return result
