# import requests
#
# url = "https://authgtj.alipay.com/login/index.htm"
#
# payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"support\"\r\n\r\n000001\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"CtrlVersion\t\"\r\n\r\n1,1,0,1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"loginScene\t\"\r\n\r\nindex\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"rds_form_token\t\"\r\n\r\nVmPR8qa8YaXUtmEZnawlDJwuBCtNK240\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"logonId\t\"\r\n\r\n18273711329\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"superSwitch\t\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"noActiveX\t\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"passwordSecurityId\t\"\r\n\r\nweb|authcenter_querypwd_login|2018203b-6c74-4d31-9c24-d71c22fba35aRZ11\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"qrCodeSecurityId\t\"\r\n\r\nweb|authcenter_qrcode_login|e26c5051-b45c-4712-9ed7-d006db2eb0edRZ11\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_using\t\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\t\"\r\n\r\nQeKQPYP58YKzJGdfmNz+9JCQxQHEPG+Nb1tiREgb82D8Z5Hihsasx+aMu41+N3UhJxUXq+E16dP/QlSOeCf8olG8HO3uiOlkWYb5E9ED7ugcUTpTm2EGUPkOFjpKOL1yhWKtDfBaDb0wjZDDDAcBazLVxe/Nk4meBNTR1K7ZcxnD5veyB7PFiH4FX8aYhfuV6xahL4kgFyxoSkEBuW3cTiI+foTJe+s3CyNl+IdhL99AHaaOVOW7ZXocxYWjPvC7oOEvDDdgf5ajN58kiDOEPcKWuGWWQkV4ZeIcN4w4EZJzPcnmlB3bX3E31A8F2DpwBKYl3hQL9reZGBBWw58FOw==\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_key_hidn\t\"\r\n\r\npassword\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"J_aliedit_uid_hidn\"\r\n\r\nalieditUid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"REMOTE_PCID_NAME\t\"\r\n\r\n_seaside_gogo_pcid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"alieditUid\"\r\n\r\na648454c81e6c65860734c242fb57209\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"security_activeX_enabled\t\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"preCheckTimes\t\"\r\n\r\n5\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ua\t\"\r\n\r\n116YlF/THtKfkR0R3FHdUJ5Qh0=|YVF/JgZHLV0wXzgYNhYiGTkXN2IJZQNuG2pKFUo=|YFF/JhUjFjgJPQ0jECAUIA46DTcZKhEhEz0OPAY0GikSIhA+DT8JO2Q7|Z1RnSRAwWixaKFlhTGECdQNpRSZII1EySWUEaQYrRShNJkpnDGAGYRs3XStEZEpqShVK|ZlVlS2s/UAJSaBt4Qhl6IHcBbilxHX4LZSNrHmkpaB5SGysdLw9Q|ZV9xUTJFM1k4XzNFIlIPYQxpAm4zAzECOAo7CDMANQI0AjlkVGBTZ119Ig==|ZF9xCChJOUwvQWFZIAB0F3lZYUEiTCdVNk1tQ2MRfxxqDmMTfFxkRBF6FicXNxk5TyJVNF5+RiJBL145RmhIOVI9SiFNKURkXCUFcBt3V29ebFxyUjRZOBggET8ffg9+XmZVb0FhAXEcaRh/Dy8XTm4hTDRfMV88HDISXjlPPl88TikJJwcwHC4MJnMYdBJ/CntZFUNhUmBMfkdlMFs3AzUMLlRgVn1fHG4cchVAJ0cOZRM+CTgNIRAkBixlL3k2eFZ0GnEYf10Yfx53GjETUjhIJUotADQPIxE9DDoBNBgiETNiAWUGdh0wBzYDLx4qCiQEJAp8DHscMkQ0QyQKKn8UeEl5WXdXd1l5NlsjSCZIKwYxHS8NJ3IZdRN+C3pYFEJgU2FNf0ZkMVo2AjQNL1VhV3xeHW8dcxRBJkYPZBI/CDkMIBElBy1kLng3eVd1G3AZflwZfh92GzASUzlJJEssATUOIhA8DTsANRkjEDJjAGQHdxwxBjcCLh8rCyUFJQsrSCZNP1wnC2oHaEhmRmZIaEhmRmZIaEhmVW5ebEJxQ3lLZVVjTX5FdUdpWmhebEJwXmwzTGJCMlE9WzZZeUFwRnJCeFZ2F2EMZQJuTnZWZBV+NVMURS1aPm4pRA1caUk2aQ==|a11zKgoqBD8POxUmCDIENmk2|al1zKgoqBF1mV2xCcUR2KQc1GzsbNQY3AjkDXAM=|aV9xKAh6GWgZbAFxF0o6SyhDL10qXHxSaFJlS3tOe1VmUWFWbTJt|aF9xKAh6GWgZbAFxF0o6SyhDL10qXHxSCzELOBYmHC9wXmxCYkJsX2hZbFgHWA==|b1p0LQ1/HG0caQR0Ek8/Ti1GKlgvWXlXZEp5TnhLfCN8|blp0LQ1/HG0caQR0Ek8/Ti1GKlgvWXlXYVF/TWNQZFRjWQZZ|bVl3Lg58H24fagd3EUw8TS5FKVssWnpUYlJ8TmBTZ1FqWAdY|bFh2Lw99Hm8eawZ2EE09TC9EKFotW3tVY1N9T2FSZlNnXQJd|c0dpMBBiAXABdBlpD1IiUzBbN0UyRGRKfExiUH5NeEh+RBtE|ckFvXnBFa1hrUX9MekhmUWpEcUZoU31Oe1VgTn1KZFVvQXFHaVloRnZGaFhrNA==\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"REMOTE_PCID_NAME\t\"\r\n\r\n_seaside_gogo_pcid\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
# headers = {
#     'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
#     'Host': "authgtj.alipay.com",
#     'Connection': "keep-alive",
#     'Content-Length': "2725",
#     'Cache-Control': "no-cache",
#     'Origin': "https://auth.alipay.com",
#     'Upgrade-Insecure-Requests': "1",
#     'Content-Type': "application/x-www-form-urlencoded",
#     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
#     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     'Referer': "https://auth.alipay.com/login/index.htm",
#     'Accept-Encoding': "gzip, deflate, br",
#     'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
#     'Cookie': "JSESSIONID=RZ11AEApCHI9x62cuOGdv43xAlkA0sauthRZ11; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; cna=U/3KEwSmeTwCAbdRtUKnmqQ7; NEW_ALIPAY_TIP=1; unicard1.vm=\"K1iSL16SV9EvE/EboTdxcg==\"; _uab_collina=153604928557284578550913; ssl_upgrade=0; session.cookieNameId=ALIPAYJSESSIONID; _umdata=C234BF9D3AFA6FE7CCE5C39C37F8091298FCAAC6876B100E55D5AF6D5086FE618FE2011882956315CD43AD3E795C914C26F8A2DD309860F54864D2CBDFB508A3; zone=RZ11A; ALIPAYJSESSIONID=RZ11AEApCHI9x62cuOGdv43xAlkA0sauthRZ11; ctoken=0siIdESjufREoKS7; umt=Laa6b2ef4347c9dc6009aae3b040aaec8; JSESSIONID=AF4DFBB43005F7A52FA9A231253021A4; spanner=B2hkE+Ez9I5FNAA/urXj01Wc/mWh3AQP4EJoL7C0n0A=; rtk=9hbZMn0h20KEbmIINhEADb6uEY+g5v/Kuuln5gYFGggJGzs1X+3",
#     'Postman-Token': "f489e8f4-70b4-f9d4-0518-409b2e56216b"
#     }
#
# response = requests.request("POST", url, data=payload, headers=headers, verify=False)
#
# print(response.text)

