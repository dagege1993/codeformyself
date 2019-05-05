import re

itemName = "威龙有机原生干红750ML"
itemName = "500ml毛铺金荞"
itemName = "1.25L果粒橙"
# itemName = "椰汁1L"
# itemName = "福佳白啤2.5L"
# itemName = "1L果粒橙"
# if 'ml' or 'ML' in itemName:
#     unit = re.findall('.*?(\d+)[ML,ml]', itemName)
#     if unit:
#         print(unit[0])


if 'L' in itemName:
    unit = re.findall('(\d+.*?)L', itemName)
    if unit:
        print(unit[0])

# itemName = '清水馒头8个'
itemName = '鲜辣鲍鱼仔(个)'
if "个" in itemName:
    unit = re.findall('(\d+)个', itemName)
    # print(unit)
    if len(unit) >= 1:
        unit = unit[0] + '个'
    else:
        unit = '一个'
    print(unit)

itemName = '海底捞德式小麦啤酒2瓶'
itemName = '海底捞经典大麦啤酒'
if '啤酒' in itemName:
    unit = re.findall('(\d+)瓶', itemName)
    if len(unit) >= 1:
        unit = unit[0] + '瓶'
    else:
        unit = '一瓶'
    print(unit)
