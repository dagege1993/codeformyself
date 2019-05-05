import time

test = """<li><span>类型：</span><a href="/list/index/cid/2/">全部</a><a href="/list/index/cid/101587/">角色扮演</a><a href="/list/index/cid/19/">休闲益智</a><a href="/list/index/cid/20/">动作冒险</a><a href="/list/index/cid/100451/">网络游戏</a><a href="/list/index/cid/51/">体育竞速</a><a href="/list/index/cid/52/">飞行射击</a><a href="/list/index/cid/53/">经营策略</a><a href="/list/index/cid/54/">棋牌天地</a><a href="/list/index/cid/102238/" class="aurr">儿童游戏</a>        </li>
"""
import re

# result = re.findall('/cid/(\d+)', test)
result = re.findall('/list/index/cid/(\d+)/', test)
names = re.findall('>(.*?)</a>', test)
print(result[1:])
print(names[1:])
# localtime = time.localtime(time.time())
# print(localtime)
# strtime = time.strftime("%Y-%m-%d", localtime)
# print(strtime)


url = 'http://zhushou.360.cn/list/index/cid/102238/?page=4'
test = re.findall('(\d+)/', url)
print(test)

url = 'http://zhushou.360.cn/list/index/cid/102238/?page=4'
test = re.findall('http://zhushou\.360\.cn/list/index/cid/(102238)/\?page=4', url)
print(test)

url = 'http://zhushou.360.cn/detail/index/soft_id/771431'
test = re.findall('soft_id/(\d+)', url)
print(test)

downloads_nums = '1402万次下载'
downloads_nums = downloads_nums.replace('次下载', '')
if '万' in downloads_nums:
    downloads_nums = downloads_nums.replace('万', '')
    downloads_nums = int(downloads_nums) * 10000
print(downloads_nums)

downloads_nums = '1亿次下载'
downloads_nums = downloads_nums.replace('次下载', '')
if '亿' in downloads_nums:
    downloads_nums = downloads_nums.replace('亿', '')
    downloads_nums = int(downloads_nums) * 100000000
print(downloads_nums)

strs = '<li id="cate--10"><a href="?orgame=1&amp;categoryId=-10">腾讯软件</a></li>'
names = re.findall('<.*>(.*)</a>', strs)
print(names)

# old_url = 'https://shouji.baidu.com/game/401/'
old_url = 'https://shouji.baidu.com/software/501/'
replace_key = re.findall('\d+', old_url)
print(replace_key)

list1 = ['1', '2', '3']
list2 = ['a', 'b', 'c']
list3 = ['A', 'B', 'C']

d = {}
for i in range(0, len(list1)):
    d[list1[i]] = (list2[i], list3[i])

print(d)

old_url = 'https://shouji.baidu.com/software/509_board_100_048/'
page_num = re.findall('list_(\d+)', old_url)
print(page_num)

old_url = 'https://shouji.baidu.com/game/board_102_200/'
# old_url = 'https://shouji.baidu.com/game/407/'
# old_url = 'https://shouji.baidu.com/software/503/'
page_num = re.findall('[game,software]/(.*)/', old_url).pop()
print(page_num)
page_num = page_num.replace('software/', '')
page_num = page_num.replace('game/', '')
print(page_num)

downloads_nums = '4.2'
ll = int(float(downloads_nums)) * 100000000
print(ll)

page_num = []
if page_num:
    print(page_num)
else:
    print(2222)

old_url = 'https://shouji.baidu.com/game/404/list_2.html'
page_num = re.findall('list_(\d+)', old_url)
print(page_num)

old_url = 'https://shouji.baidu.com/software/502/list_2.html'
page_num = re.findall('list_(\d+)', old_url)
if page_num:
    page_num = int(page_num.pop())
    page_num += 1
    change_url = re.findall('(list_\d+\.html)', old_url).pop()
    print(change_url)
    next_url = 'list_' + str(page_num) + '.html'
    new_url = old_url.replace(change_url, next_url)
    print('第二页以后的链接', new_url)

wait_re = '''
var detail = (function () {
        return {
            'sid': 3073428,
            'type': "game",
            'cid1': "2",
            'cid2': "102249",
            'pname': "com.tencent.tmgp.sgame",
            'downloadUrl': 'http://shouji.360tpcdn.com/181219/7f11214826ba3b5c8fcc927e3878c0e3/com.tencent.tmgp.sgame_42012008.apk',
            'filemd5': '7f11214826ba3b5c8fcc927e3878c0e3',
            'vcode': '42012008',
            'baike_name': '英雄战迹 Android_com.tencent.tmgp.sgame'
        };
    })();
    </script>
    
    <tr>
        <td><strong>版本：</strong>1.42.1.20<!--versioncode:42012008--><!--updatetime:2018-12-24--></td>
        <td><strong>系统：</strong>Android 4.1.x以上</td>
    </tr>

<span class="s-3">下载：7001万次</span>

'sname': '无印良品助眠器MUJI to Sleep',

<span class="version">版本: 8.12.2</span>
<span class="download-num">下载次数: 6.9亿</span>
'''
pkg_name = re.findall("'pname': (.*?),", wait_re)
app_name = re.findall("'sname': (.*?),", wait_re)
versionname = re.findall("版本：</strong>(.*)<!", wait_re)
result = versionname.pop().split('<')[0]
print(result)
downloads_nums = re.findall('下载：(.*)<', wait_re)
print(downloads_nums)
# print(pkg_name, versionname)


version = re.findall('<span class="version">版本: (.*)</span>', wait_re)
version = re.findall('<span class="download-num">下载次数: (.*)</span>', wait_re)
print(version)

ll = """
<span class="one-setup-btn" onclick="bd_app_dl_quick(this,event);" data-action="software" data-mod="" data-tj="software_2052121_285631_生化危机4" data-pos="11" data_type="apk" data_url="http://apk.gfan.com/baidudownload.php?apk=461327&amp;src=baidupage" data_name="生化危机4" data_detail_type="app" data_package="com.wiirecords.biohazardrmb" data_versionname="2.1.14" data_icon="http://a.hiphotos.bdimg.com/wisegame/pic/item/be54564e9258d109432bce4ad058ccbf6d814d7a.jpg" data_from="91Assistant_PC_V6_16" data_size="7611423">一键安装</span>
"""
version = re.findall('data_package=(.*?) ', ll)
print(version)

localtime = time.localtime(time.time())
days = time.strftime("%d", localtime)
weeks = int(days)//7 +1
month = time.strftime("%Y/%m", localtime)
print(month+'/'+str(weeks))
