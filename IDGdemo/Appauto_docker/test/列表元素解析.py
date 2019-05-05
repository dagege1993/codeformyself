# encoding=utf8
# results = ['"充2赠1"', '"榛果拿铁"', '"Hazelnut Latte"', '"默认：大/单糖/热"', '"¥27"', '"WBC（世界咖啡师大赛）冠军团队拼配"', '"充2赠1"', '"拿铁"', '"Latte"', '"默认：大/无糖/热"', '"¥24"', '"充2赠1"', '"香草拿铁"', '"Vanilla Latte"', '"默认：大/单糖/热"', '"¥27"', '"充2赠1"', '"焦糖拿铁"', '"Caramel Latte"', '"默认：大/单糖/热"', '"¥27"', '"充2赠1"', '"标准美式"', '"Americano"', '"默认：大/无糖/无奶/热"', '"¥21"', '"充2赠1"', '"加浓美式"', '"Extra Americano"', '"默认：大/无糖/无奶/热"', '"¥24"']
# results = ['"充2赠1"', '"焦糖拿铁"', '"Caramel Latte"', '"默认：大/单糖/热"', '"¥27"', '"充2赠1"', '"标准美式"', '"Americano"', '"默认：大/无糖/无奶/热"', '"¥21"', '"充2赠1"', '"加浓美式"', '"Extra Americano"', '"默认：大/无糖/无奶/热"', '"¥24"', '"充2赠1"', '"焦糖标准美式"', '"Caramel Americano"', '"默认：大/单糖/无奶/热"', '"¥24"', '"充2赠1"', '"焦糖加浓美式"', '"Caramel Extra Americano"', '"默认：大/单糖/无奶/热"', '"¥27"', '"充2赠1"', '"黑金气泡美式"', '"Black Gold Soda Americano"', '"默认：大"', '"¥24"', '"充2赠1"', '"澳瑞白"', '"Flat White"', '"默认：大/无糖/热"', '"¥27"', '"充2赠1"', '"卡布奇诺"', '"Cappuccino"', '"默认：大/无糖/热"', '"¥24"', '"焦糖玛奇朵"']
# results = ['"充2赠1"', '"黑金气泡美式"', '"Black Gold Soda Americano"', '"默认：大"', '"¥24"', '"充2赠1"', '"澳瑞白"', '"Flat White"', '"默认：大/无糖/热"', '"¥27"', '"充2赠1"', '"卡布奇诺"', '"Cappuccino"', '"默认：大/无糖/热"', '"¥24"', '"充2赠1"', '"焦糖玛奇朵"', '"Caramel Macchiato"', '"默认：大/单糖/热"', '"¥27"', '"充2赠1"', '"摩卡"', '"Mocha"', '"默认：大/默认奶油/单糖/热"', '"¥27"', '"不含咖啡的拿铁"', '"充2赠1"', '"红茶拿铁"', '"Black Tea Latte"', '"默认：大/热"', '"¥27"', '"充2赠1"', '"小雪荔枝瑞纳冰"', '"Lychee Exfreezo"', '"默认：大"', '"¥27"', '"卡布奇诺瑞纳冰"', '"Cappuccino Exfreezo"', '"默认：大/默认奶油"']
# results = ['"充2赠1"', '"红茶拿铁"', '"Black Tea Latte"', '"默认：大/热"', '"¥27"', '"充2赠1"', '"小雪荔枝瑞纳冰"', '"Lychee Exfreezo"', '"默认：大"', '"¥27"', '"充2赠1"', '"卡布奇诺瑞纳冰"', '"Cappuccino Exfreezo"', '"默认：大/默认奶油"', '"¥27"', '"充2赠1"', '"巧克力瑞纳冰"', '"Chocolate Exfreezo"', '"默认：大/默认奶油"', '"¥27"', '"充2赠1"', '"抹茶瑞纳冰"', '"Matcha Exfreezo"', '"默认：大/默认奶油"', '"¥27"', '"充2赠1"', '"石榴蔓越莓苏打水"', '"Pomegranate Cranberry Soda Water"', '"默认：大"', '"¥21"', '"充2赠1"', '"柑橘百香果"', '"Citrus Passionfruit Refresher"', '"默认：大/热"', '"¥21"', '"充2赠1"', '"巧克力"', '"Chocolate Milk"', '"默认：大/热"', '"¥24"']
# results = ['"充2赠1"', '"¥27"', '"充2赠1"', '"石榴蔓越莓苏打水"', '"Pomegranate Cranberry Soda Water"', '"默认：大"', '"¥21"', '"充2赠1"', '"柑橘百香果"', '"Citrus Passionfruit Refresher"', '"默认：大/热"', '"¥21"', '"充2赠1"', '"巧克力"', '"Chocolate Milk"', '"默认：大/热"', '"¥24"', '"充2赠1"', '"纯牛奶"', '"Milk"', '"默认：大/热"', '"¥21"', '"充2赠1"', '"依云矿泉水330ml"', '"Evian"', '"¥18"', '"充2赠1"', '"巴黎水330ml"', '"Perrier"', '"¥18"', '"10:00 6.6折"', '"金枪鱼谷物沙拉"', '"Tuna and Mixed Grain Salad"', '"¥25.08"', '"¥38"', '"经典牛肉土豆泥沙拉"']
# results = ['"充2赠1"', '"¥18"', '"充2赠1"', '"巴黎水330ml"', '"Perrier"', '"¥18"', '"10:00 6.6折"', '"金枪鱼谷物沙拉"', '"Tuna and Mixed Grain Salad"', '"¥25.08"', '"¥38"', '"经典牛肉土豆泥沙拉"', '"Beef and Mashed potato Salad"', '"¥25.08"', '"¥38"', '"川味鸡丝拌面套餐"', '"Szechuan Cold Noodles with Pulled Chicken"', '"¥23.1"', '"¥35"', '"樱桃番茄五谷食盒"', '"luckin Combo with Cherry Tomatoes"', '"¥23.1"', '"¥35"', '"10:00 6.6折"', '"夏威夷菠萝火腿卷(单卷)"', '"Hawaii Pineapple Ham Wrap"', '"¥8.58"', '"¥13"', '"蔓越莓司康"', '"Cranberry Scone"', '"¥9.9"', '"¥15"']

