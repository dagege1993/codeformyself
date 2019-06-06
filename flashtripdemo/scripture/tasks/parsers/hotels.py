# coding: utf-8
"""Created by LiuHao
"""

from itertools import chain

from tasks.utils.html import take_first
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime
from tasks.xpath import hotels_xp

from tasks.parsers import HotelOrderParser


class HCOMParser(HotelOrderParser):

    """hotels.com
    """

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if 'Hotels.com' not in sender or \
                not sender.endswith('hotels.com>'):
            return False
        if 'Booking confirmed at ' not in subject:
            return False

        if 'Your booking in' not in snippet:
            return False

        return True

    def _parse(self):  # pylint: disable=R0912, R0915
        result = self._order
        address = strip_str(take_first(self._etree, hotels_xp.ADDRESS))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        confirm_num = take_first(self._etree, hotels_xp.CONFIRM_NUMBER)
        if confirm_num:
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('conform_code is empty %s', self._message_id)

        tz = to_timezone(address)
        check_in_date = take_first(self._etree, hotels_xp.CHECK_IN_DATE)
        if check_in_date:
            check_in_date_formatted = DateTime(
                check_in_date,
                'MMMM D, YYYY'
            ) \
                .tz_to_datetime(tz)  #
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            result['check_in_date'] = check_in_date
        else:
            self.logger.error('check_in_date is empty %s', self._message_id)

        check_in_time = take_first(self._etree, hotels_xp.CHECK_IN_TIME)
        if check_in_time:
            result['check_in_time'] = check_in_time.strip('(').strip(')')
        else:
            self.logger.error('check_in_time is empty %s', self._message_id)

        check_out_date = take_first(self._etree, hotels_xp.CHECK_OUT_DATE)
        if check_out_date:
            check_out_date_formatted = DateTime(
                check_out_date,
                'MMMM D, YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_out_date_formatted:
                result['check_out_date_formatted'] = check_out_date_formatted
            result['check_out_date'] = check_out_date
        else:
            self.logger.error('check_out_date is empty %s', self._message_id)

        check_out_time = take_first(self._etree, hotels_xp.CHECK_OUT_TIME)
        if check_out_time:
            result['check_out_time'] = check_out_time.strip('(').strip(')')
        else:
            self.logger.error('check_out_time is empty %s', self._message_id)

        stay = take_first(self._etree, hotels_xp.STAY)
        if stay:
            result['number_of_nights'] = stay.split(', ')[0]
            result['number_of_rooms'] = stay.split(', ')[-1]
        else:
            self.logger.error('stay is empty %s', self._message_id)

        cancellation_details = strip_list([
            strip_str(take_first(self._etree, hotels_xp.CANCELLATION)),
            strip_str(
                take_first(self._etree, hotels_xp.CANCELLATION_POLICY_1)
            ),
            strip_str(
                take_first(self._etree, hotels_xp.CANCELLATION_POLICY_2)
            )
        ])
        if cancellation_details:
            result['cancellation_policies'] = cancellation_details
        else:
            self.logger.error('policies is empty %s', self._message_id)

        hotel_name = strip_str(take_first(self._etree, hotels_xp.NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        tel = take_first(self._etree, hotels_xp.TELEPHONE)
        if tel:
            result['telephone'] = tel.split(':')[-1].strip()
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        notice = self._etree.xpath(hotels_xp.IMPORTANT_NOTICE)
        if not notice:
            self.logger.warning('notice is empty %s', self._message_id)
        required = self._etree.xpath(hotels_xp.REQUIRED)
        if not required:
            self.logger.warning('required is empty %s', self._message_id)
        if notice or required:
            result['notice'] = list(chain(notice or [], required or []))

        price = strip_str(take_first(self._etree, hotels_xp.PRICE))
        if price:
            result['price'] = price
        else:
            self.logger.error('price is empty %s', self._message_id)
        total = strip_str(take_first(self._etree, hotels_xp.COST))
        if total:
            result['total_cost'] = total
        else:
            self.logger.error('total_cost is empty %s', self._message_id)

        guest_name = ' '.join(strip_list(self._etree.xpath(hotels_xp.ROOM_2)))
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        icon_explanation = take_first(self._etree, hotels_xp.ICON_EXPLANATION)
        if icon_explanation:
            result['icon_explanation'] = icon_explanation
        else:
            self.logger.warning(
                'icon_explanation is empty %s', self._message_id
            )
        room_all = self._etree.xpath(hotels_xp.ROOM_ALL)
        bed_type = room_all.pop(0)
        if bed_type:
            result['bed_type'] = bed_type
        else:
            self.logger.error('bed_type is empty %s', self._message_id)
        values = []
        room_tip = []
        for i in room_all:
            if len(i.strip()) < 5:
                continue
            if '-sq-' in i:
                result['room_area'] = i.strip()
            elif i.startswith(' - '):
                values.append(i.split(' - ')[-1].strip())
            else:
                room_tip.append(i.strip())
        if room_tip:
            result['room_tips'] = room_tip
        else:
            self.logger.error('room_tips is empty %s', self._message_id)
        room_type = strip_str(take_first(self._etree, hotels_xp.ROOM_1))
        if room_type:
            result['room_type'] = room_type
        else:
            self.logger.error('room_type is empty %s', self._message_id)
        preference = strip_str(take_first(self._etree, hotels_xp.PREFERENCE))
        if preference:
            result['preference'] = preference
        else:
            self.logger.error('preference is empty %s', self._message_id)
        note = strip_str(take_first(self._etree, hotels_xp.NOTE))
        if note:
            result['tip'] = note
        else:
            self.logger.error('tip is empty %s', self._message_id)
        facilities_keys = self._etree.xpath(hotels_xp.FACILITIES_KEYS)
        name_dict = {
            'Internet': 'internet',
            'Entertainment': 'entertainment',
            'Food & Drink': 'food_drink',
            'Sleep': 'sleep',
            'Bathroom': 'bathroom',
            'Practical': 'practical',
            'Comfort': 'comfort'
        }
        if facilities_keys and values:
            for i, j in zip(facilities_keys, values):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('room_details is empty %s', self._message_id)
        return result
