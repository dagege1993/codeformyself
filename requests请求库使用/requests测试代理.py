# encoding=utf8
import requests

# proxies = {
#     'http': 'http://183.129.244.16:15945',
#     'https': 'https://183.129.244.16:15945',
# }

proxies = {
    'http': 'http://183.129.244.16:17663',
    'https': 'https://183.129.244.16:17663',
}

url = 'https://www.baidu.com/'
# response = requests.get(url, proxies=proxies, )
response = requests.request('get', url, proxies=proxies, verify=False)
print(response.content)
