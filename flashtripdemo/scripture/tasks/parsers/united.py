# coding: utf-8
"""Created by LiuHao
"""
from lxml import etree
from w3lib.html import remove_tags
from tasks.xpath import united_xp
from tasks.utils.html import take_first
from tasks.utils.html import strip_str
from tasks.utils.html import strip_list
from tasks.utils.html import to_dict
from tasks.utils.html import filter_dict_value
from tasks.utils.time import to_timezone
from tasks.utils.time import DateTime

from tasks.parsers import FlightOrderParser


class UnitedParser(FlightOrderParser):

    """united.com
    """

    @classmethod
    def validate(cls, sender: str, subject: str, snippet: str) -> bool:
        if 'United Airlines' not in sender:
            return False
        if not sender.endswith('united.com>'):
            return False
        if 'eTicket Itinerary and Receipt for Confirmation' not in subject:
            return False
        if 'Receipt for confirmation' not in snippet:
            return False
        if 'United Airlines' not in snippet:
            return False
        return True

    def _parse(self):  # pylint: disable=R0912, R0915
        result = self._order
        confirm_number = strip_str(
            take_first(self._etree, united_xp.CONFIRM_NUM)
        )
        if confirm_number:
            result['confirm_code'] = confirm_number
        else:
            self.logger.error('conform_number is empty %s', self._message_id)

        traveler_info_values = self._etree.xpath(
            united_xp.TRAVELER_INFO_VALUES
        )
        if traveler_info_values:
            result['guest_name'] = traveler_info_values[0]
            result['ticket_number'] = traveler_info_values[1]
            if len(traveler_info_values) == 3:
                result['seats'] = traveler_info_values[2]
            elif len(traveler_info_values) == 4:
                result['frequent_flyer'] = traveler_info_values[2]
                result['seats'] = traveler_info_values[3]
            else:
                self.logger.error(
                    'traveler info increase %s', self._message_id
                )
        else:
            self.logger.error('traveler info is empty %s', self._message_id)

        names = [
            'flight_date', 'flight_number', 'class', 'depart_city',
            'arrive_city', 'plane_model'
        ]
        flight_info_divs = self._etree.xpath(united_xp.FLIGHT_INFO_VALUES)
        if flight_info_divs:
            for i, j in zip(names, flight_info_divs):
                val = j.xpath('./p/span/text() | ./span/text()')
                if val:
                    if i == 'flight_date' and len(val) == 2:
                        result['depart_date'] = val[0]
                        result['arrive_date'] = val[1]
                    elif i == 'flight_date' and len(val) == 1:
                        result['arrive_date'] = result['depart_date'] = val[0]
                    else:
                        result[i] = ' '.join(val)
        else:
            self.logger.error('flight info is empty %s', self._message_id)

        flight_time = self._etree.xpath(united_xp.FLIGHT_TIME)
        if len(flight_time) == 2:
            result['depart_time'] = flight_time[0]
            result['arrive_time'] = flight_time[1]
        else:
            self.logger.error('flight_time is empty %s', self._message_id)

        if (result.get('depart_date') and result.get('depart_time') and
                result.get('depart_city')):
            dt_depart = ' '.join([
                result['depart_date'], result['depart_time']
            ])
            tz = to_timezone(result['depart_city'])
            depart_formatted = DateTime(dt_depart,
                                        'DDMMMYY h:mm A').tz_to_datetime(tz)
            if depart_formatted:
                result['depart_datetime_formatted'] = depart_formatted
            else:
                self.logger.error(
                    'depart_datetime_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'depart_datetime_formatted is empty %s', self._message_id
            )

        if (result.get('arrive_date') and result.get('arrive_time') and
                result.get('arrive_city')):
            dt_arrive = ' '.join([
                result['arrive_date'], result['arrive_time']
            ])
            tz = to_timezone(result['arrive_city'])
            arrive_formatted = DateTime(dt_arrive,
                                        'DDMMMYY h:mm A').tz_to_datetime(tz)
            if arrive_formatted:
                result['arrive_datetime_formatted'] = arrive_formatted
            else:
                self.logger.error(
                    'arrive_datetime_formatted is empty %s', self._message_id
                )
        else:
            self.logger.error(
                'arrive_datetime_formatted is empty %s', self._message_id
            )

        currency = strip_str(take_first(self._etree, united_xp.CURRENCY))
        airfare = strip_str(take_first(self._etree, united_xp.AIRFARE_PRICE))
        if airfare:
            result['price'] = ' '.join([airfare, currency])
        else:
            self.logger.error('airfare is empty %s', self._message_id)

        tax_fee_price = strip_str(
            take_first(self._etree, united_xp.TAX_FEE_PRICE)
        )
        if tax_fee_price:
            result['taxes_fee'] = tax_fee_price
        else:
            self.logger.error('taxes fee is empty %s', self._message_id)
        per_person = strip_str(
            take_first(self._etree, united_xp.TOTAL_PER_PERSON)
        )
        if per_person:
            result['subtotal'] = ' '.join([per_person, currency])
        else:
            self.logger.error('per person is empty %s', self._message_id)
        fare_total = strip_str(take_first(self._etree, united_xp.TOTAL_PRICE))
        if fare_total:
            result['total_cost'] = ' '.join([fare_total, currency])
        else:
            self.logger.error('total fare is empty %s', self._message_id)

        operator = strip_str(take_first(self._etree, united_xp.OPERATED))
        if operator:
            result['operator'] = operator
        else:
            self.logger.error('operator is empty %s', self._message_id)
        payment_form = strip_str(
            take_first(self._etree, united_xp.PAYMENT_FORM)
        )
        if payment_form:
            result['payment_form'] = payment_form
        else:
            self.logger.error('payment_form is empty %s', self._message_id)
        tax_summary = strip_str(take_first(self._etree, united_xp.TAX_SUMMARY))
        if tax_summary:
            result['tax_summary'] = tax_summary
        else:
            self.logger.error('taxes_summary is empty %s', self._message_id)
        fare_summary = strip_str(
            take_first(self._etree, united_xp.FARE_SUMMARY)
        )
        if fare_summary:
            result['fare_summary'] = fare_summary
        else:
            self.logger.error('fare_summary is empty %s', self._message_id)
        fare_rule = strip_str(take_first(self._etree, united_xp.FARE_RULE))
        if fare_rule:
            result['fare_rule'] = fare_rule
        else:
            self.logger.error('fare_rule is empty %s', self._message_id)

        bag_fee_1 = take_first(self._etree, united_xp.BAG_FEE_1)
        bag_fee_2 = take_first(self._etree, united_xp.BAG_FEE_2)
        bag_fee_3 = take_first(self._etree, united_xp.BAG_FEE_3)
        bag_fee = strip_list([bag_fee_1, bag_fee_2, bag_fee_3])
        if bag_fee:
            result['bag_fee_summary'] = bag_fee
        else:
            self.logger.error('bag_fee_summary is empty %s', self._message_id)

        bag_names = self._etree.xpath(united_xp.BAG_FEE_TABLE_KEYS)
        bag_table_names = []
        if bag_names:
            bag_table_values = self._etree.xpath(
                united_xp.BAG_FEE_TABLE_VALUES
            )
            for i, j in enumerate(bag_names):
                s = remove_tags(etree.tostring(j))
                if i == 3:
                    s = strip_str(take_first(self._etree, united_xp.MAX_WT))
                bag_table_names.append(s)
            table = filter_dict_value(
                to_dict(bag_table_names, bag_table_values)
            )
        else:
            table = ''
            self.logger.error('bag_fee_table is empty %s', self._message_id)
        if table:
            result['bag_fee_table'] = table

        marketing_info_trs = self._etree.xpath(united_xp.MARKETING_INFO)
        if marketing_info_trs:
            titles = marketing_info_trs[1::3]
            contents = marketing_info_trs[2::3]
            titles_list = [
                strip_str(take_first(i, united_xp.MARKETING_INFO_TITLES))
                for i in titles
            ]
            name_dict = {
                'Important Information about MileagePlus Earning':
                    'mileage_plus_earning',
                'International eTicket Reminders':
                    'eticket_reminders',
                'Customer Care Contact Information':
                    'customer_care',
                'Refunds Within 24 Hours':
                    'refund',
                'Hazardous materials':
                    'hazardous_materials',
                'Proud Member of Star Alliance':
                    'star_alliance'
            }
            for i, j in zip(titles_list, contents):
                s = j.xpath(united_xp.MARKETING_INFO_CONTENTS)
                if s:
                    a = []
                    for k in s:
                        links = k.xpath('.//a/@href')
                        link_texts = k.xpath('.//a/text()')
                        texts = strip_str(remove_tags(etree.tostring(k)))
                        if links:
                            a.append({
                                'text': texts,
                                'links': {
                                    'name': link_texts,
                                    'value': links
                                }
                            })
                        else:
                            a.append({'text': texts})
                    result[name_dict[i]] = a
        else:
            self.logger.error('marketing_info is empty %s', self._message_id)

        notice_titles = strip_list(self._etree.xpath(united_xp.NOTICES_TITLE))
        notice_contents = strip_list(
            self._etree.xpath(united_xp.NOTICE_CONTENTS)
        )
        last_advice = strip_str(take_first(self._etree, united_xp.LAST_ADVICE))
        name_dict = {
            'Notice of Baggage Liability Limitations':
                'baggage_liability_limit',
            'Notice of Incorporated Terms':
                'incorporated_terms',
            'Notice of Certain Terms':
                'certain_terms',
            'Notice of Boarding Times':
                'boarding_times',
            'Advice to International Passengers on Carrier Liability':
                'carrier_liability',
            'Notice - Overbooking of Flights':
                'overbooking'
        }
        if notice_contents and notice_titles:
            notice_contents[-1] += last_advice
            for i, j in zip(notice_titles, notice_contents):
                if i in name_dict.keys():
                    result[name_dict[i]] = j.strip('- ')
                else:
                    self.logger.warning(
                        'notice %s is %s %s', i, j, self._message_id
                    )
        else:
            self.logger.error('notice is empty %s', self._message_id)
        return result
