'''
python中字典的键是不能直接修改，因为键是hash。

间接修改键的key值方法

第一种(推荐)：'''
# 移除字典数据pop()方法的作用是：删除指定给定键所对应的值，返回这个值并从字典中把它移除
dicts = {'a': 1, 'b': 2}
print(dicts.pop("a"))
dicts['c'] = dicts.pop("a")
print(dict)
