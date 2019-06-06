# coding: utf-8
"""Created by LiuHao"""

from itertools import chain
from datetime import datetime as dt

from lxml import etree
from w3lib.html import remove_tags
from tasks.xpath import americanairline_xp as aa_xp
from tasks.utils.html import strip_str, take_first, strip_list
from tasks.utils.time import to_timezone, DateTime
from tasks.parsers import FlightOrderParser


class AmericanAirline(FlightOrderParser):

    """aa.com"""

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if not (
            sender.strip('"').startswith('American Airlines') and
            sender.strip('>').endswith('globalnotifications.com')
        ):
            return False

        if not subject.startswith('Your trip confirmation'):
            return False

        _snippet = 'Thank you for booking your flight with American Airlines'
        if _snippet not in snippet:
            return False

        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        if dt.now().timestamp() / int(self.received_time) < 1:
            self.received_time = int(int(self.received_time) / 1000)
        record_locator = strip_str(
            take_first(self._etree, aa_xp.RECORD_LOCATOR)
        )
        if record_locator:
            result['record_locator'] = record_locator
        else:
            self.logger.error('recoder_locator is empty %s', self._message_id)

        itinerary_info_guest = strip_list(self._etree.xpath(aa_xp.INFO_2))
        if itinerary_info_guest:
            result['guest_name'] = itinerary_info_guest[0]
            # TODO (LensHo): to be fix
            if len(itinerary_info_guest) > 1:
                result['meal'] = itinerary_info_guest[-1]
            else:
                self.logger.warning('afford is empty %s', self._message_id)
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        itinerary_info_1 = strip_list(self._etree.xpath(aa_xp.INFO_1))
        if len(itinerary_info_1) == 9:
            result['carrier'] = itinerary_info_1[0]
            result['flight_number'] = itinerary_info_1[1]
            result['depart_city'] = itinerary_info_1[2]
            result['depart_date'] = itinerary_info_1[3]
            result['depart_time'] = itinerary_info_1[4]
            result['arrive_city'] = itinerary_info_1[5]
            result['arrive_date'] = itinerary_info_1[6]
            result['arrive_time'] = itinerary_info_1[7]
            result['booking_code'] = itinerary_info_1[8]
            depart_date_time = ' '.join([
                itinerary_info_1[3], itinerary_info_1[4]
            ])
            arrive_date_time = ' '.join([
                itinerary_info_1[6], itinerary_info_1[7]
            ])
            tz_depart = to_timezone(result['depart_city'])
            tz_arrive = to_timezone(result['arrive_city'])
            depart_dt = DateTime(depart_date_time, 'DDMMM h:mm A')
            depart_year = depart_dt.received_time_to_year(self.received_time)
            depart_datetime_formatted = depart_dt.year_to_datetime(
                depart_year, tz_depart
            )
            if depart_datetime_formatted:
                result['depart_datetime_formatted'] = depart_datetime_formatted
            else:
                self.logger.error(
                    'depart_datetime_formatted is empty %s', self._message_id
                )
            arrive_dt = DateTime(arrive_date_time, 'DDMMM h:mm A')
            arrive_year = arrive_dt.received_time_to_year(self.received_time)
            arrive_datetime_formatted = arrive_dt.year_to_datetime(
                arrive_year, tz_arrive
            )
            if arrive_datetime_formatted:
                result['arrive_datetime_formatted'] = arrive_datetime_formatted
            else:
                self.logger.error(
                    'arrive_datetime_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'itinerary_details is empty %s', self._message_id
            )

        # TODO: (LensHo) might not exist
        itinerary_info_2 = strip_list(self._etree.xpath(aa_xp.INFO_3))
        itinerary_info_trans = strip_list(self._etree.xpath(aa_xp.INFO_4))
        if itinerary_info_trans:
            result['transfer_information'] = itinerary_info_trans[0]
        else:
            self.logger.info(
                'transfer_information is empty %s', self._message_id
            )
        itinerary_info_afford = strip_list(self._etree.xpath(aa_xp.INFO_5))
        if itinerary_info_afford:
            result['trans_meal'] = itinerary_info_afford[-1]
        if len(itinerary_info_2) == 9:
            depart_date_time = ' '.join([
                itinerary_info_2[3], itinerary_info_2[4]
            ])
            arrive_date_time = ' '.join([
                itinerary_info_2[6], itinerary_info_2[7]
            ])
            result['trans_carrier'] = itinerary_info_2[0]
            result['trans_flight_number'] = itinerary_info_2[1]
            result['trans_depart_city'] = itinerary_info_2[2]
            result['trans_depart_date'] = itinerary_info_2[3]
            result['trans_depart_time'] = itinerary_info_2[4]
            result['trans_arrive_city'] = itinerary_info_2[5]
            result['trans_arrive_date'] = itinerary_info_2[6]
            result['trans_arrive_time'] = itinerary_info_2[7]
            result['trans_booking_code'] = itinerary_info_2[8]
            tz_depart = to_timezone(result['trans_depart_city'])
            tz_arrive = to_timezone(result['trans_arrive_city'])
            depart_dt = DateTime(depart_date_time, 'DDMMM h:mm A')
            depart_year = depart_dt.received_time_to_year(self.received_time)
            depart_datetime_formatted_2 = depart_dt.year_to_datetime(
                depart_year, tz_depart
            )
            if depart_datetime_formatted_2:
                result['trans_depart_datetime_formatted'] = \
                    depart_datetime_formatted_2
            else:
                self.logger.error(
                    'trans_depart_datetime_formatted is empty %s',
                    self._message_id
                )
            arrive_dt = DateTime(arrive_date_time, 'DDMMM h:mm A')
            arrive_year = arrive_dt.received_time_to_year(self.received_time)
            arrive_datetime_formatted_2 = arrive_dt.year_to_datetime(
                arrive_year, tz_arrive
            )
            if arrive_datetime_formatted_2:
                result['trans_arrive_datetime_formatted'] = \
                    arrive_datetime_formatted_2
            else:
                self.logger.error(
                    'trans_arrive_datetime_formatted is empty %s',
                    self._message_id
                )
        else:
            self.logger.info(
                'transfer information is empty %s', self._message_id
            )

        receipt_info = self._etree.xpath(aa_xp.INFO_6)
        if receipt_info:
            name_dict = {
                'TICKET NUMBER': 'ticket_number',
                'FARE-SGD': 'fare_sgd',
                'EQUIV FARE-EUR': 'fare_equal_to_eur',
                'TAXES AND CARRIER-IMPOSED FEES': 'taxes_fee'
            }
            for i in receipt_info[0]:
                name = take_first(i, './/strong/text()')
                value = take_first(i, './/td/text()')
                if value and name in name_dict.keys():
                    result[name_dict[name]] = value
                elif name in ['TICKET TOTAL', 'PASSENGER']:
                    pass
                else:
                    self.logger.warning(
                        '%s: passengers is empty',
                        self._message_id,
                    )
        else:
            self.logger.error('receipt_info is empty %s', self._message_id)

        total_price = strip_str(take_first(self._etree, aa_xp.TOTAL))
        if total_price:
            result['total_cost'] = total_price
        else:
            self.logger.error('price_details is empty %s', self._message_id)

        notice_1 = take_first(self._etree, aa_xp.NOTICE_1)
        notice_3 = take_first(self._etree, aa_xp.NOTICE_3)
        notice_1 = notice_1 and strip_str(
            remove_tags(etree.tostring(notice_1))
        )
        if not notice_1:
            self.logger.warning(
                'part1 of notice is empty %s', self._message_id
            )
        notice_2 = strip_str(take_first(self._etree, aa_xp.NOTICE_2))
        if not notice_2:
            self.logger.warning(
                'part2 of notice is empty %s', self._message_id
            )
        notice_3 = strip_str(remove_tags(etree.tostring(notice_3))) \
            if notice_3 else ''
        if not notice_3:
            self.logger.warning(
                'part3 of notice is empty %s', self._message_id
            )
        if notice_1 or notice_2 or notice_3:
            result['notice'] = strip_list([notice_1, notice_2, notice_3])

        related_links_1 = self._etree.xpath(aa_xp.RELATED_LINK_1)
        if not related_links_1:
            self.logger.warning(
                'part1 of related_links is empty %s', self._message_id
            )
        related_links_3 = self._etree.xpath(aa_xp.RELATED_LINK_3)
        if not related_links_3:
            self.logger.warning(
                'part2 of related_links is empty %s', self._message_id
            )
        related_texts_1 = strip_list(self._etree.xpath(aa_xp.RELATED_TEXT_1))
        related_texts_3 = strip_list(self._etree.xpath(aa_xp.RELATED_TEXT_3))
        links = chain(related_links_1 or [], related_links_3 or [])
        texts = chain(related_texts_1 or [], related_texts_3 or [])
        name_dict = {
            'Check-In Options': 'check_in_options_link',
            'Baggage Information.': 'baggage_information_link',
            'U.S. Entry Requirements.': 'us_entry_requirements_link',
            'Contact American.': 'contact_american_link',
            'Worldwide Phone Numbers': 'worldwide_phone_numbers_link',
            'Conditions of Carriage': 'conditions_of_carriage_link'
        }
        for i, j in zip(texts, links):
            if i in name_dict:
                result[name_dict[i]] = j
            else:
                self.logger.warning('%s is %s %s', i, j, self._message_id)
        return result
