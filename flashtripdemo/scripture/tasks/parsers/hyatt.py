# coding: utf-8
from itertools import chain

from tasks.xpath import hyatt_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import unpack
from tasks.utils.html import remove_space
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import HotelOrderParser


class HYATTParser(HotelOrderParser):

    """Hyatt"""

    @classmethod
    def validate(cls, sender, subject, snippet):
        if 'Hyatt Hotels' not in sender or 'hyatt.com' not in sender:
            return False
        if 'Confirmation' not in subject:
            return False
        if 'Your reservation is confirmed' not in snippet:
            return False
        return True

    def parse(self):
        result = self._order
        hotel_name = strip_str(take_first(self._etree, hyatt_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        confirm_num = strip_str(take_first(self._etree, hyatt_xp.CONFIRM_NUM))
        if confirm_num:
            confirm_num = confirm_num.split(': ')[-1]
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('conform_number is empty %s', self._message_id)

        address = ', '.join(strip_list(self._etree.xpath(hyatt_xp.ADDRESS)))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        telephone = strip_str(take_first(self._etree, hyatt_xp.PHONE))
        if telephone:
            result['telephone'] = telephone
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        check_in_out_datetime = strip_list(
            self._etree.xpath(hyatt_xp.CHECK_IN_OUT_DATETIME)
        )
        check_in_date, check_in_time, check_out_date, check_out_time = \
            unpack(check_in_out_datetime, 4)
        if check_out_date and check_in_date:
            tz = to_timezone(address)
            check_in_date = remove_space(check_in_date)
            check_out_date = remove_space(check_out_date)
            result['check_in_date'] = check_in_date
            result['check_out_date'] = check_out_date
            check_in_date_formatted = DateTime(
                check_in_date,
                'MMMM DD, YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            else:
                self.logger.error(
                    'check_in_date_formatted is empty %s', self._message_id
                )
            check_out_date_formatted = DateTime(
                check_out_date,
                'MMMM DD, YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_out_date_formatted:
                result['check_out_date_formatted'] = check_out_date_formatted
            else:
                self.logger.error(
                    'check_out_date_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'check_in_date and check_out_date is empty %s',
                self._message_id
            )

        if check_in_time and check_out_time:
            result['check_in_time'] = check_in_time
            result['check_out_time'] = check_out_time
        else:
            self.logger.error(
                'check_in_time and check_out_time is empty %s',
                self._message_id
            )

        related_links = self._etree.xpath(hyatt_xp.RELATED_LINKS)
        related_text = strip_list(
            self._etree.xpath(hyatt_xp.RELATED_LINKS_TEXT)
        )
        plan_link = self._etree.xpath(hyatt_xp.PLAN_LINK)
        plan_text = strip_list(self._etree.xpath(hyatt_xp.PLAN_TEXT))
        if not related_links and related_text:
            self.logger.error('related_links is empty %s', self._message_id)
        if not plan_text and plan_link:
            self.logger.error('plan_links is empty %s', self._message_id)
        related_links = chain(related_links or [], plan_link or [])
        related_texts = chain(related_text, plan_text)
        if related_links and related_texts:
            name_dict = {
                'Cancel Reservation': 'cancellation_link',
                'Modify Reservation': 'modify_link',
                'Get to know our hotel': 'hotel_link',
                'Add Reservation': 'add_reservation_link',
                'Customer Service': 'customer_service_link'
            }
            for i, j in zip(related_texts, related_links):
                if i in name_dict:
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        reservation_info = self._etree.xpath(hyatt_xp.RESERVATION_INFO)
        if reservation_info:
            note_1 = reservation_info.pop(0)
            note_1 = strip_list(
                note_1.xpath('./table/tr/td/table/tr[2]/td/text()')
            )
            note_2 = reservation_info.pop()
            note_2 = strip_list(note_2.xpath('.//td/text()'))
            note = list(chain([note_1, note_2]))
            if note:
                result['notice'] = note
            else:
                self.logger.error('notice is empty %s', self._message_id)
            cancellation = reservation_info.pop()
            cancellation = cancellation.xpath(
                './table/tr/td/table/tr[2]/td/text()'
            )
            cancellation = strip_list(cancellation)
            if cancellation:
                result['cancellation_policies'] = cancellation
            else:
                self.logger.error('policies is empty %s', self._message_id)

            name_dict = {
                'Guest Name': 'guest_name',
                'Number of Adults': 'number_of_guests',
                'Room(s) Booked': 'number_of_rooms',
                'Room Type': 'room_type',
                'Type of Rate': 'rate_type',
                'SERVICE CHARGE': 'service_charge',
                'SALES TAX': 'taxes_fee',
            }
            for i in reservation_info:
                title = strip_str(take_first(i, './b/text()'))
                value = '\n'.join(strip_list(i.xpath('./text()')))
                if title and value:
                    if 'Room Description' in title:
                        result['room_tips'] = [value.strip('- ')]
                    elif 'Rate Information' in title:
                        result['rate_tips'] = remove_space(value)
                    elif 'Policies' in title:
                        result['policies'] = strip_list(value.split('\n'))
                    elif title in name_dict:
                        result[name_dict[title]] = value
                    else:
                        self.logger.warning(
                            '%s is %s %s', title, value, self._message_id
                        )
        else:
            self.logger.error(
                'reservation_information is empty %s', self._message_id
            )
        return result
