# coding: utf-8
"""Created by LiuHao"""

import arrow
import ujson as json

from tasks.xpath import hilton_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import remove_space

from tasks.parsers import HotelOrderParser


class HiltonParser(HotelOrderParser):

    """Hilton"""

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        sender_name = 'Hilton Hotels & Resorts Confirmed'
        if not (
            sender.strip('"').startswith(sender_name) and
            sender.strip('>').endswith('hilton.com')
        ):
            return False

        if not (subject.startswith('Your ') and 'Confirmation' in subject):
            return False

        if 'Confirmation Number:' not in snippet:
            return False

        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        hotel_name = strip_str(take_first(self._etree, hilton_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        confirm_num = take_first(self._etree, hilton_xp.CONFIRM_NUM)
        if confirm_num:
            confirm_num = confirm_num.split(':')[-1].strip()
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        address = strip_str(take_first(self._etree, hilton_xp.ADDRESS))
        if address:
            result['address'] = remove_space(address)
        else:
            self.logger.error('address is empty %s', self._message_id)

        phone = strip_list(
            strip_str(take_first(self._etree, hilton_xp.PHONE)).split('\n')
        )
        if phone:
            result['telephone'] = ' '.join(phone)
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        json_data = take_first(self._etree, hilton_xp.JSON)
        if json_data:
            data = json.loads(json_data)
            check_in_datetime = data.get('checkinTime')
            check_out_datetime = data.get('checkoutTime')
        else:
            check_in_datetime = check_out_datetime = ''
            self.logger.error(
                'check_in_datetime and check_out_datetime is empty %s',
                self._message_id
            )
        if check_in_datetime and check_out_datetime:
            result['check_in_date_formatted'] = \
                arrow.get(check_in_datetime).datetime
            result['check_out_date_formatted'] = \
                arrow.get(check_out_datetime).datetime
            result['check_in_date'] = check_in_datetime.split('T')[0]
            result['check_in_time'
                   ] = check_in_datetime.split('T')[-1].split('-')[0]
            result['check_out_date'] = check_out_datetime.split('T')[0]
            result['check_out_time'] = \
                check_out_datetime.split('T')[-1].split('-')[0]

        update_link = take_first(self._etree, hilton_xp.UPDATE_LINK)
        if update_link:
            result['modify_link'] = update_link
        else:
            self.logger.error('modify link is empty %s', self._message_id)

        related_links = self._etree.xpath(hilton_xp.RELATED_LINK)
        names = ['Explore', 'Maps', 'Dining', 'Convenience']
        name_dict = {
            'Explore': 'explore_link',
            'Maps': 'map_link',
            'Dining': 'dining_link',
            'Convenience': 'convenience_link'
        }
        if related_links:
            for i, j in zip(names, related_links):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        reservation_info = self._etree.xpath(hilton_xp.ROOM_INFO)
        if reservation_info:
            room_type = reservation_info.pop(0)
            room_type = ' '.join(strip_list(room_type.xpath('./td/text()')))
            if room_type:
                result['room_type'] = room_type
            else:
                self.logger.error('room_type is empty %s', self._message_id)
            name_dict = {
                'Guests': 'number_of_guests',
                'Rooms': 'number_of_rooms',
                'Check In': 'check_in_raw',
                'Check Out': 'check_out_raw'
            }
            for i in reservation_info:
                title = strip_str(take_first(i, './td[1]/strong/text()'))
                value = remove_space(take_first(i, './td[2]/text()'))
                if title in name_dict.keys():
                    result[name_dict[title]] = value
                else:
                    self.logger.warning(
                        '%s is %s %s', title, value, self._message_id
                    )
        else:
            self.logger.error(
                'reservation_information is empty %s', self._message_id
            )

        charge_names = strip_list(self._etree.xpath(hilton_xp.CHARGE_NAME))
        charge_values = strip_list(self._etree.xpath(hilton_xp.CHARGE_VALUE))
        charge_values = [remove_space(i) for i in charge_values]
        charge_names = [
            remove_space(i) for i in charge_names if 'Stay per Room' not in i
        ]
        if charge_names and charge_values:
            name_dict = {
                'Taxes': 'taxes_fee_per_room',
                'Total': 'total_per_room',
                'Total for Stay': 'total_cost',
                'Service Charge': 'service_charge_per_room',
                'Rate': 'price_per_room',
                'Rate per night': 'price',
            }
            for i, j in zip(charge_names, charge_values):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('price_details is empty %s', self._message_id)

        cancellation = strip_list(self._etree.xpath(hilton_xp.CANCELLATION))
        if cancellation:
            result['cancellation_policies'] = cancellation
        else:
            self.logger.error('cancellation is empty %s', self._message_id)

        rate_rule_cancellation = \
            strip_list(self._etree.xpath(hilton_xp.RATE_RULE_CANCELLATION))
        if rate_rule_cancellation:
            result['rate_rules'] = rate_rule_cancellation
        else:
            self.logger.error(
                'rate_rule_cancellation is empty %s', self._message_id
            )
        additional_info_names = strip_list(
            self._etree.xpath(hilton_xp.ADDITIONAL_INFO_NAME)
        )
        additional_info_values = \
            strip_list(self._etree.xpath(hilton_xp.ADDITIONAL_INFO_VALUE))
        name_dict = {
            'Service Charges': 'service_charge',
            'Self parking': 'guest_parking'
        }
        if additional_info_names and additional_info_values:
            for i, j in zip(additional_info_names, additional_info_values):
                if i in name_dict.keys():
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error(
                'additional_information is empty %s', self._message_id
            )

        notice = strip_list(self._etree.xpath(hilton_xp.NOTICE))
        if notice:
            result['notice'] = notice
        return result
