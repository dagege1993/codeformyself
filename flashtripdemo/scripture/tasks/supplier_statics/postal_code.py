# coding: utf8

# Standard Library
import re

from tasks.utils.database import databases

CNMAPPING = {
    # 1 直辖市
    "10": "北京",
    "20": "上海",
    "30": "天津",
    "40": "重庆",
    # 2 华北 0
    "01": "内蒙古",
    "02": "内蒙古",
    "03": "山西",
    "04": "山西",
    "05": "河北",
    "06": "河北",
    "07": "河北",
    # 3 东北 1
    "11": "辽宁",
    "12": "辽宁",
    "13": "吉林",
    "15": "黑龙江",
    "16": "黑龙江",
    # 4 华东 2
    "21": "江苏",
    "22": "江苏",
    "23": "安徽",
    "24": "安徽",
    "25": "山东",
    "26": "山东",
    "27": "山东",
    # 5 华东 3
    "31": "浙江",
    "32": "浙江",
    "33": "江西",
    "34": "江西",
    "35": "福建",
    "36": "福建",
    # 6 华中 4
    "41": "湖南",
    "42": "湖南",
    "43": "湖北",
    "43": "湖北",
    "45": "河南",
    "46": "河南",
    "47": "河南",
    # 7 华南与贵州 5
    "51": "广东",
    "52": "广东",
    "53": "广西",
    "54": "广西",
    "55": "贵州",
    "56": "贵州",
    "57": "海南",
    # 8 西南 6
    "61": "四川",
    "62": "四川",
    "63": "四川",
    "64": "四川",
    "65": "云南",
    "66": "云南",
    "67": "云南",
    # 9 西北 7
    "71": "陕西",
    "72": "陕西",
    "73": "甘肃",
    "74": "甘肃",
    "75": "宁夏",
    # 10 西部 8
    "81": "青海",
    "83": "新疆",
    "84": "新疆",
    "85": "西藏",
}

KRMAPPING = {
    "01": "Seoul",
    "02": "Seoul",
    "03": "Seoul",
    "04": "Seoul",
    "05": "Seoul",
    "06": "Seoul",
    "07": "Seoul",
    "08": "Seoul",
    "09": "Seoul",
    "10": "Gyeonggi Province",
    "11": "Gyeonggi Province",
    "12": "Gyeonggi Province",
    "13": "Gyeonggi Province",
    "14": "Gyeonggi Province",
    "15": "Gyeonggi Province",
    "16": "Gyeonggi Province",
    "17": "Gyeonggi Province",
    "18": "Gyeonggi Province",
    "19": "Gyeonggi Province",
    "20": "Gyeonggi Province",
    "21": "Incheon",
    "23": "Incheon",
    "24": "Gangwon Province",
    "25": "Gangwon Province",
    "26": "Gangwon Province",
    "27": "North Chungcheong Province",
    "28": "North Chungcheong Province",
    "29": "North Chungcheong Province",
    "30": "Sejong City",
    "31": "South Chungcheong Province",
    "32": "South Chungcheong Province",
    "33": "South Chungcheong Province",
    "34": "Daejeon",
    "35": "Daejeon",
    "36": "North Gyeongsang Province",
    "37": "North Gyeongsang Province",
    "38": "North Gyeongsang Province",
    "39": "North Gyeongsang Province",
    "40": "North Gyeongsang Province",
    "41": "Daegu",
    "42": "Daegu",
    "43": "Daegu",
    "44": "Ulsan",
    "45": "Ulsan",
    "46": "Busan",
    "47": "Busan",
    "48": "Busan",
    "49": "Busan",
    "50": "South Gyeongsang Province",
    "51": "South Gyeongsang Province",
    "52": "South Gyeongsang Province",
    "53": "South Gyeongsang Province",
    "54": "North Jeolla Province",
    "55": "North Jeolla Province",
    "56": "North Jeolla Province",
    "57": "South Jeolla Province",
    "58": "South Jeolla Province",
    "59": "South Jeolla Province",
    "60": "South Jeolla Province",
    "61": "Gwangju",
    "62": "Gwangju",
    "63": "Jeju Province",
}


class RangePostalCodeMapping(dict):

    def find(self, postal_code):
        # postal_code, *_ = postal_code.split("-")
        try:
            postal_code = int(postal_code)
        except Exception:
            return
        for start, end in self:
            if start <= postal_code <= end:
                return self[(start, end)]


