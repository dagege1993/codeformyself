# coding: utf-8

from ftplib import FTP, FTP_TLS, parse227, parse229
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT
from io import BytesIO
import pandas as pd
from datetime import datetime
from . import DB as db

class FTP_NEW(FTP):
    def __init__(self, host='', user='', passwd='', acct='',
                 timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        self.source_address = source_address
        self.timeout = timeout
        self.host = host
        if host:
            self.connect(host)
            if user:
                self.login(user, passwd, acct)
    def makepasv(self):
        if self.af == socket.AF_INET:
            host, port = parse227(self.sendcmd('PASV'))
        else:
            host, port = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
        return self.host, port


class TraveFlex:

    host = '13.229.147.14'
    user = 'client'
    pswd = 'everyoneispartofmg'

    def get_tf_city_id(self):
        ftp_1 = FTP_NEW(
            self.host,
            self.user,
            self.pswd
        )
        excel = BytesIO()
        ftp_1.cwd('MG Mapping Hotel Level')
        files = ftp_1.nlst()
        ftp_1.retrbinary('RETR %s' % files[-1], excel.write, 1024)
        data = pd.read_excel(excel)
        for i in range(len(data)):
            _data = data.loc[i]
            idmap_upload = {
                'hotel_id': _data.get('Hotelid', ''),
                'city_code': _data.get('Citycode', ''),
                'country_code': _data.get("CountryCode", "")
            }
            data_map = {
                'name': _data['Hotelname'],
                'code': _data['Hotelid'],
                'ean_code': _data['EAN RAPID '],
                'fit_code': _data['FIT Ruums'],
                'juniper_code': _data['Juniper'],
                'hotelbeds_code': _data['HB'],
                'address': _data['Address'],
                'city_name': _data['Cityname'],
                'city_code': _data['Citycode'],
                'country_code': _data['CountryCode'],
                'country_name': _data['CountryName'],
                'paymen': _data['Payment'],
                'tel': _data['Tel No.'],
                'fax': _data['FAX No.'],
                'latitude': _data['Latitude'],
                'longitude': _data['Longtitude'],
                'star': _data['Star'],
                'room_number': _data['Number of Room'],
                'e-mail': _data['Email'],
            }
            idmap_res = db['statics.hotels.travflex.location'].update_one(
                {'hotel_id': idmap_upload['hotel_id']},
                {'$set': idmap_upload},
                upsert=True
            )
            data_res = db['statics.hotels.travflex'].update_one(
                {'code': data_map['code']},
                {
                    "$set": data_map,
                    "$setOnInsert": {"created_at": datetime.now()},
                    "$currentDate": {"updated_at": True}
                }
            )