# coding: utf-8

from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import unpack

from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.xpath import travelzoo_xp as tz_xp
from tasks.parsers import HotelOrderParser
from tasks.errors.parse_error import MissingColumnError


class TravelzooParser(HotelOrderParser):

    """travelzoo.com
    """
    name_dict = {
        'Booking Conditions': 'booking_conditions',
        'Cancellation Policy': 'cancellation_policies',
        'Check-in': 'check_in_policies',
        'Checkout': 'check_out_policies',
        'Children and additional guests': 'additional_guest_policies',
        'Pets': 'pets_policies',
        'Additional details': 'additional_details',
        'Getting there': 'getting_there'
    }

    @classmethod
    def validate(cls, sender, subject, snippet):
        if not (
            sender.strip().startswith('Travelzoo') and
            sender.strip('>').endswith('hotels@travelzoo.com')
        ):
            return False

        if not subject.startswith('Travelzoo Confirmation'):
            return False

        if 'BOOKING CONFIRMATION' not in snippet:
            return False

        return True

    def _parse(self):
        result = self._order
        result['hotel_name'] = strip_str(
            take_first(self._etree, tz_xp.HOTEL_NAME)
        )
        if not result['hotel_name']:
            raise MissingColumnError('hotel_name', self._message_id)

        result['address'] = ', '.join([
            i.strip(',') for i in self._etree.xpath(tz_xp.ADDRESS)
        ])
        if not result['address']:
            raise MissingColumnError('address', self._message_id)

        result['telephone'] = take_first(self._etree, tz_xp.PHONE)
        if not result['telephone']:
            raise MissingColumnError('telephone', self._message_id)

        result.set('hotel_link', take_first(self._etree, tz_xp.WEBSITE))

        name_code = strip_list(self._etree.xpath(tz_xp.NAME_CODE))
        if len(name_code) < 3:
            raise MissingColumnError(
                'guest_name or confirm_code', self._message_id
            )
        result['guest_name'] = name_code.pop(0)
        result['travelzoo_reference_code'] = name_code.pop(0)
        result['confirm_code'] = name_code.pop(0)
        # 有可能有其他额外确认信息
        if name_code:
            self.logger.warning(
                'other confirmation: %s %s', name_code.pop(), self._message_id
            )

        date = strip_str(take_first(self._etree, tz_xp.DATE))
        if not date:
            raise MissingColumnError('date is empty', self._message_id)

        check_in_date, check_out_date = unpack(date.split(' - '))
        if not check_in_date or not check_out_date:
            raise MissingColumnError(
                'check_in_date ot checkout_date', self._message_id
            )

        tz = to_timezone(result.get('address'))
        date_format = 'MMM DD, YYYY'
        result['check_in_date'] = check_in_date
        result['check_in_date_formatted'] = DateTime(
            check_in_date, date_format
        ).tz_to_datetime(tz)

        if not result['check_in_date_formatted']:
            result.pop('check_in_date_formatted')
            self.logger.error(
                'check_in_date_formatted is empty %s', self._message_id
            )

        result['check_out_date'] = check_out_date
        result['check_out_date_formatted'] = DateTime(
            check_out_date, date_format
        ).tz_to_datetime(tz)

        if not result['check_out_date_formatted']:
            result.pop('check_out_date_formatted')
            self.logger.error(
                'check_out_date_formatted is empty %s', self._message_id
            )

        result['number_of_guests'
               ] = strip_str(take_first(self._etree, tz_xp.GUEST_NUM))
        if not result['number_of_guests']:
            result.pop('number_of_guests')
            self.logger.error(
                'number of guests is empty %s', self._message_id
            )

        roomtype_price = strip_list(self._etree.xpath(tz_xp.ROOMTYPE_PRICE))
        if len(roomtype_price) >= 2:
            result['room_type'] = roomtype_price.pop(0)
            price = roomtype_price.pop(0)
            result['price'] = price.split('- ')[-1]
            # 可能会有其他信息
            if roomtype_price:
                self.logger.warning(
                    'other price: %s %s',
                    roomtype_price.pop(), self._message_id
                )
        else:
            self.logger.error('price is empty %s', self._message_id)

        payment = self._etree.xpath(tz_xp.PAYMENT)
        if payment:
            for item in payment:
                name = strip_str(take_first(item, './td[1]/text()'))
                cost = strip_str(take_first(item, './td[2]/text()'))
                if not name or not cost:
                    continue
                if 'Night' in name:
                    result['number_of_nights'] = name
                    result['total_without_taxes'] = cost
                elif 'tax' in name:
                    result['taxes_name'] = name
                    result['taxes_fee'] = cost
                elif 'Total' in name:
                    result['total_cost'] = cost
                # 可能会有其他价格信息
                else:
                    self.logger.warning(
                        'payment: %s is %s %s', name, cost, self._message_id
                    )
        else:
            self.logger.error('payment is empty %s', self._message_id)

        policies = self._etree.xpath('//b')
        if policies:
            for policy in policies:
                name = strip_str(take_first(policy, './text()'))
                value = strip_list(policy.xpath('../text()'))
                if name in self.name_dict:
                    result[self.name_dict[name]] = value
                elif result['hotel_name'] in name:
                    pass
                else:
                    self.logger.warning(
                        'policy: %s is %s %s', name, value, self._message_id
                    )
        else:
            self.logger.error('policies is empty %s', self._message_id)

        result['cancellation_link'] = take_first(
            self._etree, tz_xp.CANCEL_LINK
        )
        if not result['cancellation_link']:
            result.pop('cancellation_link')
            self.logger.error(
                'cancellation link is empty %s', self._message_id
            )

        contact = self._etree.xpath(tz_xp.CONTACT)
        if contact:
            result['contact_information'] = []
            for item in contact:
                link = take_first(item, './a/@href')
                if 'tel' in link:
                    region = take_first(item, './text()')
                    tel = take_first(item, './a/text()')
                    if region and tel:
                        result['contact_information'].append({
                            'name': region,
                            'value': tel
                        })

            if not result['contact_information']:
                result.pop('contact_information')
                self.logger.warning(
                    'contact information is empty %s', self._message_id
                )
        else:
            self.logger.warning('contact is empty %s', self._message_id)

        return result