import requests

url = "https://auth.alipay.com/login/index.htm"

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "JSESSIONID=RZ11NlCQDuFkIyHoa313Bvago3DRR8authRZ11; ssl_upgrade=0; _uab_collina=153682715700892265683153; mobileSendTime=-1; credibleMobileSendTime=-1; ctuMobileSendTime=-1; riskMobileBankSendTime=-1; riskMobileAccoutSendTime=-1; riskMobileCreditSendTime=-1; riskCredibleMobileSendTime=-1; riskOriginalAccountMobileSendTime=-1; cna=Fg0hFDBoOWECAWf+RN5gC5uk; _umdata=0712F33290AB8A6D627A268FADBF07713D908631153C8E788B8F5009E046188A8DFF288C52489F35CD43AD3E795C914C5F161B83FFEAEF8BE47D3548B2F05BC8; session.cookieNameId=ALIPAYJSESSIONID; unicard1.vm=\"K1iSL16SV9EvE/EboTdxcg==\"; zone=RZ11B; JSESSIONID=8EDD066A08E82ADA00C78A78BA77DEEB; spanner=8Nz5ht9WBVdFNAA/urXj06jKfq4B+t734EJoL7C0n0A=; ALIPAYJSESSIONID=RZ11BuNt4Rm6s5QpqKsLds5ZtvzAmaauthRZ11; ctoken=jh8K5dsNfOENL-G9; umt=Ld46e863c39d41bafcaf6a3c8533a69b0; rtk=dOvOMkpO991q9gyaUOySVCBF4eI7G0IxFFTkgueuS67aw/jb3IX",
    'Host': "auth.alipay.com",
    'Referer': "https://www.baidu.com/link?url=fjMMcdDQBjlZe8WX_kyRxIkw0P7zp1G-d4SYYQFIKs2xoohdAouFrmYfek2MwE1x&wd=&eqid=e02b82d6000292a2000000055b9a2a2f",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    'Postman-Token': "12c494eb-48de-294c-f91f-f9cb5e6ebe2b"
    }

response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)
