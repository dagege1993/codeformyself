# coding:utf-8

def find_each_min_supplier(categorized):
    sups = {}
    for room_type, rooms in categorized.items():
        for room in rooms:
            sup = room.get("identity", {}).get("provider", "Unknown")
            if sup not in sups:
                sups[sup] = {
                    "price": float(room.get("total_price", 99999999)),
                    "ori_price": float(room.get("ori_total_price_cny")),
                    "room_type_en": room_type,
                    "room_type_cn": room.get("translation", ""),
                }
                continue
            if float(room.get("total_price", 99999999)) < sups[sup]["price"]:
                sups[sup]["price"] = float(room.get("total_price", 99999999))
                sups[sup]["room_type_en"] = room_type
                sups[sup]["room_type_cn"] = room.get("translation", "")
    return sups
