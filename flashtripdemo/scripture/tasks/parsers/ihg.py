# coding: utf-8
"""Created by LiuHao"""

from tasks.xpath import ihg_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import HotelOrderParser


class IHGParser(HotelOrderParser):

    """IHG
    """

    @classmethod
    def validate(cls, sender, subject, snippet):
        if not sender.endswith('ihg.com>'):
            return False
        if not subject.startswith('Your Reservation Confirmation'):
            return False
        if not (
            snippet.startswith('Thank you for booking with') and
            'IHG' in snippet
        ):
            return False
        return True

    def _parse(self):  # pylint: disable=R0912,R0915
        result = self._order
        hotel_name = strip_str(take_first(self._etree, ihg_xp.HOTEL_NAME))
        if hotel_name:
            result['hotel_name'] = hotel_name
        else:
            self.logger.error('hotel_name is empty %s', self._message_id)

        confirm_num = strip_str(take_first(self._etree, ihg_xp.CONFIRM_NUM))
        if confirm_num:
            result['confirm_code'] = confirm_num
        else:
            self.logger.error('confirm_number is empty %s', self._message_id)

        address = ', '.join(strip_list(self._etree.xpath(ihg_xp.ADDRESS)))
        if address:
            result['address'] = address
        else:
            self.logger.error('address is empty %s', self._message_id)

        telephone = strip_str(take_first(self._etree, ihg_xp.PHONE))
        if telephone:
            result['telephone'] = telephone.split(': ')[-1]
        else:
            self.logger.error('telephone is empty %s', self._message_id)

        tz = to_timezone(address)
        check_in_date = strip_str(
            take_first(self._etree, ihg_xp.CHECK_IN_DATE)
        )
        if check_in_date:
            result['check_in_date'] = check_in_date
        else:
            self.logger.error('check_in_date is empty %s', self._message_id)
        check_out_date = strip_str(
            take_first(self._etree, ihg_xp.CHECK_OUT_DATE)
        )
        if check_out_date:
            result['check_out_date'] = check_out_date
        else:
            self.logger.error('check_out_date is empty %s', self._message_id)
        check_in_time = strip_str(
            take_first(self._etree, ihg_xp.CHECK_IN_TIME)
        )
        if check_in_time:
            result['check_in_time'] = check_in_time
        else:
            self.logger.error('check_in_time is empty %s', self._message_id)
        check_out_time = strip_str(
            take_first(self._etree, ihg_xp.CHECK_OUT_TIME)
        )
        if check_out_time:
            result['check_out_time'] = check_out_time
        else:
            self.logger.error('check_out_time is empty %s', self._message_id)
        check_in_date_formatted = DateTime(check_in_date,
                                           'MM/DD/YY').tz_to_datetime(tz)  #
        if check_in_date_formatted:
            result['check_in_date_formatted'] = check_in_date_formatted
        check_out_date_formatted = DateTime(check_out_date,
                                            'MM/DD/YY').tz_to_datetime(tz)
        if check_out_date_formatted:
            result['check_out_date_formatted'] = check_out_date_formatted

        guest_name = strip_str(take_first(self._etree, ihg_xp.GUEST_NAME))
        if guest_name:
            result['guest_name'] = guest_name
        else:
            self.logger.error('guest_name is empty %s', self._message_id)

        room_num = strip_str(take_first(self._etree, ihg_xp.ROOMS))
        guest_num = strip_str(take_first(self._etree, ihg_xp.ADULTS))
        room_type = strip_str(take_first(self._etree, ihg_xp.ROOM_TYPE))
        if room_num:
            result['number_of_rooms'] = room_num
        else:
            self.logger.error('number of rooms is empty %s', self._message_id)
        if guest_num:
            result['number_of_guests'] = guest_num
        else:
            self.logger.error('number of guests is empty %s', self._message_id)
        if room_type:
            result['room_type'] = room_type
        else:
            self.logger.error('room_type is empty %s', self._message_id)

        price_des = strip_str(take_first(self._etree, ihg_xp.RATE_NOTICE))
        if price_des:
            result['price_tips'] = [price_des]
        else:
            self.logger.error(
                'price_description is empty %s', self._message_id
            )

        rate_names = strip_list(self._etree.xpath(ihg_xp.RATE_NAME))
        rate_values = strip_list(self._etree.xpath(ihg_xp.RATE_VALUE))
        if rate_values and rate_names:
            _, price = rate_names.pop(0), rate_values.pop(0)  # noqa
            result['price'] = price
            name_dict = {
                'Service Charge': 'service_charge',
                'Total Taxes': 'taxes_fee',
                'Estimated Total Price': 'total_cost'
            }
            for i, j in zip(rate_names, rate_values):
                if i in name_dict:
                    result[name_dict[i]] = j
                else:
                    self.logger.warning(' %s is %s %s', i, j, self._message_id)

        cancellation_name = strip_str(
            take_first(self._etree, ihg_xp.CANCELLATION_NAME)
        )
        cancellation_value = strip_str(
            take_first(self._etree, ihg_xp.CANCELLATION_VALUE)
        )
        if 'Cancellation' in cancellation_name and cancellation_value:
            result['cancellation_policy'] = cancellation_value
        else:
            self.logger.error(
                'cancellation_policy is empty %s', self._message_id
            )
        rate_des_name = strip_str(
            take_first(self._etree, ihg_xp.RATE_DES_NAME)
        )
        rate_des_value = strip_str(
            take_first(self._etree, ihg_xp.RATE_DES_VALUE)
        )
        if 'Rate' in rate_des_name and rate_des_value:
            result['rate_tip'] = rate_des_value
        else:
            self.logger.error('rate_tip is empty %s', self._message_id)

        hotel_link = take_first(self._etree, ihg_xp.HOTEL_LINK)
        if hotel_link:
            result['hotel_link'] = hotel_link
        else:
            self.logger.error('hotel_link is empty %s', self._message_id)
        preference_link = take_first(self._etree, ihg_xp.PREFERENCE_LINK)
        if preference_link:
            result['preference_link'] = preference_link
        else:
            self.logger.error('preference_link is empty %s', self._message_id)

        related_links = self._etree.xpath(ihg_xp.RELATED_LINK)
        if related_links:
            related = []
            for i in related_links:
                link = i.xpath('./a/@href')
                text = i.xpath('./a/text()')
                if link and text:
                    if 'CANCEL' in text[0]:
                        result['cancellation_link'] = link
                    elif 'MODIFY' in text[0]:
                        result['modify_link'] = link
                    elif 'DOWNLOAD' in text[0]:
                        pass
                    else:
                        related.append({'name': text[0], 'value': link})
            if related:
                result['related_links'] = related
            else:
                self.logger.error(
                    'related_links is empty %s', self._message_id
                )

        notice = self._etree.xpath(ihg_xp.NOTICE)
        if notice:
            notice = notice[0].xpath('./text() | ./*')
            a = []
            name_dict = {
                'Early Departure Fee:': 'early_departure_fee',
                'Daily Valet Parking Fee:': 'daily_valet_parking_fee',
                'Pet Policy:': 'pet_policy',
                'Payment Card Authorization Form:': 'payment_card_auth_form'
            }
            for i in notice:
                if not isinstance(i, str) and i.tag == 'br':
                    continue
                elif not isinstance(i, str) and i.tag == 'span':
                    if a and not a[-1]['links'] == 0:
                        del a[-1]['links']
                    span = i.xpath('./span/text()')
                    if span:
                        try:
                            name = name_dict[span[0]]
                            b = {'text': '', 'links': []}
                            for j in i.xpath('./text() | ./*'):
                                if isinstance(j, str):
                                    b['text'] = ''.join([b['text'], j])
                                elif not isinstance(j, str) and j.tag == 'a':
                                    b['text'] = ''.join([b['text'], j.text])
                                    c = {
                                        'name': j.text,
                                        'value': j.get('href')
                                    }
                                    b['links'].append(c)
                                else:
                                    pass
                            result[name] = b
                            a.append(b)
                        except KeyError as e:
                            self.logger.exception(e)
                            self.logger.warning(
                                'unknown key %s %s', span[0], self._message_id
                            )
                    else:
                        try:
                            name = name_dict[i.text]
                            b = {'text': '', 'links': []}
                            result[name] = b
                            a.append(b)
                        except KeyError as exc:
                            self.logger.exception(exc)
                            self.logger.warning(
                                'unknown key %s %s', name_dict[i.text],
                                self._message_id
                            )
                elif isinstance(i, str):
                    if a:
                        a[-1]['text'] = ''.join([a[-1]['text'], i])
                    else:
                        self.logger.error(
                            'string before span %s %s', i, self._message_id
                        )
                else:
                    self.logger.warning(
                        'unknown tag %s %s', i.tag, self._message_id
                    )
            if a and not a[-1]['links']:
                del a[-1]['links']
        else:
            self.logger.error('notice is empty %s', self._message_id)
        tip = take_first(self._etree, ihg_xp.ADDITION_FEE)
        if tip:
            result['notice'] = tip
        else:
            self.logger.warning(
                'hotel_information_notice is empty %s', self._message_id
            )
        return result