# results = ['"樱桃番茄五谷食盒"', '"luckin Combo with Cherry Tomatoes"', '"¥23.1"', '"¥35"', '"10:00 6.6折"', '"夏威夷菠萝火腿卷(单卷)"',
#            '"Hawaii Pineapple Ham Wrap"', '"¥8.58"', '"¥13"', '"蔓越莓司康"', '"Cranberry Scone"', '"¥9.9"', '"¥15"',
#            '"巧克力麦芬"', '"Chocolate Muffin"', '"¥8.58"', '"¥13"', '"香椰提子麦芬"', '"Coconut Raisin Muffin"', '"¥8.58"',
#            '"¥13"', '"香蕉核桃麦芬"', '"Banana Walnut Muffin"', '"¥8.58"', '"¥13"', '"火腿金枪鱼双拼三明治"', '"Ham Tuna Sandwich"',
#            '"¥15.84"', '"¥24"', '"提拉米苏蛋糕"', '"Tiramisu Cake"']


# results = ['"香蕉核桃麦芬"', '"Banana Walnut Muffin"', '"¥8.58"', '"¥13"', '"火腿金枪鱼双拼三明治"', '"Ham Tuna Sandwich"', '"¥15.84"', '"¥24"', '"提拉米苏蛋糕"', '"Tiramisu Cake"', '"¥16.5"', '"¥25"', '"黑森林蛋糕"', '"Black Forest Cake"', '"¥16.5"', '"¥25"', '"芝士蓝莓蛋糕"', '"Cheese Blueberry Cake"', '"¥16.5"', '"¥25"', '"售罄"', '"意大利烤鸡卷(单卷)"', '"Italian Roasted Chicken Wrap"', '"¥8.58"', '"¥13"', '"售罄"', '"火腿鲜蔬卷(单卷)"', '"Ham Vegetable Wrap"', '"¥8.58"', '"¥13"', '"售罄"', '"火腿芝士羊角"', '"Ham  Cheese  Croissant"', '"¥10.56"', '"¥16"', '"巧克力司康"']
results = ['"充2赠1"', '"NFC鲜榨橙汁"', '"NFC Fresh Orange Juice"', '"¥24"', '"充2赠1"', '"猕猴桃复合果汁"', '"Kiwifruit Juice"',
           '"¥24"', '"充2赠1"', '"NFC鲜榨蓝莓草莓混合果汁"', '"NFC Fresh Blueberry &amp; Strawberry Juice"', '"¥24"']


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


if '"10:00 6.6折"' in results:
    results.remove('"10:00 6.6折"')
if '"售罄"' in results:
    results.remove('"售罄"')
if '"WBC（世界咖啡师大赛）冠军团队拼配"' in results:
    results.remove('"WBC（世界咖啡师大赛）冠军团队拼配"')
if '"充2赠1"' in results:
    p = results.index('"充2赠1"')
    p = p + 1
    print(p)
    counts = results.count('"充2赠1"')
    print(counts)
    for i in range(counts):
        start = results.index('"充2赠1"')
        start = start + 1
        results = results[start:]
        end = results.index('"充2赠1"')
        data = results[:end]
        print(data)
# 如果不在
else:
    for result in results:
        # print(result)
        is_chinese = is_Chinese(result.strip())
        if is_chinese is True:
            start = results.index(result)
            end = start + 4
            # print(start)
            try:
                food_data = results[start:end]
                print(food_data)
            except Exception as e:
                print(e)
    # print(result.startswith(''))

tt = ['"猕猴桃复合果汁"', '"Kiwifruit Juice"', '"¥24"']
tt.insert(3, '优惠')
print(tt)
