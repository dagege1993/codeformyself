# coding: utf-8
"""Create by LiuHao
"""

from lxml import etree
from w3lib.html import remove_tags
from tasks.xpath import accor_xp
from tasks.parsers import HotelOrderParser
from tasks.utils.html import take_first, strip_str, strip_list, to_dict
from tasks.utils.time import to_timezone, DateTime


class Accor(HotelOrderParser):

    """accor.com
    """

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if not (
            sender.startswith('AccorHotels ') and
            sender.strip('>').endswith('accor-mail.com')
        ):
            return False

        if not subject.startswith('Confirmation of your reservation:'):
            return False

        if 'Please see below for details of your reservation.' not in snippet:
            return False

        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        guest_name = strip_str(take_first(self._etree, accor_xp.GUEST))
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        confirm_num = strip_str(take_first(self._etree, accor_xp.CONFIRM_NUM))
        if confirm_num:
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        address = ', '.join(strip_list(self._etree.xpath(accor_xp.ADDRESS)))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        check_in_out_date = strip_str(
            take_first(
                self._etree,
                accor_xp.CHECK_IN_OUT_DATE
            )
        ) \
            .split(' ')
        if not check_in_out_date:
            self.logger.error(
                'check_in_out_date is empty %s', self._message_id
            )
        if len(check_in_out_date) == 4:
            check_in_date = check_in_out_date[1]
            check_out_date = check_in_out_date[-1]
            result['check_in_date'] = check_in_date
            result['check_out_date'] = check_out_date
            tz = to_timezone(address)
            check_in_date_formatted = DateTime(check_in_date, 'MM/DD/YYYY'
                                               ).tz_to_datetime(tz)
            if check_in_date_formatted:
                result['check_in_date_formatted'] = check_in_date_formatted
            check_out_date_formatted = DateTime(
                check_out_date,
                'MM/DD/YYYY'
            ) \
                .tz_to_datetime(tz)
            if check_out_date_formatted:
                result['check_out_date_formatted'] = check_out_date_formatted

        hotel_link = take_first(self._etree, accor_xp.HOTEL_LINK)
        if hotel_link:
            result['hotel_link'] = hotel_link
        else:
            self.logger.error('hotel_link is empty %s', self._message_id)
        map_link = take_first(self._etree, accor_xp.MAP_LINK)
        if map_link:
            result['map_link'] = map_link
        else:
            self.logger.error('map_link is empty %s', self._message_id)
        related_links = self._etree.xpath(accor_xp.RELATED_LINKS)
        if not related_links:
            self.logger.error('related_links is empty %s', self._message_id)
        related_texts = strip_list(self._etree.xpath(accor_xp.RELATED_TEXTS))
        related_links = to_dict(related_texts, related_links)
        if related_links:
            result['related_links'] = related_links
            for i in related_links:
                if i.get('name') in 'Cancel':
                    related_links.remove(i)
                    result['cancellation_link'] = i.get('value')
                    break

        hotel_name = strip_str(take_first(self._etree, accor_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        phone_email = strip_list(self._etree.xpath(accor_xp.PHONE_EMAIL))
        phone = phone_email.pop(0) if phone_email else ''
        email = phone_email.pop(0) if phone_email else ''
        if phone:
            result['telephone'] = phone.split(': ')[-1]
        else:
            self.logger.error('telephone is empty %s', self._message_id)
        if email:
            result['email'] = email
        else:
            self.logger.warning('email is empty %s', self._message_id)

        bed_type = strip_str(take_first(self._etree, accor_xp.BED_TYPE))
        if bed_type:
            result['bed_type'] = bed_type
        else:
            self.logger.error('bed_type is empty %s', self._message_id)

        room_detail = strip_str(take_first(self._etree, accor_xp.DETAILS))
        if room_detail:
            result['room_tips'] = [room_detail]
        else:
            self.logger.error('room_details is empty %s', self._message_id)

        stay = strip_str(take_first(self._etree, accor_xp.STAY))
        if stay:
            days = stay.split(',  ')[-1].split(' ')[0]
            result['number_of_rooms'] = stay.split(' ')[0]
            result['number_of_nights'] = stay.split(', ')[-1]
        else:
            days = ''
            self.logger.error('stay is empty %s', self._message_id)

        room_price_values = strip_list(
            self._etree.xpath(accor_xp.ROOM_PRICE_VALUE)
        )
        if room_price_values:
            price_sum = 0
            currency = ''
            for i in room_price_values:
                price_sum += float(i.split(' ')[-1])
                currency = i.split(' ')[0] + ' '
            if days:
                result['price'] = currency + \
                    str(round(price_sum / int(days), 2))
            else:
                self.logger.error('price is empty %s', self._message_id)
        total_price_names = strip_list(
            self._etree.xpath(accor_xp.TOTAL_PRICE_NAME)
        )
        total_price_values = strip_list(
            self._etree.xpath(accor_xp.TOTAL_PRICE_VALUE)
        )
        if len(total_price_values) > 1:
            # last two --> total
            unused_total_name, total_value = total_price_values[-2:]
            result['total_cost'] = total_value
            total_price_values.pop(0)  # Total price of stay
        else:
            self.logger.error('total_price is empty %s', self._message_id)
        if total_price_names and total_price_values:
            for i, j in zip(total_price_names, total_price_values):
                if i in 'Total amount including VAT':
                    result['total_amount_including_vat'] = j
                elif i in 'Other taxes excluded':
                    result['other_taxes_excluded'] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)

        info_names = strip_list(self._etree.xpath(accor_xp.INFO_NAME))
        info_values = self._etree.xpath(accor_xp.INFO_VALUE)
        if info_values and info_names:
            name_dict = {
                'Practical information': 'practical_information',
                'Special requirements': 'your_special_requirements',
                'Sales conditions': 'sales_conditions',
                'Taxes': 'taxes-fee'
            }
            info_values = map(remove_tags, map(etree.tostring, info_values))
            for i, j in zip(info_names, strip_list(info_values)):
                if i in name_dict:
                    result[name_dict[i]] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('notice is empty %s', self._message_id)
        require = result.get('your_special_requirements')
        if require:
            result['your_special_requirements'] = [require]

        policy_names = strip_list(self._etree.xpath(accor_xp.POLICIES_NAMES))
        policy_values = strip_list(self._etree.xpath(accor_xp.POLICIES_VALUES))
        if policy_names and policy_values:
            policy_values = policy_values[2:]
            for i, j in zip(policy_names, policy_values):
                if 'Check in Policy' in i:
                    result['check_in_policies'] = [j]
                    check_in_time = str(DateTime(j, 'HH:mm').to_time())  # H
                    if check_in_time:
                        result['check_in_time'] = check_in_time
                elif 'Check out Policy' in i:
                    result['check_out_policies'] = [j]
                    check_out_time = str(DateTime(j, 'HH:mm').to_time())
                    if check_out_time:
                        result['check_out_time'] = check_out_time
                elif 'Cancellation policy' in i:
                    result['cancellation_policies'] = [j]
                elif 'Guarantee Policy' in i:
                    result['guarantee_policies'] = [j]
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        return result
