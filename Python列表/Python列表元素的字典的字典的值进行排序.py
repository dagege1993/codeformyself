room_list = [

    {'agentInfo': '', 'area': '220m²',

     'priceInfo': {'avgPrimeGroupAmount': {'a': 1, 'b': 4}, 'cacheBack': 0, 'cnyOriginalPrice': 20590.0,
                   'cnyPrice': 20590.0,
                   'cnyTax': 4290.0, 'cnyTotalPrice': 25326.0, 'cnyTotalPriceWithoutTax': 20590.0,
                   'cnyTotalTax': 4290.0, 'currency': 'JPY', 'discountId': 0, 'exg': 0.061197,
                   'localPrice': 336448.0, 'localTax': 70101.0, 'localTotalPrice': 413839.0,
                   'localTotalTax': 70101.0, 'prepayDiscountAmount': 0, 'prepayDiscounts': [],
                   'prepayTotalDiscountAmount': 0, 'totalFinalFee': 20590.0, 'totalPrimeGroupAmount': 0},
     'priceLowestRoom': False, 'promotags': [], 'rateid': ''},
    {'agentInfo': '', 'area': '220m²',
     'priceInfo': {'avgPrimeGroupAmount': {'a': 1, 'b': 3}, 'cacheBack': 0, 'cnyOriginalPrice': 20936.0,
                   'cnyPrice': 20936.0,
                   'cnyTax': 4362.0, 'cnyTotalPrice': 25752.0, 'cnyTotalPriceWithoutTax': 20936.0,
                   'cnyTotalTax': 4362.0, 'currency': 'JPY', 'discountId': 0, 'exg': 0.061197,
                   'localPrice': 342112.0, 'localTax': 71278.0, 'localTotalPrice': 420803.0,
                   'localTotalTax': 71278.0, 'prepayDiscountAmount': 0, 'prepayDiscounts': [],
                   'prepayTotalDiscountAmount': 0, 'totalFinalFee': 20936.0, 'totalPrimeGroupAmount': 0},
     'priceLowestRoom': False, 'promotags': [], 'rateid': '',
     },
    {'agentInfo': '', 'area': '220m²',
     'priceInfo': {'avgPrimeGroupAmount': {'a': 1, 'b': 2}, 'cacheBack': 0, 'cnyOriginalPrice': 21543.0,
                   'cnyPrice': 21543.0,
                   'cnyTax': 4489.0, 'cnyTotalPrice': 26499.0, 'cnyTotalPriceWithoutTax': 21543.0,
                   'cnyTotalTax': 4489.0, 'currency': 'JPY', 'discountId': 0, 'exg': 0.061197,
                   'localPrice': 352035.0, 'localTax': 73353.0, 'localTotalPrice': 433016.0,
                   'localTotalTax': 73353.0, 'prepayDiscountAmount': 0, 'prepayDiscounts': [],
                   'prepayTotalDiscountAmount': 0, 'totalFinalFee': 21543.0, 'totalPrimeGroupAmount': 0},
     }

]

# key=lambda e: e.__getitem__('priceInfo').get('cnyTotalPrice')
# print(key)
# sorted_rooms = sorted(room_list, key=lambda e: e.__getitem__('priceInfo').get('cnyTotalPrice'))
sorted_rooms = sorted(room_list, key=lambda e: e.__getitem__('priceInfo').get('avgPrimeGroupAmount').get('b'))
# sorted_rooms = sorted(room_list, key=lambda e: e.__getitem__('priceInfo').get(''))
print(sorted_rooms)
