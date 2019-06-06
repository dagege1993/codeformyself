# coding: utf-8
"""Created by LiuHao"""

from typing import Dict

from lxml import etree
from w3lib.html import remove_tags

from tasks.xpath import expedia_flight_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.html import to_dict
from tasks.utils.html import unpack
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import FlightOrderParser


class ExpediaFlightParser(FlightOrderParser):

    """Flight on Expedia.com"""

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if not (
            snippet.startswith('Expedia.com ') and
            'Your reservation is booked and confirmed' in snippet
        ):
            return False

        if not (
            sender.strip('"').startswith('Expedia.com') and
            sender.strip('>').endswith('expediamail.com')
        ):
            return False

        if 'Expedia travel confirmation' not in subject:
            return False

        return True

    def _parse(self) -> Dict:  # pylint: disable=R0912,R0915,R0916
        result = self._order

        itinerary = strip_str(
            take_first(self._etree, expedia_flight_xp.ITINERARY)
        )
        if itinerary:
            result['itinerary_code'] = itinerary
        else:
            self.logger.error('itinerary is empty %s', self._message_id)
        confirm_num = strip_str(
            take_first(self._etree, expedia_flight_xp.CONFIRM_NUM)
        )
        if confirm_num:
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_code is empty %s', self._message_id)
        booking_id = strip_str(
            take_first(self._etree, expedia_flight_xp.BOOKING_ID)
        )
        if booking_id:
            result['booking_id'] = booking_id
        else:
            self.logger.error('booking_id is empty %s', self._message_id)
        ticket = strip_str(take_first(self._etree, expedia_flight_xp.TICKET))
        if ticket:
            result['ticket_number'] = ticket.split(' ')[0] \
                if ' ' in ticket else ticket
        else:
            self.logger.error('ticket_number is empty %s', self._message_id)

        depart_date, arrive_date = \
            unpack(strip_list(take_first(self._etree,
                                         expedia_flight_xp.DATES).split(' - ')))
        if depart_date and arrive_date:
            result['depart_date'] = depart_date
            result['arrive_date'] = arrive_date
        else:
            self.logger.error(
                'depart_date and arrive_date is empty %s', self._message_id
            )

        related_links_1 = self._etree.xpath(expedia_flight_xp.RELATED_LINK_1)
        if related_links_1:
            name_dict = {
                'Change': 'change_link',
                'cancel': 'cancellation_link',
                'Customer Support': 'customer_support_link'
            }
            for i in related_links_1:
                link = take_first(i, './@href')
                text = take_first(i, './text()')
                if text in name_dict.keys():
                    result[name_dict[text]] = link
                else:
                    self.logger.warning(
                        '%s is %s %s', text, link, self._message_id
                    )
        else:
            self.logger.error(
                'part 1 of related_links is empty %s', self._message_id
            )
        related_links_2 = self._etree.xpath(expedia_flight_xp.RELATED_LINK_2)
        related_texts_2 = self._etree.xpath(expedia_flight_xp.RELATED_TEXT_2)
        if related_links_2 and related_texts_2:
            result['related_links'] = to_dict(related_texts_2, related_links_2)
        else:
            self.logger.warning(
                'part 2 of related_links is empty %s', self._message_id
            )

        flight_name = strip_str(
            take_first(self._etree, expedia_flight_xp.FLIGHT_NAME)
        )
        if flight_name:
            result['flight_name'] = flight_name
        else:
            self.logger.error('flight_name is empty %s', self._message_id)

        policies = strip_str(
            take_first(self._etree, expedia_flight_xp.CANCELLATION)
        )
        if policies:
            result['policies'] = [policies]
        else:
            self.logger.error('policies is empty %s', self._message_id)
        depart_station = strip_str(
            take_first(self._etree, expedia_flight_xp.DEPART_STATION)
        )
        if depart_station:
            result['depart_station'] = depart_station
        else:
            self.logger.error('depart_station is empty %s', self._message_id)
        depart_time = strip_str(
            take_first(self._etree, expedia_flight_xp.DEPART_TIME)
        )
        if depart_time:
            result['depart_time'] = depart_time
        else:
            self.logger.error('depart_time is empty %s', self._message_id)
        depart_terminal = strip_str(
            take_first(self._etree, expedia_flight_xp.DEPART_TERMINAL)
        )
        if depart_terminal:
            result['depart_terminal'] = depart_terminal
        else:
            self.logger.error('depart_terminal is empty %s', self._message_id)
        arrive_station = strip_str(
            take_first(self._etree, expedia_flight_xp.ARRIVE_STATION)
        )
        if arrive_station:
            result['arrive_station'] = arrive_station
        else:
            self.logger.error('arrive_station is empty %s', self._message_id)
        arrive_time = strip_str(
            take_first(self._etree, expedia_flight_xp.ARRIVE_TIME)
        )
        if arrive_time:
            result['arrive_time'] = arrive_time
        else:
            self.logger.error('arrive_time is empty %s', self._message_id)
        arrive_terminal = strip_str(
            take_first(self._etree, expedia_flight_xp.ARRIVE_TERMINAL)
        )
        if arrive_terminal:
            result['arrive_terminal'] = arrive_terminal
        else:
            self.logger.error('arrive_terminal is empty %s', self._message_id)
        if arrive_station \
                and depart_station \
                and arrive_time \
                and arrive_date \
                and depart_time \
                and depart_date:
            tz_depart = to_timezone(depart_station)
            tz_arrive = to_timezone(arrive_station)
            depart_datetime = ' '.join([depart_date, depart_time])
            arrive_datetime = ' '.join([arrive_date, arrive_time])
            depart_datetime = \
                DateTime(depart_datetime,  # TODO: (LensHo) datetime formatted
                         'MMM DD, YYYY h:mma').tz_to_datetime(tz_depart)
            if depart_datetime:
                result['depart_datetime_formatted'] = depart_datetime
            else:
                self.logger.error(
                    'depart_datetime_formatted is empty %s', self._message_id
                )
            arrive_datetime = \
                DateTime(arrive_datetime,
                         'MMM DD, YYYY h:mma').tz_to_datetime(tz_arrive)
            if arrive_datetime:
                result['arrive_datetime_formatted'] = arrive_datetime
            else:
                self.logger.error(
                    'arrive_datetime_formatted is empty %s', self._message_id
                )

        cabin = strip_str(take_first(self._etree, expedia_flight_xp.CABIN))
        if cabin:
            result['cabin'] = cabin
        else:
            self.logger.error('cabin is empty %s', self._message_id)

        flight_info_divs = self._etree.xpath(
            expedia_flight_xp.FLIGHT_INFO_DIVS
        )
        if flight_info_divs:
            name_dict = {
                'Included': 'included',
                'Fee applies': 'fee_applies',
                'Not included': 'not_included'
            }
            for i in flight_info_divs:
                name = take_first(i, expedia_flight_xp.FLIGHT_INFO_DIV_NAME)
                value = i.xpath(expedia_flight_xp.FLIGHT_INFO_DIV_VALUE)
                if name in name_dict.keys():
                    result[name_dict[name]] = value
                else:
                    self.logger.warning(
                        '%s is %s %s', name, value, self._message_id
                    )

        flight_duration = take_first(
            self._etree, expedia_flight_xp.FLIGHT_DURATION
        )
        flight_duration = strip_str(flight_duration)
        if flight_duration:
            result['flight_duration'] = flight_duration
        else:
            self.logger.error('flight_duration is empty %s', self._message_id)

        guest_name = strip_str(
            take_first(self._etree, expedia_flight_xp.GUEST)
        )
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        price = strip_list(self._etree.xpath(expedia_flight_xp.PRICE))
        if price:
            name_dict = {'Flight': 'price', 'Taxes & Fees': 'taxes_fee'}
            for i, j in zip(price[::2], price[1::2]):
                if 'Traveler' in i:
                    continue
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('price is empty %s', self._message_id)
        total = strip_str(take_first(self._etree, expedia_flight_xp.TOTAL))
        if total:
            result['total_cost'] = total
        else:
            self.logger.error('total_cost is empty %s', self._message_id)

        united_restrictions = self._etree.xpath(
            expedia_flight_xp.UNITED_RESTRICTIONS
        )
        united_restrictions = strip_list([
            remove_tags(etree.tostring(i)) for i in united_restrictions
        ])
        res_des = strip_list(
            self._etree.xpath(expedia_flight_xp.UNITED_RESTRICTIONS_DES)
        )
        if united_restrictions:
            if res_des:
                des_num = range(len(res_des))
                name_dict = {str(k + 1): v for k, v in zip(des_num, res_des)}
            restrictions = []
            for i in united_restrictions:
                if i[-1].isdigit() and res_des:
                    restrictions.append({
                        'text': i,
                        'explanation': name_dict[i[-1]]
                    })
                else:
                    restrictions.append({'text': i})
            if restrictions:
                result['united_restrictions'] = restrictions
            else:
                self.logger.error('united_res is empty %s', self._message_id)
        else:
            self.logger.error(
                'united_restrictions is empty %s', self._message_id
            )

        notice = strip_list(self._etree.xpath(expedia_flight_xp.NOTICE))
        if notice:
            result['notice'] = notice
        else:
            self.logger.error('notice is empty %s', self._message_id)
        airline_rule = strip_str(
            take_first(self._etree, expedia_flight_xp.AIRLINE_RULE)
        )
        if airline_rule:
            result['airline_rule'] = airline_rule
        else:
            self.logger.error('airline_rule is empty %s', self._message_id)
        tel = strip_str(take_first(self._etree, expedia_flight_xp.PHONE))
        if tel:
            result['telephone'] = tel.split(' ')[-1].strip('.')
        else:
            self.logger.error('telephone is empty %s', self._message_id)
        return result
