# coding: utf-8
"""Created by LiuHao
"""
from itertools import chain

from lxml import etree
from w3lib.html import replace_tags
from tasks.xpath import marriott_xp
from tasks.utils.html import take_first
from tasks.utils.html import filter_dict_value
from tasks.utils.html import group
from tasks.utils.html import unpack
from tasks.utils.html import to_dict
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import HotelOrderParser


class MarriottParser(HotelOrderParser):

    """marriott
    """

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str):
        if 'Marriott Reservations' not in sender:
            return False

        if not subject.startswith('Reservation Confirmation'):
            return False

        if not snippet.startswith(
            'Please review your reservation details and '
            'keep for your records.'
        ):
            return False

        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        hotel_name = strip_str(take_first(self._etree, marriott_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        address = strip_str(take_first(self._etree, marriott_xp.ADDRESS))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        tel = take_first(self._etree, marriott_xp.PHONE)
        if tel:
            result['telephone'] = tel
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        confirm_num = take_first(self._etree, marriott_xp.CONFIRM_NUM)
        if confirm_num:
            confirm_num = confirm_num.split(': ')[-1]
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        guest = take_first(self._etree, marriott_xp.GUEST)
        if guest:
            guest = guest.split('For ')[-1]
            result['guest_name'] = guest
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        check_in_out_time = strip_list(
            self._etree.xpath(marriott_xp.CHECK_IN_OUT_TIME)
        )
        if len(check_in_out_time) == 2:
            result['check_in_time'] = check_in_out_time[0]
            result['check_out_time'] = check_in_out_time[1]
        else:
            self.logger.error(
                'check_in_date and check_out_time is empty %s',
                self._message_id
            )
        check_in_out_date = strip_list(
            self._etree.xpath(marriott_xp.CHECK_IN_OUT_DATE)
        )
        check_in_date, check_out_date = unpack(check_in_out_date)
        if check_in_date and check_out_date:
            result['check_in_date'] = check_in_date
            result['check_out_date'] = check_out_date
            tz = to_timezone(address)
            check_in_date_formatted = \
                DateTime(check_in_date, 'MMMM DD, YYYY').tz_to_datetime(tz)
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            else:
                self.logger.error(
                    'check_in_date_formatted is empty %s', self._message_id
                )
            check_out_date_formatted = \
                DateTime(check_out_date, 'MMMM DD, YYYY').tz_to_datetime(tz)
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

        related_links = self._etree.xpath(marriott_xp.RELATED_LINK)
        related_text = self._etree.xpath(marriott_xp.RELATED_TEXT)
        related_links = to_dict(related_text, related_links)
        if related_links:
            related = []
            for i in related_links:
                if 'Hotel Website' in i.get('name'):
                    result['hotel_link'] = i.get('value')
                    related_links.remove(i)
                elif 'Map & Directions' in i.get('name'):
                    result['map_link'] = i.get('value')
                    related_links.remove(i)
                elif 'Cancel' in i.get('name'):
                    result['cancellation_link'] = i.get('value')
                else:
                    related.append(i)
            if related:
                result['related_links'] = related_links
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        room_type = take_first(self._etree, marriott_xp.ROOM_TYPE)
        room_type_value = take_first(self._etree, marriott_xp.ROOM_TYPE_VALUE)
        if room_type and room_type_value:
            result['room_type'] = room_type_value
        else:
            self.logger.error('room_type is empty %s', self._message_id)
        room_num_guest = strip_list(
            self._etree.xpath(marriott_xp.ROOM_NUM_GUEST)
        )
        room_num_guest_name, room_num_guest_value = group(room_num_guest)
        if room_num_guest_name and room_num_guest_value:
            for i, j in zip(room_num_guest_name, room_num_guest_value):
                if 'NUMBER OF ROOMS' in i:
                    result['number_of_rooms'] = j
                elif 'GUESTS PER ROOM' in i:
                    continue
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('room number is empty %s', self._message_id)

        guarantee = strip_list(
            self._etree.xpath(marriott_xp.GUARANTEED_METHOD)
        )
        if guarantee:
            result['guarantee_policies'] = [guarantee[-1]]
        else:
            self.logger.error('guarantee is empty %s', self._message_id)
        price_des = strip_str(
            take_first(self._etree, marriott_xp.CHARGE_DESCRIPTION)
        )
        if price_des:
            result['price_tips'] = [price_des]
        else:
            self.logger.warning(
                'price_description is empty %s', self._message_id
            )

        notice = strip_list(self._etree.xpath(marriott_xp.HOTEL_ALERT))
        if notice:
            result['notice'] = notice
        else:
            self.logger.error('notice is empty %s', self._message_id)

        rates = strip_list(self._etree.xpath(marriott_xp.RATES))
        if rates:
            rates_type = rates.pop()
            if 'Best Available rate' in rates_type:
                nights = sum([int(i.split(' ')[0]) for i in rates[1::3]])
                price = sum([float(i.split(' ')[0]) for i in rates[2::3]])
                currency = ' ' + rates[2].split(' ')[-1]
                result['price'] = str(round(price / nights, 2)) + currency
            else:
                result['price'] = rates[-1]
                self.logger.error('price is empty %s', self._message_id)
        else:
            self.logger.error('rates is empty %s', self._message_id)
        taxes = strip_list(self._etree.xpath(marriott_xp.TAXES))
        name, value = unpack(taxes)
        if name and value:
            if 'TAXES & FEES' in name:
                result['taxes_fee'] = taxes[-1]
            else:
                self.logger.error('%s is %s %s', name, value, self._message_id)
        else:
            self.logger.error('taxes is empty %s', self._message_id)
        total = strip_list(self._etree.xpath(marriott_xp.TOTAL))
        name, value = unpack(total)
        if total:
            if 'Total' in name:
                result['total_cost'] = total[-1]
            else:
                self.logger.error('%s is %s %s', name, value, self._message_id)
        else:
            self.logger.error('total_price is empty %s', self._message_id)
        other_charge = strip_list(self._etree.xpath(marriott_xp.OTHER_CHARGE))
        other_charge = [
            i for i in other_charge if i != '\u2022' and i != 'Other Charges'
        ]
        if other_charge:
            result['other_charges'] = other_charge
        else:
            self.logger.warning('other_charge is empty %s', self._message_id)

        cancellation = take_first(
            self._etree, marriott_xp.RATE_CANCELLATION_DETAILS
        )
        if cancellation is not None:
            cancellation = replace_tags(etree.tostring(cancellation))
            cancellation = cancellation.split('&#8226; \n')
            result['cancellation_policies'] = strip_list(cancellation)
        else:
            self.logger.error(
                'cancellation_policy is empty %s', self._message_id
            )

        rate_guarantee_title = take_first(
            self._etree, marriott_xp.RATE_GUARANTEE_TITLE
        )
        rate_guarantee = strip_list(
            self._etree.xpath(marriott_xp.RATE_GUARANTEE)
        )
        rate_guarantee = [i for i in rate_guarantee if i != '\u2022']
        if rate_guarantee and 'GUARANTEE' in rate_guarantee_title:
            guarantee = result.get('guarantee_policies')
            if guarantee:
                result['guarantee_policies'].extend(rate_guarantee)
            else:
                result['guarantee_policies'] = rate_guarantee
        else:
            self.logger.error('rate guarantee is empty %s', self._message_id)

        addition_title = take_first(
            self._etree, marriott_xp.ADDITION_INFO_TITLE
        )
        addition_link = strip_list(
            self._etree.xpath(marriott_xp.ADDITION_INFO_LINK)
        )
        addition_text = strip_list(
            self._etree.xpath(marriott_xp.ADDITION_INFO_TEXT)
        )
        if addition_text and 'ADDITIONAL' in addition_title:
            result['additional_information'] = to_dict(
                addition_text, addition_link
            )
        else:
            self.logger.error(
                'additional information is empty %s', self._message_id
            )

        contact_links = self._etree.xpath(marriott_xp.CONTACT_LINK)
        contact_texts = strip_list(self._etree.xpath(marriott_xp.CONTACT_TEXT))
        contact = strip_list(self._etree.xpath(marriott_xp.CONTACT_1))
        contact_1 = [{'name': i, 'value': i} for i in contact]
        contact = chain(to_dict(contact_texts, contact_links), contact_1)
        contact = filter_dict_value(contact)
        if contact:
            result['contact_information'] = contact
        return result