BRMAPPING = RangePostalCodeMapping(
    {
        (1000, 9999): (
            "São Paulo Metropolitan Region including the suburbs "
            "or the area outside the São Paulo metropolitan region"
        ),
        (11000, 19999): "State of São Paulo",
        (20000, 28999): "State of Rio de Janeiro",
        (29000, 29999): "State of Espírito Santo",
        (30000, 39999): "State of Minas Gerais",
        (40000, 48999): "State of Bahia",
        (49000, 49999): "State of Sergipe",
        (50000, 56999): "State of Pernambuco",
        (57000, 57999): "State of Alagoas",
        (58000, 58999): "State of Paraíba",
        (59000, 59999): "State of Rio Grande do Norte",
        (60000, 63999): "State of Ceará",
        (64000, 64999): "State of Piauí",
        (65000, 65999): "State of Maranhão",
        (66000, 68899): "State of Pará",
        (68900, 68999): "State of Amapá",
        (69000, 69299): "State of Amazonas (part 1)",
        (69300, 69399): "State of Roraima",
        (69400, 69899): "State of Amazonas (part 2)",
        (69900, 69999): "State of Acre",
        (70000, 72799): "Federal District (part 1)",
        (72800, 72999): "State of Goiás (part 1)",
        (73000, 73699): "Federal District (part 2)",
        (73700, 76799): "State of Goiás (part 2)",
        (76800, 76999): "State of Rondônia (part 1)",
        (77000, 77999): "State of Tocantins",
        (78000, 78899): "State of Mato Grosso",
        (78900, 78999): "State of Rondônia (part 2)",
        (79000, 79999): "State of Mato Grosso do Sul",
        (80000, 87999): "State of Paraná",
        (88000, 89999): "State of Santa Catarina",
        (90000, 99999): "State of Rio Grande do Sul",
    }
)

CZMAPPING = RangePostalCodeMapping(
    {
        (100, 199): "Prague",
        (250, 295): "Central Bohemian Region",
        (301, 349): "Plzeň Region",
        (350, 364): "Karlovy Vary Region",
        (370, 399): "South Bohemian Region",
        (400, 441): "Ústí nad Labem Region",
        (460, 473): "Liberec Region",
        (500, 572): "Hradec Králové and Pardubice Regions",
        (580, 595): "Vysočina Region",
        (600, 698): "South Moravian Region",
        (700, 749): "Moravian-Silesian Region",
        (750, 769): "Zlín Region",
        (779, 798): "Olomouc Region",
    }
)

# TODO: GR<Greece> missing many.


def get_province_by_postal_code(postal_code, country_code):
    postal_code = postal_code.strip().upper()
    if country_code == "UK":
        country_code = "GB"
        if len(postal_code) > 4:
            postal_code = postal_code[:4]
    elif country_code == "US":
        try:
            short_state, code = postal_code.split()
            assert len(short_state) == 2
            assert not short_state.isdigit()
            postal_code = f"{code:0>5}"
        except Exception:
            if "-" in postal_code:
                postal_code, _ = postal_code.split("-")
            postal_code = f"{postal_code:0>5}"
    # elif country_code == "IT":
    #     postal_code = f"{postal_code:0>6}"
    elif country_code in ["DE", "ES", "FR", "IT"]:
        postal_code = f"{postal_code:0>5}"
    elif country_code == "CA":
        if "-" in postal_code:
            postal_code, _ = postal_code.split("-")
        else:
            first, *seconds = postal_code.split()
            if len(seconds) >= 2:
                postal_code = seconds[0]
            else:
                postal_code = first
    elif country_code == "JP":
        postal_code = re.compile(f"^{postal_code[:3]}")
    elif country_code == "CN":
        postal_code = f"{postal_code:0>6}"
        return CNMAPPING.get(postal_code[:2])
    elif country_code == "KR":
        postal_code = f"{postal_code:0>5}"
        return KRMAPPING.get(postal_code[:2])
    elif country_code == "BR":
        postal_code, *_ = postal_code.split("-")
        return BRMAPPING.find(postal_code)
    elif country_code == "TW":
        return "台湾"
    elif country_code == "HK":
        return "香港"
    elif country_code == "SG":
        return "新加坡"
    elif country_code == "CZ":
        return CZMAPPING.find(postal_code[:3])
    elif country_code == "BR":
        # 巴西
        if "." in postal_code:
            postal_code = postal_code.replace(".", "")
        if len(postal_code) > 5:
            postal_code = "-".join([postal_code[:5], postal_code[:-3]])
    if country_code == "IT":
        print(f"Country({country_code}), PostalCode({postal_code})")
    zipcodes = databases("scripture").statics.postal_codes.find(
        {"country_code": country_code, "postal_code": postal_code}
    )
    provinces = set(zipcode["admin_name1"] for zipcode in zipcodes)
    if provinces:
        return provinces.pop()
    if isinstance(postal_code, str) and " " in postal_code:
        return get_province_by_postal_code(
            postal_code.split(" ")[0], country_code
        ) or get_province_by_postal_code(
            postal_code.replace(" ", ""), country_code
        )


if __name__ == "__main__":
    import yaml

    with open("data/countries.yml") as yml:
        countries = yaml.load(yml)

    agent = databases("agent")
    cursor = agent.statics.hotels.hotelbeds.find(
        {
            "wgstar": {"$gte": 3},
            # "country.code": {"$in": list(countries["hotelbeds"].keys())},
            "country.code": "IT",
            "province": {"$exists": False},
        }
    )
    print("Total:", cursor.count())
    for hb in cursor:
        if not hb.get("postalCode"):
            continue
        try:
            province = get_province_by_postal_code(
                hb["postalCode"], hb["countryCode"]
            )
        except RecursionError:
            print(
                f'RecursionError: Country({hb["countryCode"]}),'
                f'PostalCode({hb["postalCode"]})'
            )
            continue
        if province:
            agent.statics.hotels.hotelbeds.update_one(
                {"_id": hb["_id"]}, {"$set": {"province": province}}
            )
        else:
            print(
                f'Country({hb["countryCode"]}), PostalCode({hb["postalCode"]})'
            )
