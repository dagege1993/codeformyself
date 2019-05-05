import base64
from hashlib import md5
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

e = '登录密码' + ";" + password + ";" + 验证码 + ";" + 验证码 + ";" + "%s" % loginPageType

public_key = """-----BEGIN PUBLIC KEY-----
{rsaPublicKey}  // 加密所用到的公钥
-----END PUBLIC KEY-----""".format(rsaPublicKey=rsaPublicKey)

rsakey = RSA.importKey(public_key)
cipher = PKCS1_v1_5.new(rsakey)
cipher_text = base64.b64encode(cipher.encrypt(e))
print
cipher_text
---------------------
作者：后青春诗ing
来源：CSDN
原文：https: // blog.csdn.net / weixin_42812527 / article / details / 81322209
版权声明：本文为博主原创文章，转载请附上博文链接！
