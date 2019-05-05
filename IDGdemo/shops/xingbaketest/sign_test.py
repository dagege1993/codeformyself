'''
引入hmac,hashlib加密模块
'''
import hmac
import hashlib


def jm_sha256(key, value):
    '''
    sha256加密
    return:加密结果转成16进制字符串形式，并大写
    '''
    hsobj = hashlib.sha256(key.encode("utf-8"))
    hsobj.update(value.encode("utf-8"))
    return hsobj.hexdigest()


def jm_md5(key, value):
    '''
    md5加密
    return:加密结果转成16进制字符串形式，并大写
    '''
    hsobj = hashlib.md5(key.encode("utf-8"))
    hsobj.update(value.encode("utf-8"))
    return hsobj.hexdigest().upper()


def hmac_sha256(key, value):
    '''
    hmacsha256加密
    return:加密结果转成16进制字符串形式，并大写
    '''
    message = value.encode('utf-8')
    return hmac.new(key.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest().upper()


def hmac_md5(key, value):
    '''
    hmacmd5加密
    return:加密结果转成16进制字符串形式，并大写
    '''
    message = value.encode('utf-8')
    return hmac.new(key.encode('utf-8'), message, digestmod=hashlib.md5).hexdigest().upper()


if __name__ == '__main__':
    key = 'MIIEowIBAAKCAQEA4VoHujAt31BlzIbCyNXDYEVt5F03WMEdkQ+i0RPu0YzrLUP0VGZL7R/gY3ZqDrzUau4+nDjIZ3qOyUxX2SUiL4XNgoR/0ux9KUnl8HjNmPMfFStYfDttSQYm1LwFxRaET8o+X7fM4u5UhfzR9FXJZJ8l0AIPvVAp7qgjQ0NBoLWMNFDVPJkrChw7fPuogw8lroWflBEpP6+QqTRD58+tj9C17h2cFXMpuV2aRBXsNLIg6TzoQg/fgA0nth8k25Z/npv7HMO29oOJ2tbpZltXY/2WLI407Cf8UG1dKP68M986OkwwjtPpv6jEHVoZizE/+zj4qTy7uu78lsaqppb32wIDAQABAoIBAQCzdf4XYUz2vVEEiwFN7SY1YbU9Gpr7/HauUhRoioYyrRWQq8BFAl5OzYblzqRxbiF/spF72aCG/8v8NOb0z6Sk0dqyqRAeiiS2n9oVIi8hMeQ7+JP0A2NptxNvcPjrVp4x6K65jWcGBaScO5V8DmFe13rGZw3fxppOK+pBI6t87fifUuiNNzdgqUOIXAx4kypYBAzCPuVH2ypxMxYnhnIrZ9iZcayYbF2mrYax4YGwMckGs4uFzOPiJHj6vg4cEL4g3b1vOrDgY1wwnmTM93HNqS89WYVOpFDnOTRsOlmL6COJH2U/YqHe3CbYxGXJnYjLqKJ/k5QwXaZoK+98wUnJAoGBAPhaqIh++o93gF7vicsboHT0l5DvqCPSwdwFBlr2i3ODuVLrUvHbrRDN0bTlWwO2GuEBZyXGqNGerMaJlr67BTXIg4KDwXCpMJ8YxyRUQ7EGsLp3WS6Zzt6VeSKYRMzu7CHfyUzXwK0e5kylVWeiclzFEBWHpGC5FsYRoSYNSU6/AoGBAOhKFW2b4PhjCBDzQZrUWd0lR7aGufyHaKUEVKS5isXXmOonWQT4BEsLcXX1m9i3ZN0gB4uCY+bdiLkdoEwPppSRG0e7z0a0MRB6YtC5LBhkUcYKIS41dYsOeNG2cAG2Cs3UZwHgnyC9g1NFFoCkhkV1fyRWi32c2GQCsJzIRTnlAoGADIVFidwc9a6ooiChacPyyvKp0XzDlUrCyzzVnTBgx2oUpcGHZPoWN4qoz93gQMelg0J22MizKh49x6SYHPWAxb1eI+5QikV9VggBwisdXodf0YbC0D6g10fh24Shs1M4RFzr4Rvfctrj8WlEbP0bluG4dd1oxBeQtludLDXvRDECgYAdHuyAyUHy4bdpKJXY6zY42yuaXlmCpxcfWOOjov8avmSVNkmard0b61tWBmx7RsKGVjWb78TGdI9nZadq4atohKh+3bSmkIB2KGGq+QvmIu19fleai2ko/a932v8/t6qzEyW2voo0eI22KrsfdYC/xHMkAxWJsdgO8adigFjtYQKBgGlEJcXfOKNICdKsN0/v5LSop8ZC20mO1bBHNZu8vk37/6peAH1geICS6BKfooNChavn6dfBi+ch2W19Jq73/nuYj1wdvVzkpXBmjnTLig7XBa4iOs1z/we1l+oBXf/zjg8wbptx/02mBuay6Zt3k9Pk8NjmlmqMeYje4Y+mbcg9'
    value = 'appid=859977c6f22b4f9ce98d4b02d031b4a8&lang=zh-cn&store_id=25023'
    result = hmac_sha256(key, value)
    print(result)

'mcOSiT9YT7246yLUxPIa9bPvHtjWVJn%2Fmp90Kdk3H%2F9BG72vriVEHmfQBnXrSaRs1Wpm%2B%2Bct9hIY%0AnX7X%2BmTSi%2BuLJNtcl331d7pWrl%2Bu6R42lZ9Agl3ISCPes0RqEyyWGyGpI2KSeK1EKK7eLOgelxMb%0A%2FlYRhZqVkj2BVV5foHtAwAI5m0Pls8%2BShPuI0mTQPbQqW3S2j%2Fii68VmpIXddCU6yAw02sZG7%2BrE%0AlJHL5EvG5ybdC881LO1i0YPIWhkW6tUL4G%2FB7y3pzEkICRX5ium4HHMaoIYjz4PjTJtW6qM0gYZG%0Aqr6djRfRts%2F8d5pEZsrnOryskKOpd%2F3XW0lSfA%3D%3D%0A'
