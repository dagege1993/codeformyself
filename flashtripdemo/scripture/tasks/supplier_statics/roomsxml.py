# coding: utf8

import pathlib
import requests

import xlrd
import rarfile
from lxml import objectify

from . import BaseSupplier, Providers


class RoomsXML(BaseSupplier):

    supplier = Providers.roomsxml

    @classmethod
    def address(cls, address1, address2, address3):
        _addr = []
        if address1:
            _addr.append(address1.text)
        if address2:
            _addr.append(address2.text)
        if address3:
            _addr.append(address3.text)
        addr = ','.join(_addr)
        addr.strip(',')
        return addr

    @classmethod
    def images(cls, elements):
        imgs = []
        for image in elements:
            imgs.append(f'www.roomsxml.com{image.Url.text}')
        return imgs

    @classmethod
    def descriptions(cls, elements):
        descs = []
        for desc in elements:
            if desc.Text:
                descs.append(desc.Text.text)
        return '\n'.join(descs)

    @classmethod
    def amenities(cls, elements):
        _amenities = []
        for amenity in elements:
            _amenities.append(amenity.Text)
        return _amenities

    @classmethod
    def rating(cls, elements):
        return ' '.join([elements.Score.text, elements.System.text])

    def fetch(self, types='Hotels'):
        url = "http://integrate.roomsxml.com/Main.aspx"
        data = [
            f"rbtnForDownloading={types}",
            "ddlLanguage=English",
            "btnGenerate=Download+File",
            "__EVENTTARGET=",
            "__EVENTARGUMENT=",
            "__LASTFOCUS=",
            ("__VIEWSTATE=%2FwEPDwUKLTg0MzU4OTUxNQ8WAh4TVmFsaWRhdGVSZXF1ZXN0TW"
             "9kZQIBFgICAw9kFgICAw9kFgJmD2QWBGYPZBYCAgEPZBYCAgMPDxYCHgRUZXh0Bf"
             "UDcm9vbXNYTUwgaXMgYW4gYWNjb21tb2RhdGlvbiBkaXN0cmlidXRpb24gc3lzdG"
             "VtIGRlc2lnbmVkIGZvciB0cmF2ZWwgY29tcGFuaWVzLiBUaGUgcG9pbnQgb2YgZG"
             "lmZmVyZW5jZSB3aXRoIHJvb21zWE1MIGlzIGluIGl0cyBwcm9wcmlldGFyeSBzb2"
             "Z0d2FyZSBjYXBhYmlsaXR5IHRvIGZsYXdsZXNzbHkgbWFwIGFuZCBkZS1kdXBsaW"
             "NhdGUgdGhlIGludmVudG9yeSB0aGF0IGNvbWVzIGZyb20gbWFueSBkZXN0aW5hdG"
             "lvbiBzcGVjaWZpYyBzdXBwbGllcnMsIGRpcmVjdCBjb250cmFjdGluZyBhbmQgZH"
             "luYW1pY2FsbHkgZnJvbSBsYXJnZSBob3RlbCBjaGFpbnMuIDxici8%2BPGJyLz5U"
             "aGUgcm9vbXNYTUwgSW50ZWdyYXRpb24gUG9ydGFsIHByb3ZpZGVzIHlvdSB0aGUg"
             "bmVjZXNzYXJ5IGRvY3VtZW50YXRpb24sIGRhdGEgZmlsZXMgYW5kIHRvb2xzIHRv"
             "IHN1Y2Nlc3NmdWxseSBpbnRlZ3JhdGUgeW91ciBob3RlbCBib29raW5nIGVuZ2lu"
             "ZSB3aXRoIHRoZSByb29tc1hNTCBBUEkuZGQCBA9kFgICAQ9kFgQCAQ8PFgIfAQUc"
             "U3RhdGljIERhdGEgRG93bmxvYWRzIChMaXZlKWRkAgUPZBYCZg9kFgQCAQ8QZGQW"
             "AQIBZAIDDxAPFgIeB1Zpc2libGVnZGRkZGSCvVE%2BnXcK2grSBmtoY4xBtLro5g"
             "%3D%3D"),
            "__VIEWSTATEGENERATOR=202EA31B",
            ("__PREVIOUSPAGE=CgxpQ18qxkfYM7lqTUhQJOK6i3Ye21zZ1TFmcmwaVQo4hn4OR"
             "K-MCre5vrmNMj2_4SfsZKiO5lGAO2Gq9C-wxG1WO1A1"),
            ("__EVENTVALIDATION=%2FwEdABIlkjQoQDO8fPzwImfk17dQysnTe25jqqbYufpZ"
             "bmXBaEcidJ4SVFvJO8xvoFZnGbjF0oFYOIEZrDOo%2F%2FlPZH%2BCrMacgn%2FG"
             "763d2kKDiLea3RCE7zYNCNWjpy22jqsMHsM%2BEA0Dgf816WTzaft6izpaARTLOl"
             "hLSy%2BpIZXPbU5CT7Uh5N2o1TL%2FHQwd6vnFhEoBTqiiN3F6H8PyARXHe6Gyd1"
             "S54g%2BOCoLSxfwdXYIvhkKpG0wtvUPuRqomjRpogQyWLR35r%2FuxvOfyET43VD"
             "f%2FhtsxQEaHtlyvh79o2syFY9XG%2FmJu3BkIS%2FUrk1SPVlc%2F9bWH0QHqAI"
             "T1fpzDtC8BKai3Y3c1yI2lNl3SKe8YryEntSbvVuoP782PskDRpLrPMsFqhvDolB"
             "6kkAUTFzFoe6lmWg%3D%3D")
        ]
        headers = {
            "Host": "integrate.roomsxml.com",
            "User-Agent": ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) "
                           "Gecko/20100101 Firefox/58.0"),
            "Referer": "http://integrate.roomsxml.com/Main.aspx",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        cookies = {
            "ASP.NET_SessionId": "1uftew0jexwofqfdzfvv0vzp",
            "Cookie": "UserId=5622&IsLive=True"
        }
        resp = requests.post(
            url,
            data='&'.join(data),
            headers=headers,
            cookies=cookies,
            stream=True
        )
        if types == 'Hotels':
            rarpath = f'/tmp/statics_{types}_roomsxml.rar'
            with open(rarpath, 'wb') as hotels:
                for chunk in resp.iter_content(4096):
                    hotels.write(chunk)

            with rarfile.RarFile(rarpath) as rf:
                rf.extractall()
            xmls = pathlib.Path('.') / 'HotelDetailXML'
            for xmlfile in xmls.glob('*.xml'):
                if not xmlfile.is_file():
                    continue
                xml_content = xmlfile.read_bytes()
                if not xml_content:
                    continue
                yield objectify.fromstring(xml_content)
            xmls.unlink()
        elif types == 'Regions':
            xlsxpath = f'/tmp/statis_{types}_roomsxml.xlsx'
            with open(xlsxpath, 'wb') as regionfile:
                for chunk in resp.iter_content(4096):
                    regionfile.write(chunk)
            workbook = xlrd.open_workbook(xlsxpath)
            sheet = workbook.sheet_by_name('Region')
            headers = sheet.row_values(0)
            headers[0] = 'code'
            for row_no in range(1, sheet.nrows):
                values = sheet.row_values(row_no)
                values[0], values[3] = int(values[0]), int(values[3])
                yield dict(
                    zip(headers, values)
                )

    def hotels(self):
        for hotel in self.fetch('Hotels'):
            doc = {
                'code': hotel.Id.text,
                'name': hotel.Name.text,
                'region': {
                    'code': hotel.Region.Id,
                    'name': hotel.Region.Name
                },
                'city': {
                    'code': hotel.Region.CityId,
                    'name': hotel.Address.City
                },
                'state': {
                    'name': hotel.Address.State
                },
                'country': {
                    'name': hotel.Address.Country
                },
                'type': hotel.Type,
                'address': self.address(
                    hotel.Address.Address1,
                    hotel.Address.Address2,
                    hotel.Address.Address3
                ),
                'postal_code': hotel.Address.Zip,
                'phone': hotel.Address.Tel,
                'fax': hotel.Address.Fax,
                'email': hotel.Address.Email,
                'website': hotel.Address.Url,
                'rank': hotel.Rank
            }
            try:
                doc['amenities'] = self.amenities(hotel.Amenity)
            except AttributeError:
                pass
            try:
                doc['images'] = self.images(hotel.Photo)
            except AttributeError:
                pass
            try:
                doc['description'] = self.descriptions(hotel.Description)
            except AttributeError:
                pass
            try:
                doc['latitude'] = hotel.GeneralInfo.Latitude
                doc['longitude'] = hotel.GeneralInfo.Longitude
            except AttributeError:
                pass
            try:
                doc['stars'] = hotel.stars
                doc['wgstar'] = int(hotel.stars.text)
            except AttributeError:
                doc['stars'] = '0'
                doc['wgstar'] = 0
            try:
                doc['rating'] = self.rating(hotel.Rating)
            except AttributeError:
                pass

            if not doc['city']['name']:
                region = self.table('region').find_one({
                    'code': int(doc['city']['code'])
                })
                if not region:
                    print('region missing', doc['city']['code'])
                else:
                    doc['city']['name'] = region.get('Region Name')
            self.save(doc)

    def regions(self):
        for region in self.fetch('Regions'):
            self.save(region, 'regions')
