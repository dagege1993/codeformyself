### 2018 - 02 - 01
#### 背景
现有三方数据的图片地址都是供应商的，很多没有CDN，经常遇到访问不到的情况，或者加载特别慢，严重影响页面展现。
#### 目的
将图片存储到我们的CDN上，以改善用户体验。
#### How
1.下载源图片
2.上传到OSS/CDN
3.替换数据库内的图片访问地址，使用我们CDN的地址
#### 代码细节
patch图片地址 → New/Old → WriteToDB
                              ↳  celery task[download and upload]
因为下载和上传是重IO的操作，且很多图片是在国外，速度很慢，且与保存数据库不是强依赖关系，所以可以使用celery并行。

#### 背景
scripture数据库内statics.hotels.bonotel/hotelbeds/hotelpro/roomsxml四个集合内存储了第三方服务商酒店的静态数据，每条document存储了一家酒店的数据，但只有英文名，没有相对应的中文名
#### 目的
为前端界面展示中文名提供中文名数据
#### HOW
1.连接scripture，依次选中statics.hotels.bonotel/hotelbeds/hotelpro/roomsxml四个供应商静态数据所在集合，并对每个集合对象执行2
2.集合中每条document对应一个酒店的数据，遍历集合的所有document，对每个document执行3
3.取出document的字段name，name是酒店的英文名
  请求携程接口 http://hotels.ctrip.com/international/Tool/cityFilter.ashx?charset=gb2312&flagship=1&keyword={{name}}得到响应，响应中存储了该酒店的信息，
  数据样本如下
  ```
  {"key":"Bellagio","data":"@Bellagio|Bellagio，雅罗斯拉夫，雅罗斯拉夫尔州，俄罗斯|hotel|9273177|雅罗斯拉夫，雅罗斯拉夫尔州，俄罗斯|6973|yaroslavl|Bellagio|-1|0||10800|2018-02-01 12:09:00@Bellagio|贝拉焦，伦巴第大区，意大利|city|32001|bellagio|32001|bellagio|%E8%B4%9D%E6%8B%89%E7%84%A6|103|0||3600|2018-02-01 12:09:00@Bellagio%26%2339%3Bs%20Sunrise|Bellagio's%20Sunrise，贝拉焦，伦巴第大区，意大利|hotel|9465818|贝拉焦，伦巴第大区，意大利|32001|bellagio|Bellagio's%20Sunrise|-1|0||3600|2018-02-01 12:09:00@Bellagio%20Lake%20View%20Villa|Bellagio%20Lake%20View%20Villa，奥利韦托拉廖，伦巴第大区，意大利|hotel|9965920|奥利韦托拉廖，伦巴第大区，意大利|69454||Bellagio%20Lake%20View%20Villa|-1|0||3600|2018-02-01 12:09:00@Bellagio%20Mini-Hotel|Bellagio%20Mini-Hotel，皮聪大，阿布哈兹自治共和国，格鲁吉亚|hotel|10018019|皮聪大，阿布哈兹自治共和国，格鲁吉亚|78451||Bellagio%20Mini-Hotel|-1|0||14400|2018-02-01 12:09:00@Bellagio%20Hotel|Bellagio%20Hotel，基加利，基加利市，卢旺达|hotel|10043062|基加利，基加利市，卢旺达|1277|kigali|Bellagio%20Hotel|-1|0||7200|2018-02-01 12:09:00@Bellagio%20Apartment%20-%20Como%20Lake|Bellagio%20Apartment%20-%20Como%20Lake，莱科，伦巴第大区，意大利|hotel|10062753|莱科，伦巴第大区，意大利|9841|lecco|Bellagio%20Apartment%20-%20Como%20Lake|-1|0||3600|2018-02-01 12:09:00@Bellagio%20Tower%20Apartment|Bellagio%20Tower%20Apartment，埃斯特角城，马尔多纳多省，乌拉圭|hotel|10572355|埃斯特角城，马尔多纳多省，乌拉圭|5563|puntadeleste|Bellagio%20Tower%20Apartment|-1|0||-10800|2018-02-01 12:09:00@Bellagio%20Mansion%20Apartment%20by%20Mediapura|Bellagio%20Mansion%20Apartment%20by%20Mediapura，雅加达，雅加达首都特区，印度尼西亚|hotel|10575154|雅加达，雅加达首都特区，印度尼西亚|524|jakarta|Bellagio%20Mansion%20Apartment%20by%20Mediapura|-1|0||25200|2018-02-01 12:09:00@Bellagio%20Terrace|Bellagio%20Terrace，里贾纳，萨斯喀彻温省，加拿大|hotel|10889428|里贾纳，萨斯喀彻温省，加拿大|3841|regina|Bellagio%20Terrace|-1|0||-21600|2018-02-01 12:09:00@Bellagio%20Tower|Bellagio%20Tower，埃斯特角城，马尔多纳多省，乌拉圭|hotel|11496230|埃斯特角城，马尔多纳多省，乌拉圭|5563|puntadeleste|Bellagio%20Tower|-1|0||-10800|2018-02-01 12:09:00@Bellagio%20Towers%20by%20Stays%20PH|Bellagio%20Towers%20by%20Stays%20PH，塔吉格，国家首都区，菲律宾|hotel|13665890|塔吉格，国家首都区，菲律宾|35808|taguig|Bellagio%20Towers%20by%20Stays%20PH|-1|0||28800|2018-02-01 12:09:00@Bellagio%20Apartment|Bellagio%20Apartment，布拉格，捷克|hotel|14201525|布拉格，捷克|1288|prague|Bellagio%20Apartment|-1|0||3600|2018-02-01 12:09:00@Bellagio|%E8%B4%9D%E6%8B%89%E5%90%89%E5%A5%A5%E5%BA%A6%E5%81%87%E6%9D%91，拉斯维加斯，内华达州，美国|hotel|715163|拉斯维加斯，内华达州，美国|26282|lasvegas|%E8%B4%9D%E6%8B%89%E5%90%89%E5%A5%A5%E5%BA%A6%E5%81%87%E6%9D%91|-1|0||-28800|2018-02-01 12:09:00@Bellagio%20Hotel%20Complex|%E8%B4%9D%E6%8B%89%E5%90%89%E5%A5%A5%E7%BB%BC%E5%90%88%E9%85%92%E5%BA%97，埃里温，亚美尼亚|hotel|3119343|埃里温，亚美尼亚|3245|yerevan|%E8%B4%9D%E6%8B%89%E5%90%89%E5%A5%A5%E7%BB%BC%E5%90%88%E9%85%92%E5%BA%97|-1|0||14400|2018-02-01 12:09:00"}
  ```
  以`@`为分割符分割`response【"data"]`，分割出的每一条对应携程匹配出的一家酒店
  取出分割出的第一家酒店，再次以`|`分割这条数据，切出第一个字段为酒店英文名，判断和name是否相符，若相符，则继续
  切除的第二个字段为该酒店的英文名和地址，以`，`为分割符分割该字段，分割出的第一条即为酒店中文名，
  更新该document字段ctrip_name为该条数据
  
 
 # 2018 - 03 - 16
 
