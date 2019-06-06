# coding: utf-8
"""Created by LiuHao"""

import arrow

from lxml import etree
from w3lib.html import remove_tags

from tasks.xpath import booking_xp
from tasks.utils.html import take_first
from tasks.utils.html import filter_dict_value
from tasks.utils.html import to_dict
from tasks.utils.html import slice_list
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.time import DateTime
from tasks.utils.time import to_timezone

from tasks.parsers import HotelOrderParser


class BookingParser(HotelOrderParser):

    """booking.com
    """

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        """Override"""
        if not sender.endswith('booking.com>'):
            return False
        if 'Booking confirmed at' not in subject:
            return False
        if not snippet.startswith('Booking.com Confirmation Number:'):
            return False
        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        """Override"""
        result = self._order
        confirm_num_values = self._etree.xpath(
            booking_xp.CONFIRMATION_NUMBER_VALUES
        )
        confirm_num_values = strip_list(confirm_num_values)
        if len(confirm_num_values) == 2:
            result['confirm_code'] = confirm_num_values[0]
            result['pin_code'] = confirm_num_values[1]
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        name = strip_str(take_first(self._etree, booking_xp.HOTEL_NAME))
        if name:
            result['hotel_name'] = name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        address = slice_list(
            strip_str(take_first(self._etree, booking_xp.ADDRESS)), -3
        )[0]
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        telephone = strip_str(take_first(self._etree, booking_xp.PHONE))
        if telephone:
            result['telephone'] = telephone
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        check_in_date_formatted = take_first(
            self._etree, booking_xp.CHECK_IN_DATE_FORMATTED
        )
        if check_in_date_formatted:
            result['check_in_date_formatted'] = \
                arrow.get(check_in_date_formatted).datetime
        check_out_date_formatted = take_first(
            self._etree, booking_xp.CHECK_OUT_DATE_FORMATTED
        )
        if check_out_date_formatted:
            result['check_out_date_formatted'] = \
                arrow.get(check_out_date_formatted).datetime

        check_in_date = strip_str(
            take_first(self._etree, booking_xp.CHECK_IN_DATE)
        )
        if check_in_date:
            result['check_in_date'] = check_in_date
        else:
            self.logger.error('check_in_date is empty %s', self._message_id)

        check_in_time = strip_str(
            take_first(self._etree, booking_xp.CHECK_IN_TIME)
        ) \
            .strip('(').strip(')')
        if check_in_time:
            result['check_in_time'] = check_in_time
        else:
            self.logger.error('check_in_time is empty %s', self._message_id)

        check_out_date = strip_str(
            take_first(self._etree, booking_xp.CHECK_OUT_DATE)
        )
        if check_out_date:
            result['check_out_date'] = check_out_date
        else:
            self.logger.error('check_out_date is empty %s', self._message_id)

        check_out_time = strip_str(
            take_first(self._etree, booking_xp.CHECK_OUT_TIME)
        ) \
            .strip('(').strip(')')
        if check_out_time:
            result['check_out_time'] = check_out_time
        else:
            self.logger.error('check_out_time is empty %s', self._message_id)

        price_details = strip_list(self._etree.xpath(booking_xp.PRICE_DETAILS))
        if price_details:
            result['bed_type'] = price_details[0]
            result['price'] = price_details[1]
            result['total_cost'] = price_details[-1]
            tmp = zip(price_details[::2][1:-1], price_details[1::2][1:-1])
            for i, j in tmp:
                self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('price_details is empty %s', self._message_id)

        requests = strip_list(
            self._etree.xpath(booking_xp.SPECIAL_REQUEST_1) or
            self._etree.xpath(booking_xp.SPECIAL_REQUEST_2)
        )
        your_special_requirements = [
            i for i in requests
            if i and i != "\u2022" and i != "Special Requests"
        ]
        if your_special_requirements:
            result['your_special_requirements'] = your_special_requirements
        else:
            self.logger.warning(
                'your_special_requirements is empty %s', self._message_id
            )

        free_cancellation = strip_str(
            take_first(self._etree, booking_xp.CANCELLATION)
        )
        free_cancellation = free_cancellation.split('.')[0].replace('\n', ' ')
        if free_cancellation:
            result['free_cancellation'] = free_cancellation
        else:
            self.logger.error(
                'free_cancellation_policy is empty %s', self._message_id
            )

        payment_forms = strip_str(
            take_first(self._etree, booking_xp.PAYMENT_FORMS)
        )
        if payment_forms:
            result['payment_forms'] = payment_forms
        else:
            self.logger.warning('payment_forms is empty %s', self._message_id)

        if free_cancellation:
            tz = check_out_date_formatted[-5:] \
                if check_out_date_formatted else to_timezone(address)
            free_cancellation_time = \
                DateTime(free_cancellation,
                         'MMMM DD, YYYY hh:mm A').tz_to_datetime(tz)  # D, H
            if str(free_cancellation_time):
                result['free_cancellation_time'] = free_cancellation_time

        notice = strip_list(
            self._etree.xpath(booking_xp.IMPORTANT_INFORMATION)
        )
        price_extra = strip_list(self._etree.xpath(booking_xp.PRICE_EXTRA))
        if price_extra:
            result['price_tips'] = [
                i for i in price_extra if 'Book.com' not in i
            ]
        else:
            self.logger.error('price_extra is empty %s', self._message_id)
        if notice:
            result['notice'] = notice
        else:
            self.logger.error('notice is empty %s', self._message_id)

        stay = strip_str(take_first(self._etree, booking_xp.STAY))
        if stay:
            result['number_of_nights'] = stay.split(',')[0]
            result['number_of_rooms'] = stay.split(',')[-1].strip()
        else:
            self.logger.error('stay is empty %s', self._message_id)

        booking_summary_keys = strip_list(
            self._etree.xpath(booking_xp.BOOKING_SUMMERY_KEYS)
        )
        booking_summary_values = self._etree.xpath(
            booking_xp.BOOKING_SUMMERY_VALUES
        )
        if booking_summary_values and booking_summary_keys:
            booking_summary_values = strip_list([
                remove_tags(etree.tostring(i)) for i in booking_summary_values
            ])
            for k, v in zip(booking_summary_keys, booking_summary_values):
                if 'Cancellation cost' in k:
                    cost = self._etree.xpath(booking_xp.CANCELLATION_COST)
                    if cost:
                        v = [remove_tags(etree.tostring(i)) for i in cost]
                        v = [i.replace('\n', ' ').strip() for i in v]
                        result['cancellation_cost'] = v
                elif 'Prepayment' in k:
                    result['prepayment'] = v
                elif k in ['Check-in', 'Check-out', 'Your reservation']:
                    pass
                else:
                    self.logger.warning('%s is %s %s', k, v, self._message_id)
        else:
            self.logger.error('booking_summary is empty %s', self._message_id)
        room_tip = slice_list(
            strip_list(self._etree.xpath(booking_xp.ROOM_AREA)), 1
        )[1]
        if room_tip:
            result['room_tips'] = room_tip
        else:
            self.logger.warning('room_tip is empty %s', self._message_id)
        order_condition_keys = self._etree.xpath(
            booking_xp.BOOKING_CONDITIONS_KEYS
        )
        order_condition_keys = slice_list(order_condition_keys, 3)[0]
        order_condition_values = self._etree.xpath(
            booking_xp.BOOKING_CONDITIONS_VALUES
        )
        order_condition_values = slice_list(order_condition_values, 3)[0]
        if order_condition_values and order_condition_keys:
            order_condition_values = map(
                lambda i: remove_tags(etree.tostring(i)),
                order_condition_values
            )
            order_condition_values = strip_list(order_condition_values)
            name_dict = {
                'Guest parking': 'guest_parking',
                'Internet': 'internet'
            }
            for k, v in zip(order_condition_keys, order_condition_values):
                if k in order_condition_keys:
                    result[name_dict[k]] = v
                elif 'Cancellation policy' in k:
                    result['cancellation_policies'] = [v]
                else:
                    self.logger.warning('%s is %s %s', k, v, self._message_id)
        else:
            self.logger.error('room_details is empty %s', self._message_id)

        hotel_link = take_first(self._etree, booking_xp.HOTEL_URL)
        if hotel_link:
            result['hotel_link'] = hotel_link
        else:
            self.logger.error('hotel_link is empty %s', self._message_id)
        address_link = take_first(self._etree, booking_xp.ADDRESS_URL)
        if address_link:
            result['map_link'] = address_link
        else:
            self.logger.error('map_link is empty %s', self._message_id)
        cancellation_link = take_first(
            self._etree, booking_xp.CANCELLATION_URL
        )
        if cancellation_link:
            result['cancellation_link'] = cancellation_link
        else:
            self.logger.error(
                'cancellation_link is empty %s', self._message_id
            )
        change_keys = strip_list(
            self._etree.xpath(booking_xp.CHANGE_LINKS_KEYS)
        )
        change_values = self._etree.xpath(booking_xp.CHANGE_LINKS_VALUES)
        related_links = filter_dict_value(to_dict(change_keys, change_values))
        if related_links:
            result['related_links'] = related_links
        else:
            self.logger.error('related_links is empty %s', self._message_id)
        return result
