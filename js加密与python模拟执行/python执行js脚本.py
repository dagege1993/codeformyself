import execjs

file = 'encryption.js'
# ctx = node.compile(open(file).read())
ctx = execjs.compile('Alipay.js')  # 加载JS文件
print(ctx)


