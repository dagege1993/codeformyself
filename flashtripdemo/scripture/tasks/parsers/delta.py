# coding: utf-8

from lxml import etree
from w3lib.html import remove_tags

from tasks.xpath import delta_xp
from tasks.utils.html import take_first
from tasks.utils.html import take_last
from tasks.utils.html import strip_list
from tasks.utils.html import strip_str
from tasks.utils.time import DateTime
from tasks.utils.time import to_timezone

from tasks.parsers import FlightOrderParser
from tasks.errors.parse_error import MissingColumnError


class DeltaParser(FlightOrderParser):

    """delta.com
    """

    @classmethod
    def validate(cls, sender, subject, snippet):
        if not (
            sender.strip('"').startswith('Delta Air Lines') and
            sender.strip('>').endswith('delta.com')
        ):
            return False

        if 'Congrats On Your SkyMiles Award Trip' not in subject:
            return False

        # TODO(LensHo): 需要用snippet来验证是否需要解析
        print("delta.com snippet: ", snippet)

        return True

    def _parse(self):
        result = self._order
        confirm_code = take_first(self._etree, delta_xp.CONFIRM_CODE)
        if not confirm_code:
            raise MissingColumnError('confirm_code', self._message_id)
        confirm_code = remove_tags(etree.tostring(confirm_code))
        result['confirm_code'] = ''.join(confirm_code)

        result.set(
            'modify_link', take_first(self._etree, delta_xp.CHANGE_LINK)
        )

        # TODO(LensHo): 起飞降落只有一个日期
        flight_date = strip_list(self._etree.xpath(delta_xp.FLIGHT_DATE))
        if not flight_date:
            raise MissingColumnError('flight_date', self._message_id)

        result['depart_date'] = result['arrive_date'] = flight_date[0]
        if len(flight_date) >= 2:
            result['trans_depart_date'] = flight_date[1]
            result['trans_arrive_date'] = flight_date[1]

        flight_num = strip_list(self._etree.xpath(delta_xp.FLIGHT_NUM))
        if not flight_num:
            raise MissingColumnError('flight_number', self._message_id)

        result['flight_number'] = flight_num[0]
        if len(flight_num) >= 2:
            result['trans_flight_number'] = flight_num[1]

        cabin = strip_list(self._etree.xpath(delta_xp.CABIN))
        if cabin:
            result['class'] = cabin[0]
            if len(cabin) >= 2:
                result['trans_class'] = cabin[1]
        else:
            self.logger.error('class is empty %s', self._message_id)

        depart_station = strip_list(self._etree.xpath(delta_xp.DEPART_STATION))
        if not depart_station:
            raise MissingColumnError('depart_station', self._message_id)
        result['depart_city'] = depart_station[0]
        if len(depart_station) >= 2:
            result['trans_depart_city'] = depart_station[1]

        depart_time = strip_list(self._etree.xpath(delta_xp.DEPART_TIME))
        if not depart_time:
            raise MissingColumnError('depart_time', self._message_id)
        result['depart_time'] = depart_time[0]
        if len(depart_time) >= 2:
            result['trans_depart_time'] = depart_time[1]

        arrive_time = strip_list(self._etree.xpath(delta_xp.ARRIVE_TIME))
        if not arrive_time:
            raise MissingColumnError('arrive_time', self._message_id)
        result['arrive_time'] = arrive_time[0]
        if len(arrive_time) >= 2:
            result['trans_arrive_time'] = arrive_time[1]
        elif len(arrive_time) > 2 and 'm' in arrive_time[2]:
            self.logger.error('换乘超过1次 %s', self._message_id)

        arrive_station = strip_list(self._etree.xpath(delta_xp.ARRIVE_STATION))
        if not arrive_station:
            raise MissingColumnError('arrive_station', self._message_id)
        result['arrive_city'] = arrive_station[0]
        if len(arrive_station) >= 2:
            result['trans_arrive_city'] = arrive_station[1]

        restricted_title = strip_str(
            take_first(self._etree, delta_xp.RESTRICTED_TITLE)
        )
        restricted_text = take_first(self._etree, delta_xp.RESTRICTED_TEXT)
        if len(restricted_text) and restricted_title:
            text = strip_str(remove_tags(etree.tostring(restricted_text)))
            if 'RESTRICTED HAZARDOUS ITEMS' in restricted_title:
                result['restricted_hazardous_items'] = text
            else:
                # 有可能是其他条目
                self.logger.warning(
                    '%s is %s %s', restricted_title, text, self._message_id
                )
        else:
            self.logger.error(
                'restricted_hazardous_items is empty %s', self._message_id
            )

        result['guest_name'
               ] = strip_str(take_first(self._etree, delta_xp.GUEST_NAME))
        if not result['guest_name']:
            result.pop('guest_name')
            self.logger.error('guest_name is empty %s', self._message_id)

        seat = strip_list(self._etree.xpath(delta_xp.SEAT))
        if seat:
            result['seat'] = seat[0]
            if len(seat) >= 2:
                result['trans_seat'] = seat[1]
        else:
            self.logger.error('seat is empty %s', self._message_id)

        result['ticket_number'
               ] = strip_str(take_last(self._etree, delta_xp.TICKET_NUM))
        if not result['ticket_number']:
            raise MissingColumnError('ticket_number', self._message_id)

        try:
            result['issue_date'], result['expire_date'] = strip_list(
                self._etree.xpath(delta_xp.ISSUE_EXPIRE_DATE)
            )
        except ValueError:
            self.logger.error(
                'issue_expire_date is empty %s', self._message_id
            )

        year = int('20' + result.get('issue_date')[-2:]) \
            if result.get('issue_date') else 0
        tz_dp = to_timezone(result.get('depart_city'))
        tz_ar = to_timezone(result.get('arrive_city'))
        dp_dt = ' '.join([result['depart_date'], result['depart_time']])
        ar_dt = ' '.join([result['arrive_date'], result['arrive_time']])
        dt_format = 'DDMMM h:mmA'
        dt_dp = DateTime(dp_dt, dt_format)
        year = year or dt_dp.received_time_to_year(self.received_time)
        result['depart_datetime_formatted'] = dt_dp.year_to_datetime(
            year, tz_dp
        )
        if not result['depart_datetime_formatted']:
            result.pop('depart_datetime_formatted')
            self.logger.error(
                'depart datetime formatted is empty %s', self._message_id
            )

        result['arrive_datetime_formatted'] = DateTime(
            ar_dt, dt_format
        ).year_to_datetime(year, tz_ar)

        if not result['arrive_datetime_formatted']:
            result.pop('arrive_datetime_formatted')
            self.logger.error(
                'arrive datetime formatted is empty %s', self._message_id
            )

        # TODO(LensHo): 没考虑转机时过年的情况, 只考虑换乘一次
        trans_dp_date = result.get('trans_depart_date')
        trans_dp_time = result.get('trans_depart_time')
        if trans_dp_date and trans_dp_time:
            trans_dp_dt = trans_dp_date + ' ' + trans_dp_time
            result['trans_depart_datetime_formatted'] = DateTime(
                trans_dp_dt, dt_format
            ).year_to_datetime(year, tz_ar)

            if not result['trans_depart_datetime_formatted']:
                result.pop('trans_depart_datetime_formatted')
                self.logger.error(
                    'trans_depart_datetime_formatted is empty %s',
                    self._message_id
                )

        trans_ar_date = result.get('trans_arrive_date')
        trans_ar_time = result.get('trans_arrive_time')
        tz_trans_ar = to_timezone(result.get('trans_arrive_city'))
        if trans_ar_date and trans_ar_time:
            trans_ar_dt = trans_ar_date + ' ' + trans_ar_time
            result['trans_arrive_datetime_formatted'] = DateTime(
                trans_ar_dt, dt_format
            ).year_to_datetime(year, tz_trans_ar)
            if not result['trans_arrive_datetime_formatted']:
                result.pop('trans_arrive_datetime_formatted')
                self.logger.error(
                    'trans_arrive_datetime_formatted is empty %s',
                    self._message_id
                )

        result['payment_card_number'] = strip_str(
            take_first(self._etree, delta_xp.PAYMENT_METHOD_CARD)
        )
        if not result['payment_card_number']:
            result.pop('payment_card_number')
            self.logger.error('payment_card is empty %s', self._message_id)

        result['payment'] = strip_str(
            take_first(self._etree, delta_xp.PAYMENT_METHOD_MONEY)
        )
        if not result['payment']:
            result.pop('payment')
            self.logger.error('payment is empty %s', self._message_id)

        result['duration'
               ] = strip_str(take_first(self._etree, delta_xp.DURATION))
        if not result['duration']:
            result.pop('duration')
            self.logger.error('duration is empty %s', self._message_id)

        result['transportation_fare'
               ] = strip_str(take_first(self._etree, delta_xp.BASE_FARE))
        if not result['transportation_fare']:
            result.pop('transportation_fare')
            self.logger.error(
                'transportation_fare is empty %s', self._message_id
            )

        result['price'
               ] = strip_str(take_first(self._etree, delta_xp.TAXES_FEE))
        if not result['price']:
            result.pop('price')
            self.logger.error('price is empty %s', self._message_id)

        result['total_cost'
               ] = strip_str(take_first(self._etree, delta_xp.TOTAL))
        if not result['total_cost']:
            result.pop('total_cost')
            self.logger.error('total_cost is empty %s', self._message_id)

        baggage_info = take_first(self._etree, delta_xp.BAGGAGE_INFO)
        baggage_text = take_first(self._etree, delta_xp.BAGGAGE_TEXT)
        baggage_link = take_first(self._etree, delta_xp.BAGGAGE_LINK)
        if baggage_info:
            result['baggage_allowance'] = {
                'text': remove_tags(etree.tostring(baggage_info)).strip()
            }
            if baggage_link and baggage_text:
                result['baggage_allowance'].update({
                    'links': {
                        'name': baggage_text,
                        'value': baggage_link
                    }
                })
        else:
            self.logger.error(
                'baggage_allowance is empty %s', self._message_id
            )

        hazardous_title = strip_str(
            take_first(self._etree, delta_xp.HAZARDOUS_MATERIALS_TITLE)
        )
        hazardous_text_1 = strip_str(
            take_first(self._etree, delta_xp.HAZARDOUS_MATERIALS_TEXT_1)
        )
        hazardous_text_2 = take_first(
            self._etree, delta_xp.HAZARDOUS_MATERIALS_TEXT_2
        )
        link = take_first(self._etree, delta_xp.HAZARDOUS_MATERIALS_LINK)
        text = strip_str(
            take_first(self._etree, delta_xp.HAZARDOUS_MATERIALS_TEXT)
        )
        if hazardous_title == 'Transportation of Hazardous Materials':
            if hazardous_text_2:
                hazardous_text_2 = remove_tags(
                    etree.tostring(hazardous_text_2)
                )
            else:
                hazardous_text_2 = ''
                self.logger.error(
                    'part of hazardous_material text is empty %s',
                    self._message_id
                )
            if hazardous_text_1 or hazardous_text_2:
                hazardous_text = '\n'.join([
                    hazardous_text_1, hazardous_text_2
                ]).strip()
                result['transportation_of_hazardous_materials'] = {
                    'text': hazardous_text
                }
            if link and text and \
                    result.get('transportation_of_hazardous_materials'):
                result['transportation_of_hazardous_materials'].update({
                    'links': {
                        'name': text,
                        'value': link
                    }
                })
        else:
            self.logger.warning(
                'Transportation of Hazardous Materials not found %s',
                self._message_id
            )

        return result
