# coding: utf-8
"""Created by LiuHao
"""
import re

from tasks.xpath import priceline_xp
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import take_last
from tasks.utils.html import take_first
from tasks.utils.html import remove_space
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import HotelOrderParser


class PricelineParser(HotelOrderParser):

    """priceline
    """

    sender_re = re.compile('<([a-zA-Z]+)@trans.priceline.com>')

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        matched = cls.sender_re.search(sender)
        if not matched or matched.group(1) != 'hotel':
            return False
        if not subject.startswith('Your priceline itinerary'):
            return False
        if 'Thank you for booking with priceline.com' not in snippet:
            return False
        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        name = remove_space(take_first(self._etree, priceline_xp.NAME))
        if name:
            result['hotel_name'] = name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        address = ', '.join(self._etree.xpath(priceline_xp.ADDRESS)).strip()
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        check_in_date = strip_str(
            take_last(self._etree, priceline_xp.CHECK_IN_DATE)
        )
        tz = to_timezone(address)
        if check_in_date:
            result['check_in_date'] = check_in_date
            check_in_date_formatted = \
                DateTime(check_in_date, 'MMMM DD, YYYY').tz_to_datetime(tz)
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            else:
                self.logger.error(
                    'check_in_date_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error('check_in_date is empty %s', self._message_id)

        check_in_time = strip_str(
            take_last(self._etree, priceline_xp.CHECK_IN_TIME)
        )
        if check_in_time:
            result['check_in_time'] = check_in_time.strip('(').strip(')')
        else:
            self.logger.error('check_in_time is empty %s', self._message_id)
        check_out_date = strip_str(
            take_last(self._etree, priceline_xp.CHECK_OUT_DATE)
        )
        if check_out_date:
            result['check_out_date'] = check_out_date
            check_out_date_formatted = \
                DateTime(check_out_date, 'MMMM DD, YYYY').tz_to_datetime(tz)
            if check_out_date_formatted:
                result['check_out_date_formatted'] = check_out_date_formatted
            else:
                self.logger.error(
                    'check_out_date_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error('check_out_date is empty %s', self._message_id)
        check_out_time = strip_str(
            take_last(self._etree, priceline_xp.CHECK_OUT_TIME)
        )
        if check_out_time:
            result['check_out_time'] = check_out_time.strip('(').strip(')')
        else:
            self.logger.error('check_out_time is empty %s', self._message_id)

        tel = strip_str(take_last(self._etree, priceline_xp.PHONE))
        if tel:
            result['telephone'] = tel
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        confirm_num = self._etree.xpath(priceline_xp.CONFIRM_NUM)
        if confirm_num:
            confirm_num = ''.join(confirm_num).strip()
            pin = confirm_num.split(': ')[-1].strip(')')
            confirm_num = confirm_num.split(' (')[0]
            result['confirm_code'] = confirm_num
            result['pin_code'] = pin
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        room_keys = strip_list(self._etree.xpath(priceline_xp.ROOM_KEYS))
        room_values = strip_list(self._etree.xpath(priceline_xp.ROOM_VALUES))
        if len(room_keys) == len(room_values) and room_keys:
            name_dict = {
                'Deal Type': 'deal_type',
                'Room Price': 'price',
                'Number of rooms': 'number_of_rooms',
                'Number of nights': 'number_of_nights'
            }
            for i, j in zip(room_keys, room_values):
                if i in name_dict:
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is%s %s', i, j, self._message_id)
        else:
            self.logger.error('price is empty %s', self._message_id)
        room_info_keys = strip_list(
            self._etree.xpath(priceline_xp.ROOM_INFO_KEYS)
        )
        room_info_values = strip_list(
            self._etree.xpath(priceline_xp.ROOM_INFO_VALUES)
        )
        room_info_values = list(map(remove_space, room_info_values))
        if room_info_keys and room_info_values:
            name_dict = {
                'Internet': 'internet',
                'Guest Parking': 'guest_parking',
                'Prepayment': 'prepayment',
                'Meal Plan': 'meal_plan'
            }
            for k, v in zip(room_info_keys[::-1], room_info_values[::-1]):
                if k in name_dict:
                    result[name_dict[k]] = v
                elif 'Room Type' in k:
                    room_type = strip_list(
                        self._etree.xpath(priceline_xp.ROOM_TYPE)
                    )
                    if room_type:
                        result['room_type'] = ' '.join(room_type)
                    else:
                        self.logger.error(
                            'room_type is empty %s', self._message_id
                        )
                else:
                    self.logger.warning('%s is %s %s', k, v, self._message_id)
        else:
            self.logger.error('room_info is empty %s', self._message_id)
        reservation_name = strip_list(
            self._etree.xpath(priceline_xp.RESERVATION_NAME)
        )
        if reservation_name:
            result['guest_name'] = reservation_name[0].split(': ')[-1]
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        total = strip_str(
            take_first(self._etree, priceline_xp.ROOM_PRICE_TOTAL)
        )
        if total:
            result['total_cost'] = total
        else:
            self.logger.error('total_price is empty %s', self._message_id)

        room_price_keys = strip_list(
            self._etree.xpath(priceline_xp.ROOM_PRICE_KEYS)
        )
        room_price_keys = strip_list(room_price_keys)
        room_price_values = strip_list(
            self._etree.xpath(priceline_xp.ROOM_PRICE_VALUES)
        )
        if room_price_keys and room_price_values:
            name_dict = {
                'Room Subtotal': 'subtotal',
                'Hotel Fee': 'service_charge',
                'Taxes & Fees': 'taxes_fee'
            }
            for i, j in zip(room_price_keys, room_price_values):
                if i in name_dict:
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('price_details is empty %s', self._message_id)

        price_extra = strip_list(self._etree.xpath(priceline_xp.PRICE_EXTRA))
        price_extra = [remove_space(j) for j in price_extra]
        if price_extra:
            result['price_tips'] = price_extra
        else:
            self.logger.error('price_extra is empty %s', self._message_id)
        notice = strip_list(self._etree.xpath(priceline_xp.NOTICE))
        notice = [remove_space(j) for j in notice]
        if notice:
            result['notice'] = notice
        else:
            self.logger.error('notice is empty %s', self._message_id)
        payment_type = strip_str(
            take_first(self._etree, priceline_xp.PAYMENT_TYPE)
        )
        if payment_type:
            result['payment_forms'] = payment_type
        else:
            self.logger.error('payment_form is empty %s', self._message_id)
        return result
