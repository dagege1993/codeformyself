import json

ll = [{'count': 180, 'tag': '味道赞'}, {'count': 145, 'tag': '服务热情'}, {'count': 118, 'tag': '点心好'},
      {'count': 35, 'tag': '价格实惠'}, {'count': 33, 'tag': '回头客'}, {'count': 15, 'tag': '干净卫生'},
      {'count': 6, 'tag': '饮品赞'}, {'count': 5, 'tag': '菜品健康'}, {'count': 4, 'tag': '现做现卖'}, {'count': 3, 'tag': '朋友聚餐'}]
print(json.dumps(ll, ensure_ascii=False, indent=4))

# 这样会报错,因为join方法期望是列表里包含全字符串而不是字典