#### 背景
从携程抓取的酒店中文名不完全
#### 目的
调用翻译接口进行翻译，补充没有抓到的中文名数据。
#### How
1. 一次从statics.hotels.bonotel/hotelbeds/hotelpro/roomsxml四个表中取出没有ctrip_name的数据插入statics.hotels.without_ctrip_name新表中
2. 依次从新表中取出每条数据，请求翻译接口，解析出相应中的中文名
3. 根据数据中的ori_id在旧表中更新ctrip_name字段
#### 代码细节
一开始没考虑到接口能承受的压力，和第三方翻译服务的限制，高并发抓取数据，导致出现大量503，所以改为了一次请求一个。


# 2018 - 04 - 20
#### 背景\
- 第三方数据的图片地址都是供应商的，为了提高加载速度，我们把它们存入cdn中。
- hotelspro/jactravel 上传cdn图片失败
- 图片过多，OSS空间占用过多
#### 目的
- 修复hotelspro上传图片失败
- 只上传酒店星级大于等于3星的，减少oss空间占用
#### How
- jactravel是一直没有，待添加
  hotelspro测试时因为图片需翻墙才能访问，已添加代理，这部分也添加了抛出异常，以便重跑
```python
        try:
        resp = requests.get(ori_url, proxies=settings.PROXIES)
    except Exception as exc:
        raise UploadFailed(ori_url) from exc
    body = resp.content
    if resp.status_code != 200 or not body:
        raise UploadFailed(
            ori_url, f'<{resp.status_code}>{resp.text}'
        )
```
 测试时发现hotelspro的新document有为None的，所以修改为
 ```python
doc['cdn_images'] = self.image_saver.upload_images(
                [img for img in (doc.get('images') or []) if img],
                ori_images
            )

```
- 只上传酒店星级大于等于3星的
```python
 if document['wgstar'] >= 3:
                self.save_images(ori_document, document)

```


# 2018 - 04 - 26
#### 背景
- hotelspro上传cdn图片失败
#### 目的
统计AOS供应商上传图片成功率.
#### How
success = 0
count = 0
遍历供应wgstar不小于3的document, 
```
count += len(doc.get('images') or [])
if 'cdn_images' in doc:
    for url in (doc.get('cdn_images') or []):
        try:
            if OSS.object_exists(URL(url).path):
                success += 1
```
最后得到 成功个数success和总数count，成功率success/count
