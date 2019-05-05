import pandas as pd

data = {
    "id": "1844",
    "name": "青岛颐和国际店",
    "address": {
        "city": "青岛市",
        "streetAddressLine1": "香港中路10号颐和国际一层102",
        "streetAddressLine2": 'NULL',
        "streetAddressLine3": 'NULL',
        "postalCode": "266071"
    },
    "coordinates": {
        "latitude": 36.065044,
        "longitude": 120.381809
    },
    "today": {
        "closeTime": "21:30:00",
        "openTime": "07:00:00"
    },
    "features": [
        "OG",
        "DL",
        "MIC",
        "PO"
    ],
    "hasArtwork": False
}
id = data.get('id')
name = data.get('name')
address_dict = data.get('address')
city = address_dict.get('city')
address_values = address_dict.values()
address = ''.join(address_values)
print(address)


# 传入城市,获取城市级别
def get_city_level():
    path = r'city_level.xlsx'
    results = pd.read_excel(path)
    city_list = results['城市']
    level_list = results['城市等级']
    city_level_dict = dict(zip(city_list, level_list))
    print(city_level_dict)
    return (city_level_dict)


get_city_level()
