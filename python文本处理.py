ll = [',                  '
      ',岗位晋升,                                    '
      ',                                  ,                  '
      ',发展空间大,                                    '
      ',                                  ,                  '
      ',带薪年假,                                    '
      ',                                  ,                  '
      ',绩效奖金,                                    '
      ',                                  ,                  '
      ',交通补助,                                    '
      ',                                  ,                  '
      ',午餐补助,                                    '
      ',                                  ,                  '
      ',五险一金,                                    '
      ',                                  ,                  '
      ',生育补贴,                                    ,']

# for l in ll:
# 	print(l)
# print()
result = " ".join(ll)
print(1, result)
# result2 = result.replace(',', '')
result2 = result.replace(' ', '')
result2 = result2.replace(',,,', '')
print(result2.strip(',,'))
# print(result2.split())
