# coding: utf-8
"""Created by LiuHao
"""

from lxml import etree
from w3lib.html import remove_tags
from tasks.xpath import spg_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import to_dict
from tasks.utils.html import remove_space
from tasks.utils.html import take_last
from tasks.utils.time import DateTime
from tasks.utils.time import to_timezone

from tasks.parsers import HotelOrderParser


class SPGPaser(HotelOrderParser):

    """SPG"""

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if not sender.endswith("confirm.starwoodhotels.com>"):
            return False
        if 'Your reservation has been confirmed' not in subject:
            return False

        _snippet = 'View in a browser for up-to-date reservation information'
        if not snippet.startswith(_snippet):
            return False
        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        related_link = self._etree.xpath(spg_xp.RELATED_LINKS)
        related_text = strip_list(self._etree.xpath(spg_xp.RELATED_TEXT))
        if related_link:
            result['related_links'] = to_dict(related_text, related_link)
        else:
            self.logger.error('related_links is empty %s', self._message_id)

        hotel_name = strip_str(take_first(self._etree, spg_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        address = self._etree.xpath(spg_xp.ADDRESS)
        if address and len(address) >= 3:
            address = remove_space(' '.join(address[:2]).replace('\t', ''))
            result['address'] = address
        else:
            address = ''
            self.logger.error('address is empty %s', self._message_id)

        tel = strip_str(take_first(self._etree, spg_xp.PHONE))
        if tel:
            result['telephone'] = tel
        else:
            self.logger.error('telephone is empty %s', self._message_id)
        fax = strip_str(take_first(self._etree, spg_xp.FAX))
        if fax:
            result['fax'] = fax.split(': ')[-1]
        else:
            self.logger.warning('fax is empty %s', self._message_id)

        confirm_num = strip_list(self._etree.xpath(spg_xp.ADDRESS))
        if confirm_num and len(confirm_num) >= 4:
            result['confirm_code'] = confirm_num[3]
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        reservation_explanation = strip_str(
            take_first(self._etree, spg_xp.EXPLANATION)
        )
        if reservation_explanation:
            result['tip'] = reservation_explanation
        else:
            self.logger.warning(
                'reservation_explanation is empty %s', self._message_id
            )

        reservation_keys = strip_list(
            self._etree.xpath(spg_xp.RESERVATION_INFO_KEYS)
        )
        reservation_values = strip_list(
            self._etree.xpath(spg_xp.RESERVATION_INFO_VALUES)
        )
        if reservation_keys and reservation_values:
            tz = to_timezone(address)
            for i, j in zip(reservation_keys, reservation_values):
                if 'Check In' in i:
                    check_in_date = j.split('\n')[0]
                    check_in_time = j.split(' - ')[-1].strip('  *')
                    if check_in_time:
                        result['check_in_time'] = check_in_time
                    else:
                        self.logger.error(
                            'check_in_time is empty %s', self._message_id
                        )
                    if check_in_date:
                        result['check_in_date'] = check_in_date
                        formatted = DateTime(check_in_date,
                                             'DD-MMM-YYYY').tz_to_datetime(tz)
                        if formatted:
                            result['check_in_date_formatted'] = formatted
                        else:
                            self.logger.error(
                                'check_in_date_formatted is empty %s',
                                self._message_id
                            )
                    else:
                        self.logger.error(
                            'check_in_date is empty %s', self._message_id
                        )
                elif 'Check Out' in i:
                    check_out_date = j.split('\n')[0]
                    check_out_time = j.split(' - ')[-1].strip('  *')
                    if check_out_time:
                        result['check_out_time'] = check_out_time
                    else:
                        self.logger.error(
                            'check_out_time is empty %s', self._message_id
                        )
                    if check_out_date:
                        result['check_out_date'] = check_out_date
                        formatted = DateTime(check_out_date,
                                             'DD-MMM-YYYY').tz_to_datetime(tz)
                        if formatted:
                            result['check_out_date_formatted'] = formatted
                        else:
                            self.logger.error(
                                'check_out_date_formatted is empty %s',
                                self._message_id
                            )
                    else:
                        self.logger.error(
                            'check_in_date is empty %s', self._message_id
                        )
                elif 'Number of Guests' in i:
                    result['number_of_guests'] = j
                elif 'Number of Rooms' in i:
                    result['number_of_rooms'] = j
                else:
                    self.logger.warning(' %s is %s %s', i, j, self._message_id)
        else:
            self.logger.error(
                'reservation_information is empty %s', self._message_id
            )

        accommodation_keys = strip_list(
            self._etree.xpath(spg_xp.ACCOMMODATION_INFO_KEYS)
        )
        accommodation_values = \
            strip_list(self._etree.xpath(spg_xp.ACCOMMODATION_INFO_VALUES))
        if accommodation_keys and accommodation_values:
            for i, j in zip(accommodation_keys, accommodation_values):
                if 'Guest Name' in i:
                    result['guest_name'] = j  # TODO: (LensHo) 多个名字
                elif 'Number of Adults' in i:
                    result['number_of_adults'] = j
                elif 'Number of Children' in i:
                    result['number_of_children'] = j
                else:
                    self.logger.warning('%s is %s %s', i, j, self._message_id)
        else:
            self.logger.error('accommodation is empty %s', self._message_id)

        accommodation_details = strip_list(
            self._etree.xpath(spg_xp.ACCOMMODATION_DETAILS)
        )
        if accommodation_details:
            result['room_tips'] = accommodation_details
        else:
            self.logger.warning(
                'accommodation_details is empty %s', self._message_id
            )

        room_description = strip_str(
            take_last(self._etree, spg_xp.ROOM_DESCRIPTION)
        )
        if room_description:
            bed_type = room_description.split(': ')[-1]
            result['bed_type'] = bed_type
            room_tips = result.get('room_tips')
            if room_tips:
                result['room_tips'].append(room_description)
            else:
                result['room_tips'] = [room_description]
        else:
            self.logger.warning('room_tip is empty %s', self._message_id)

        currency = strip_str(take_first(self._etree, spg_xp.CURRENCY))
        if not currency:
            self.logger.error('currency is empty %s', self._message_id)
        room_rate_avg = strip_str(
            take_first(self._etree, spg_xp.PER_ROOM_RATE)
        )
        if room_rate_avg:
            result['price'] = ' '.join([room_rate_avg, currency])
        else:
            self.logger.error('room_rate_avg is empty %s', self._message_id)
        estimated_avg = strip_str(
            take_first(self._etree, spg_xp.ESTIMATED_TOTAL_1)
        )
        if estimated_avg:
            result['total_cost'] = ' '.join([estimated_avg, currency])
        else:
            self.logger.error('total is empty %s', self._message_id)
        other_fees_name = strip_list(self._etree.xpath(spg_xp.OTHER_COST_KEYS))
        other_fees_avg = strip_list(
            self._etree.xpath(spg_xp.OTHER_COST_VALUES_1)
        )
        if other_fees_name and other_fees_avg:
            other_fees_name = other_fees_name[::2]
            other_fees_value = map(remove_space, other_fees_name[1::2])
            other_fees_avg = other_fees_avg[1::2]
            other_fees = zip(other_fees_name, other_fees_value, other_fees_avg)
            for name, fee, avg in other_fees:
                if 'Value Added Tax' in name:
                    result['taxes_fee'] = ' '.join([fee, avg, currency])
                elif 'Service Charge' in name:
                    result['service_charge'] = ' '.join([fee, avg, currency])
                else:
                    self.logger.warning(
                        '%s is %s %s', name, fee + avg + currency,
                        self._message_id
                    )
        else:
            self.logger.error('other_fee is empty %s', self._message_id)

        price_explanation = strip_str(
            take_first(self._etree, spg_xp.EXPLANATION_PRICE)
        )
        if price_explanation:
            result['price_tips'] = [price_explanation]
        else:
            self.logger.warning(
                'price_explanation is empty %s', self._message_id
            )

        policies = strip_list(self._etree.xpath(spg_xp.CANCELLATION))
        if policies:
            result['policies'] = policies
        else:
            self.logger.error('policies is empty %s', self._message_id)

        privacy_links = self._etree.xpath(spg_xp.PRIVACY_LINK)
        privacy_texts = strip_list(self._etree.xpath(spg_xp.PRIVACY_LINK_TEXT))
        privacy = take_first(self._etree, spg_xp.PRIVACY)
        if privacy is not None:
            result['privacies'] = [{
                'text': strip_str(remove_tags(etree.tostring(privacy))),
                'links': to_dict(privacy_texts, privacy_links)
            }]
        else:
            self.logger.error('privacy is empty %s', self._message_id)

        disclosure = self._etree.xpath(spg_xp.DISCLOSURE)
        if disclosure:
            disclosure = disclosure[0].xpath('./text() | ./*')
            a = []
            for i in disclosure:
                if i == '\n' or not isinstance(i, str) and i.tag == 'br':
                    continue
                elif not isinstance(i, str) and i.tag == 'strong':
                    b = {'name': i.text, 'text': '', 'links': []}
                    if a and not a[-1]['links']:
                        del a[-1]['links']
                    a.append(b)

                elif isinstance(i, str):
                    if a:
                        a[-1]['text'] = ''.join([a[-1]['text'], i])
                    else:
                        self.logger.error(
                            'string before strong %s %s', i, self._message_id
                        )
                elif i.tag == 'a':
                    if a:
                        a[-1]['text'] = ''.join([a[-1]['text'], i.text])
                        b = {'name': i.text, 'value': i.get('href')}
                        a[-1]['links'].append(b)
                    else:
                        self.logger.error(
                            'tag before strong %s %s', i.tag, self._message_id
                        )
                else:
                    self.logger.error(
                        'unknown tag %s %s', i.tag, self._message_id
                    )
            if a and not a[-1]['links']:
                del a[-1]['links']
                result['disclosures'] = a
            else:
                self.logger.error('disclosure is empty %s', self._message_id)
        else:
            self.logger.error('disclosure_raw is empty %s', self._message_id)
        return result
