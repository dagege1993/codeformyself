# coding: utf-8
"""
修复cdn不完整图片
created at 2017-8-29
by LensHo
"""

import logging
import base64
import binascii

import oss2
import requests
from pymongo import MongoClient

from scripture import settings


logger = logging.getLogger(__name__)

oss_auth = oss2.Auth(settings.OSS_SCRIPTURE_ACCESS_KEY_ID,
                     settings.OSS_SCRIPTURE_ACCESS_KEY_SECRET)

oss_bucket = oss2.Bucket(oss_auth,
                         settings.OSS_SCRIPTURE_ENDPOINT,
                         'weegotr-statics')

mc = MongoClient()
db = mc.cdn_pic

UPYUN = 'migrater'

upyun_base_url = 'http://v0.api.upyun.com/weegotest/'


def compare_md5():
    for oss_obj in oss2.ObjectIterator(oss_bucket, prefix='upyun'):
        if db.ok.find_one({'aliyun': oss_obj.key}):
            continue

        try:
            md5_aliyun = oss_bucket.head_object(
                oss_obj.key).headers['Content-MD5']
        except:
            db.wrong_ali.insert_one({'url': oss_obj.key})
            logger.error('error occurs when get %s Content-Md5', oss_obj.key)
            continue
        md5_aliyun = binascii.hexlify(
            base64.decodebytes(md5_aliyun.encode('utf-8'))
        ).decode()

        url = upyun_base_url + oss_obj.key[6:]
        try:
            md5_upyun = requests.head(url,
                                      auth=(UPYUN, UPYUN)).headers['Content-Md5']
        except:
            db.wrong_upy.insert_one({'url': url})
            logger.error('error occurs when get %s Content-Md5', url)
            continue
        if md5_aliyun != md5_upyun:
            db.pic_diff.insert_one({'aliyun': oss_obj.key, 'upyun': url})
            logger.error('different md5 %s %s', oss_obj.key, url)
            continue
        db.ok.insert_one({'aliyun': oss_obj.key})
        logger.debug('%s is ok', oss_obj.key)


pics_different = """upyun/attractions/iosimgs/570b74d224e4b3334b000008.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/570b74d224e4b3334b000008.jpeg
    upyun/attractions/iosimgs/570b800524e4b3334b000020.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/570b800524e4b3334b000020.jpeg
    upyun/attractions/iosimgs/5714afe4b35cc5d62c0000e6.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5714afe4b35cc5d62c0000e6.png
    upyun/attractions/iosimgs/571d91e451d9a75d0300000d.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/571d91e451d9a75d0300000d.jpeg
    upyun/attractions/iosimgs/571dff3e51d9a75d03000134.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/571dff3e51d9a75d03000134.jpeg
    upyun/attractions/iosimgs/5722fdc4a82d62fe58000036.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5722fdc4a82d62fe58000036.png
    upyun/attractions/iosimgs/5722fdfda82d62fe5800003a.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5722fdfda82d62fe5800003a.png
    upyun/attractions/iosimgs/573c3b4b5949965f12000083.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573c3b4b5949965f12000083.jpeg
    upyun/attractions/iosimgs/573c3b595949965f12000085.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573c3b595949965f12000085.jpeg
    upyun/attractions/iosimgs/573c50a05949965f120000d9.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573c50a05949965f120000d9.jpeg
    upyun/attractions/iosimgs/573d5de75949965f1200011b.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573d5de75949965f1200011b.jpeg
    upyun/attractions/iosimgs/573d8bff5949965f120001ae.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573d8bff5949965f120001ae.jpeg
    upyun/attractions/iosimgs/573d9a4c5949965f12000216.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573d9a4c5949965f12000216.png
    upyun/attractions/iosimgs/573e75c75949965f120002a7.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573e75c75949965f120002a7.jpeg
    upyun/attractions/iosimgs/573e80985949965f120002ee.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573e80985949965f120002ee.jpeg
    upyun/attractions/iosimgs/573e83795949965f12000307.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573e83795949965f12000307.jpeg
    upyun/attractions/iosimgs/573e8f66fc57224023000060.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573e8f66fc57224023000060.jpeg
    upyun/attractions/iosimgs/573ed78ffc5722402300023d.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573ed78ffc5722402300023d.jpeg
    upyun/attractions/iosimgs/573ee5059ed831f604000008.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/573ee5059ed831f604000008.jpeg
    upyun/attractions/iosimgs/5742712a912c73d62b00006b.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742712a912c73d62b00006b.png
    upyun/attractions/iosimgs/574272ef912c73d62b000076.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/574272ef912c73d62b000076.jpeg
    upyun/attractions/iosimgs/574273d2912c73d62b000083.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/574273d2912c73d62b000083.jpeg
    upyun/attractions/iosimgs/574274af912c73d62b00008e.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/574274af912c73d62b00008e.jpeg
    upyun/attractions/iosimgs/57427976912c73d62b0000b4.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57427976912c73d62b0000b4.jpeg
    upyun/attractions/iosimgs/574279c2912c73d62b0000ba.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/574279c2912c73d62b0000ba.jpeg
    upyun/attractions/iosimgs/57427b03912c73d62b0000d5.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57427b03912c73d62b0000d5.jpeg
    upyun/attractions/iosimgs/57427c02912c73d62b0000e2.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57427c02912c73d62b0000e2.jpeg
    upyun/attractions/iosimgs/57429b25912c73d62b000158.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57429b25912c73d62b000158.jpeg
    upyun/attractions/iosimgs/5742a430912c73d62b0001da.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742a430912c73d62b0001da.png
    upyun/attractions/iosimgs/5742aac3912c73d62b0001f5.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742aac3912c73d62b0001f5.png
    upyun/attractions/iosimgs/5742aad3912c73d62b0001fb.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742aad3912c73d62b0001fb.png
    upyun/attractions/iosimgs/5742b971190c0b0e0200004d.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742b971190c0b0e0200004d.png
    upyun/attractions/iosimgs/5742bac8190c0b0e02000063.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742bac8190c0b0e02000063.png
    upyun/attractions/iosimgs/5742bb89190c0b0e0200006a.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742bb89190c0b0e0200006a.png
    upyun/attractions/iosimgs/5742bb92190c0b0e0200006e.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742bb92190c0b0e0200006e.png
    upyun/attractions/iosimgs/5742bce6190c0b0e02000082.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5742bce6190c0b0e02000082.png
    upyun/attractions/iosimgs/5747e816190c0b0e020001f9.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5747e816190c0b0e020001f9.png
    upyun/attractions/iosimgs/5747e836190c0b0e02000203.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5747e836190c0b0e02000203.png
    upyun/attractions/iosimgs/5749136b190c0b0e020002ed.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5749136b190c0b0e020002ed.jpeg
    upyun/attractions/iosimgs/5757d787eb33b5755b000040.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5757d787eb33b5755b000040.jpeg
    upyun/attractions/iosimgs/5780d2b44d5bd88e32000162.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5780d2b44d5bd88e32000162.jpeg
    upyun/attractions/iosimgs/57833d2a4d5bd88e3200016f.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57833d2a4d5bd88e3200016f.jpeg
    upyun/attractions/iosimgs/578341a04d5bd88e3200018e.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/578341a04d5bd88e3200018e.jpeg
    upyun/attractions/iosimgs/5784678de162b01475000010.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5784678de162b01475000010.jpeg
    upyun/attractions/iosimgs/5791db49bd9ee9d10700016b.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5791db49bd9ee9d10700016b.jpeg
    upyun/attractions/iosimgs/5791ebafbd9ee9d1070001ae.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5791ebafbd9ee9d1070001ae.jpeg
    upyun/attractions/iosimgs/57970286bd9ee9d10700020c.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57970286bd9ee9d10700020c.jpeg
    upyun/attractions/iosimgs/5797035fbd9ee9d107000215.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5797035fbd9ee9d107000215.jpeg
    upyun/attractions/iosimgs/57973a00bd9ee9d107000239.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57973a00bd9ee9d107000239.png
    upyun/attractions/iosimgs/57973efabd9ee9d10700024e.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57973efabd9ee9d10700024e.png
    upyun/attractions/iosimgs/579740aabd9ee9d107000252.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/579740aabd9ee9d107000252.jpeg
    upyun/attractions/iosimgs/57a189e0958235cd08000002.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57a189e0958235cd08000002.jpeg
    upyun/attractions/iosimgs/57a1909e958235cd0800000a.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57a1909e958235cd0800000a.jpeg
    upyun/attractions/iosimgs/57a1929f958235cd0800001a.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57a1929f958235cd0800001a.png
    upyun/attractions/iosimgs/57a19c14958235cd0800001f.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/57a19c14958235cd0800001f.jpeg
    upyun/attractions/iosimgs/582abb8c7cdc62f545000040.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582abb8c7cdc62f545000040.jpeg
    upyun/attractions/iosimgs/582adca77cdc62f54500005d.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582adca77cdc62f54500005d.jpeg
    upyun/attractions/iosimgs/582d10319512b6b91d000084.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582d10319512b6b91d000084.png
    upyun/attractions/iosimgs/582d11519512b6b91d000088.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582d11519512b6b91d000088.png
    upyun/attractions/iosimgs/582d13db9512b6b91d000091.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582d13db9512b6b91d000091.png
    upyun/attractions/iosimgs/582d73cc9512b6b91d0001cd.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582d73cc9512b6b91d0001cd.png
    upyun/attractions/iosimgs/582d7d8e9512b6b91d0001fc.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582d7d8e9512b6b91d0001fc.png
    upyun/attractions/iosimgs/582ea5029512b6b91d00033c.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/582ea5029512b6b91d00033c.jpeg
    upyun/attractions/iosimgs/583502aa9f34bd843100028a.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583502aa9f34bd843100028a.jpeg
    upyun/attractions/iosimgs/5836a7a9de75e9d423000139.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5836a7a9de75e9d423000139.jpeg
    upyun/attractions/iosimgs/5836a7b1de75e9d42300013d.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5836a7b1de75e9d42300013d.jpeg
    upyun/attractions/iosimgs/5839323aa35440685000001a.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5839323aa35440685000001a.jpeg
    upyun/attractions/iosimgs/583935d8a354406850000027.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583935d8a354406850000027.jpeg
    upyun/attractions/iosimgs/5839411ea3544068500000a3.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5839411ea3544068500000a3.jpeg
    upyun/attractions/iosimgs/583941d4a3544068500000a9.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583941d4a3544068500000a9.jpeg
    upyun/attractions/iosimgs/583941d4a3544068500000af.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583941d4a3544068500000af.jpeg
    upyun/attractions/iosimgs/58394608a3544068500000dd.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58394608a3544068500000dd.jpeg
    upyun/attractions/iosimgs/58394641a3544068500000df.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58394641a3544068500000df.jpeg
    upyun/attractions/iosimgs/58394e39a35440685000011e.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58394e39a35440685000011e.jpeg
    upyun/attractions/iosimgs/58394e57a354406850000120.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58394e57a354406850000120.jpeg
    upyun/attractions/iosimgs/583cdb05d7db855272000070.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583cdb05d7db855272000070.jpeg
    upyun/attractions/iosimgs/583d09e3d7db8552720000be.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d09e3d7db8552720000be.png
    upyun/attractions/iosimgs/583d09e4d7db8552720000c4.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d09e4d7db8552720000c4.png
    upyun/attractions/iosimgs/583d109ed7db8552720000e7.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d109ed7db8552720000e7.png
    upyun/attractions/iosimgs/583d1140d7db8552720000ed.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d1140d7db8552720000ed.png
    upyun/attractions/iosimgs/583d1faed7db8552720000fc.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d1faed7db8552720000fc.png
    upyun/attractions/iosimgs/583d230cd7db85527200010f.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d230cd7db85527200010f.png
    upyun/attractions/iosimgs/583d34a1d7db85527200013d.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d34a1d7db85527200013d.png
    upyun/attractions/iosimgs/583d379fd7db85527200014e.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d379fd7db85527200014e.png
    upyun/attractions/iosimgs/583d41f9d7db85527200016e.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d41f9d7db85527200016e.png
    upyun/attractions/iosimgs/583d4b2ed7db855272000182.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d4b2ed7db855272000182.png
    upyun/attractions/iosimgs/583d65f1d7db8552720001a9.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d65f1d7db8552720001a9.png
    upyun/attractions/iosimgs/583d8f2fd7db8552720001df.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583d8f2fd7db8552720001df.png
    upyun/attractions/iosimgs/583db322d7db8552720001f5.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583db322d7db8552720001f5.png
    upyun/attractions/iosimgs/583db72dd7db855272000200.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583db72dd7db855272000200.png
    upyun/attractions/iosimgs/583db9fed7db85527200020d.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583db9fed7db85527200020d.png
    upyun/attractions/iosimgs/583df5d1d7db855272000241.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583df5d1d7db855272000241.png
    upyun/attractions/iosimgs/583dfa1bd7db855272000247.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/583dfa1bd7db855272000247.png
    upyun/attractions/iosimgs/58412155ffaa23d63c00002d.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58412155ffaa23d63c00002d.jpeg
    upyun/attractions/iosimgs/58412707ffaa23d63c00005b.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58412707ffaa23d63c00005b.jpeg
    upyun/attractions/iosimgs/584626708e6c19cd3a000018.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584626708e6c19cd3a000018.jpeg
    upyun/attractions/iosimgs/584632b58e6c19cd3a000028.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584632b58e6c19cd3a000028.png
    upyun/attractions/iosimgs/584634688e6c19cd3a00002a.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584634688e6c19cd3a00002a.png
    upyun/attractions/iosimgs/58465a4eeee27b6b7f00000a.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58465a4eeee27b6b7f00000a.png
    upyun/attractions/iosimgs/584b8ce32570f081410001cc.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584b8ce32570f081410001cc.png
    upyun/attractions/iosimgs/584b93852570f081410001dc.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584b93852570f081410001dc.png
    upyun/attractions/iosimgs/584ba20d2570f081410001fe.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584ba20d2570f081410001fe.jpeg
    upyun/attractions/iosimgs/584ba4242570f08141000200.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584ba4242570f08141000200.png
    upyun/attractions/iosimgs/584ba7332570f08141000213.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/584ba7332570f08141000213.png
    upyun/attractions/iosimgs/585218e3dbf273bc57000020.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/585218e3dbf273bc57000020.png
    upyun/attractions/iosimgs/585218e3dbf273bc57000022.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/585218e3dbf273bc57000022.png
    upyun/attractions/iosimgs/5852194fdbf273bc57000030.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5852194fdbf273bc57000030.png
    upyun/attractions/iosimgs/58521ccbdbf273bc57000046.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58521ccbdbf273bc57000046.png
    upyun/attractions/iosimgs/5857a37393aaea7978000054.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5857a37393aaea7978000054.png
    upyun/attractions/iosimgs/5857a37593aaea7978000056.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5857a37593aaea7978000056.png
    upyun/attractions/iosimgs/5857a37593aaea7978000058.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5857a37593aaea7978000058.png
    upyun/attractions/iosimgs/5857a37793aaea797800005c.png , http://v0.api.upyun.com/weegotest/attractions/iosimgs/5857a37793aaea797800005c.png
    upyun/attractions/iosimgs/586b7932224c8cf732000342.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/586b7932224c8cf732000342.jpeg
    upyun/attractions/iosimgs/58844014028b837c6a00003c.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58844014028b837c6a00003c.jpeg
    upyun/attractions/iosimgs/58afa25af54a88a31500002a.jpeg , http://v0.api.upyun.com/weegotest/attractions/iosimgs/58afa25af54a88a31500002a.jpeg
    upyun/shopping/iosimgs/55caaacb8531934f4f000084.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caaacb8531934f4f000084.jpeg
    upyun/shopping/iosimgs/55caaad48531934f4f000086.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caaad48531934f4f000086.jpeg
    upyun/shopping/iosimgs/55caaf095062d43e1a000062.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caaf095062d43e1a000062.jpeg
    upyun/shopping/iosimgs/55caaf4a5062d43e1a000076.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caaf4a5062d43e1a000076.jpeg
    upyun/shopping/iosimgs/55cab0a05062d43e1a0000b0.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cab0a05062d43e1a0000b0.jpeg
    upyun/shopping/iosimgs/55cab9d45c2555f92400003c.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cab9d45c2555f92400003c.png
    upyun/shopping/iosimgs/55cabf1c8fb2cd6f2b000008.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cabf1c8fb2cd6f2b000008.jpeg
    upyun/shopping/iosimgs/55cabf348fb2cd6f2b000012.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cabf348fb2cd6f2b000012.jpeg
    upyun/shopping/iosimgs/55cac18c8fb2cd6f2b000036.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cac18c8fb2cd6f2b000036.jpeg
    upyun/shopping/iosimgs/55cac1a16936997c0a000052.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cac1a16936997c0a000052.jpeg
    upyun/shopping/iosimgs/55cac3106936997c0a000060.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cac3106936997c0a000060.jpeg
    upyun/shopping/iosimgs/55cacaabfe3d2b7f30000050.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cacaabfe3d2b7f30000050.jpeg
    upyun/shopping/iosimgs/55cad5ee79608a6134000010.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cad5ee79608a6134000010.jpeg
    upyun/shopping/iosimgs/55caec8d6936997c0a00026c.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caec8d6936997c0a00026c.jpeg
    upyun/shopping/iosimgs/55caeca56936997c0a00026e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caeca56936997c0a00026e.jpeg
    upyun/shopping/iosimgs/55caf7f06936997c0a000300.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caf7f06936997c0a000300.jpeg
    upyun/shopping/iosimgs/55caf9226936997c0a00031e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55caf9226936997c0a00031e.jpeg
    upyun/shopping/iosimgs/55cb17976936997c0a000426.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb17976936997c0a000426.jpeg
    upyun/shopping/iosimgs/55cb17a7cf8b79675200001a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb17a7cf8b79675200001a.jpeg
    upyun/shopping/iosimgs/55cb18d1cf8b796752000022.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb18d1cf8b796752000022.jpeg
    upyun/shopping/iosimgs/55cb1983cf8b79675200002a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb1983cf8b79675200002a.jpeg
    upyun/shopping/iosimgs/55cb19f8cf8b79675200002e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb19f8cf8b79675200002e.jpeg
    upyun/shopping/iosimgs/55cb1a40cf8b796752000032.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb1a40cf8b796752000032.jpeg
    upyun/shopping/iosimgs/55cb1dc46936997c0a00048c.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb1dc46936997c0a00048c.jpeg
    upyun/shopping/iosimgs/55cb1e6b6936997c0a00049e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb1e6b6936997c0a00049e.jpeg
    upyun/shopping/iosimgs/55cb2e996936997c0a0004f4.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb2e996936997c0a0004f4.jpeg
    upyun/shopping/iosimgs/55cb31a4fc9bab0d6200000a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb31a4fc9bab0d6200000a.jpeg
    upyun/shopping/iosimgs/55cb32b08a8ea4b417000002.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb32b08a8ea4b417000002.jpeg
    upyun/shopping/iosimgs/55cb32e88a8ea4b417000004.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb32e88a8ea4b417000004.jpeg
    upyun/shopping/iosimgs/55cb32e88a8ea4b417000006.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb32e88a8ea4b417000006.jpeg
    upyun/shopping/iosimgs/55cb3aafa74283ba6200002e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3aafa74283ba6200002e.jpeg
    upyun/shopping/iosimgs/55cb3b438a8ea4b417000016.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3b438a8ea4b417000016.png
    upyun/shopping/iosimgs/55cb3c2b8a8ea4b417000028.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3c2b8a8ea4b417000028.jpeg
    upyun/shopping/iosimgs/55cb3d628a8ea4b417000030.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3d628a8ea4b417000030.jpeg
    upyun/shopping/iosimgs/55cb3d7a376493f364000008.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3d7a376493f364000008.jpeg
    upyun/shopping/iosimgs/55cb3d95376493f364000012.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3d95376493f364000012.png
    upyun/shopping/iosimgs/55cb3db0376493f364000018.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3db0376493f364000018.png
    upyun/shopping/iosimgs/55cb3e3f8a8ea4b417000036.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3e3f8a8ea4b417000036.jpeg
    upyun/shopping/iosimgs/55cb3e528a8ea4b417000038.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3e528a8ea4b417000038.jpeg
    upyun/shopping/iosimgs/55cb3e538a8ea4b41700003a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3e538a8ea4b41700003a.jpeg
    upyun/shopping/iosimgs/55cb3e84376493f364000030.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb3e84376493f364000030.jpeg
    upyun/shopping/iosimgs/55cb42d4d0b4b1be66000010.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb42d4d0b4b1be66000010.jpeg
    upyun/shopping/iosimgs/55cb4646f1cb31cd67000018.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb4646f1cb31cd67000018.jpeg
    upyun/shopping/iosimgs/55cb4c598a8ea4b4170000ce.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb4c598a8ea4b4170000ce.jpeg
    upyun/shopping/iosimgs/55cb51088a8ea4b417000104.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cb51088a8ea4b417000104.jpeg
    upyun/shopping/iosimgs/55cd4bfa6f876ceb47000004.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cd4bfa6f876ceb47000004.png
    upyun/shopping/iosimgs/55cd4ecf6f876ceb4700001c.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cd4ecf6f876ceb4700001c.jpeg
    upyun/shopping/iosimgs/55cd6983383958f856000014.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/55cd6983383958f856000014.jpeg
    upyun/shopping/iosimgs/562d9a54d0f0c1f97b000008.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/562d9a54d0f0c1f97b000008.jpeg
    upyun/shopping/iosimgs/562d9aa9d0f0c1f97b00000a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/562d9aa9d0f0c1f97b00000a.jpeg
    upyun/shopping/iosimgs/569a129dcbaa92e70d00002b.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569a129dcbaa92e70d00002b.jpeg
    upyun/shopping/iosimgs/569da9dcd97041ae14000035.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569da9dcd97041ae14000035.jpeg
    upyun/shopping/iosimgs/569dab866a81d59a15000018.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569dab866a81d59a15000018.jpeg
    upyun/shopping/iosimgs/569db4486a81d59a150000ce.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569db4486a81d59a150000ce.jpeg
    upyun/shopping/iosimgs/569db69a6a81d59a15000115.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569db69a6a81d59a15000115.jpeg
    upyun/shopping/iosimgs/569dc0b86a81d59a15000188.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569dc0b86a81d59a15000188.jpeg
    upyun/shopping/iosimgs/569deccb722a59013100000d.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569deccb722a59013100000d.jpeg
    upyun/shopping/iosimgs/569dfb4e7e70ed4b39000062.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569dfb4e7e70ed4b39000062.jpeg
    upyun/shopping/iosimgs/569dfbc67e70ed4b3900006c.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569dfbc67e70ed4b3900006c.jpeg
    upyun/shopping/iosimgs/569e005ffbc72cd63d000027.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/569e005ffbc72cd63d000027.jpeg
    upyun/shopping/iosimgs/56a04ae0e6ecbfab36000021.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a04ae0e6ecbfab36000021.jpeg
    upyun/shopping/iosimgs/56a2fd8051a85fa277000144.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fd8051a85fa277000144.jpeg
    upyun/shopping/iosimgs/56a2fdd551a85fa277000148.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fdd551a85fa277000148.png
    upyun/shopping/iosimgs/56a2fdd651a85fa27700014a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fdd651a85fa27700014a.jpeg
    upyun/shopping/iosimgs/56a2fe7451a85fa277000150.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fe7451a85fa277000150.jpeg
    upyun/shopping/iosimgs/56a2fe8f51a85fa277000152.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fe8f51a85fa277000152.jpeg
    upyun/shopping/iosimgs/56a2fec151a85fa277000156.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fec151a85fa277000156.png
    upyun/shopping/iosimgs/56a2fee151a85fa27700015a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fee151a85fa27700015a.jpeg
    upyun/shopping/iosimgs/56a2fef351a85fa27700015e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fef351a85fa27700015e.jpeg
    upyun/shopping/iosimgs/56a2fef351a85fa277000160.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fef351a85fa277000160.jpeg
    upyun/shopping/iosimgs/56a2ff3251a85fa277000162.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2ff3251a85fa277000162.jpeg
    upyun/shopping/iosimgs/56a2ffbd51a85fa277000166.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2ffbd51a85fa277000166.jpeg
    upyun/shopping/iosimgs/56a2fffd51a85fa277000168.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a2fffd51a85fa277000168.jpeg
    upyun/shopping/iosimgs/56a340a69881fcc87d000032.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a340a69881fcc87d000032.jpeg
    upyun/shopping/iosimgs/56a7237f29dab5811800010e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56a7237f29dab5811800010e.jpeg
    upyun/shopping/iosimgs/56ac34fe1d65d5f63400001a.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56ac34fe1d65d5f63400001a.jpeg
    upyun/shopping/iosimgs/56b0864078fc52214e000028.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56b0864078fc52214e000028.jpeg
    upyun/shopping/iosimgs/56b08d2678fc52214e000044.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56b08d2678fc52214e000044.jpeg
    upyun/shopping/iosimgs/56d12804c59bb6b474000055.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d12804c59bb6b474000055.jpeg
    upyun/shopping/iosimgs/56d15106c59bb6b47400005d.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d15106c59bb6b47400005d.jpeg
    upyun/shopping/iosimgs/56d172e2c59bb6b4740000b3.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d172e2c59bb6b4740000b3.png
    upyun/shopping/iosimgs/56d172f6c59bb6b4740000b7.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d172f6c59bb6b4740000b7.png
    upyun/shopping/iosimgs/56d4253cf1dd31c60a000031.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d4253cf1dd31c60a000031.jpeg
    upyun/shopping/iosimgs/56d427eff1dd31c60a00003d.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d427eff1dd31c60a00003d.jpeg
    upyun/shopping/iosimgs/56d5393c9d8c03c010000006.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56d5393c9d8c03c010000006.jpeg
    upyun/shopping/iosimgs/56f90984f96e6047400000ea.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56f90984f96e6047400000ea.jpeg
    upyun/shopping/iosimgs/56f909cff96e6047400000ee.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/56f909cff96e6047400000ee.jpeg
    upyun/shopping/iosimgs/57034e77fb42ceae7100009d.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/57034e77fb42ceae7100009d.png
    upyun/shopping/iosimgs/570354e3fb42ceae710000b1.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/570354e3fb42ceae710000b1.jpeg
    upyun/shopping/iosimgs/5704e76bd6f883220b000167.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/5704e76bd6f883220b000167.png
    upyun/shopping/iosimgs/570b778c24e4b3334b00000e.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/570b778c24e4b3334b00000e.jpeg
    upyun/shopping/iosimgs/574279ff912c73d62b0000bc.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/574279ff912c73d62b0000bc.jpeg
    upyun/shopping/iosimgs/582c1aaf9512b6b91d000044.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/582c1aaf9512b6b91d000044.jpeg
    upyun/shopping/iosimgs/58300c68ae95a1e218000019.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58300c68ae95a1e218000019.png
    upyun/shopping/iosimgs/583e7220d7db8552720002fe.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7220d7db8552720002fe.png
    upyun/shopping/iosimgs/583e7911d7db855272000306.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7911d7db855272000306.png
    upyun/shopping/iosimgs/583e7912d7db855272000308.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7912d7db855272000308.png
    upyun/shopping/iosimgs/583e7afdd7db85527200030d.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7afdd7db85527200030d.png
    upyun/shopping/iosimgs/583e7afdd7db855272000313.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7afdd7db855272000313.png
    upyun/shopping/iosimgs/583e7d7dd7db855272000319.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e7d7dd7db855272000319.png
    upyun/shopping/iosimgs/583e833bd7db85527200032d.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e833bd7db85527200032d.png
    upyun/shopping/iosimgs/583e833cd7db85527200032f.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e833cd7db85527200032f.png
    upyun/shopping/iosimgs/583e8a60d7db855272000351.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e8a60d7db855272000351.png
    upyun/shopping/iosimgs/583e8a61d7db855272000353.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e8a61d7db855272000353.png
    upyun/shopping/iosimgs/583e8a64d7db855272000355.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e8a64d7db855272000355.png
    upyun/shopping/iosimgs/583e8e7f328e737e1c00000a.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/583e8e7f328e737e1c00000a.png
    upyun/shopping/iosimgs/584a508e2570f081410000a0.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/584a508e2570f081410000a0.jpeg
    upyun/shopping/iosimgs/584a50942570f081410000a4.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/584a50942570f081410000a4.jpeg
    upyun/shopping/iosimgs/5859e26d93aaea797800011f.png , http://v0.api.upyun.com/weegotest/shopping/iosimgs/5859e26d93aaea797800011f.png
    upyun/shopping/iosimgs/58845ab2028b837c6a0000b2.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58845ab2028b837c6a0000b2.jpeg
    upyun/shopping/iosimgs/58845abb028b837c6a0000b4.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58845abb028b837c6a0000b4.jpeg
    upyun/shopping/iosimgs/58845c6a028b837c6a0000ba.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58845c6a028b837c6a0000ba.jpeg
    upyun/shopping/iosimgs/58845c6e028b837c6a0000bc.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58845c6e028b837c6a0000bc.jpeg
    upyun/shopping/iosimgs/58845c76028b837c6a0000be.jpeg , http://v0.api.upyun.com/weegotest/shopping/iosimgs/58845c76028b837c6a0000be.jpeg"""


def fix():
    for pic in pics_different.split('\n'):
        ali_pic, up_pic = pic.split(' , ')
        try:
            resp = requests.get(up_pic, auth=(UPYUN, UPYUN))
            upyun_md5 = resp.headers['Content-Md5']
            oss_bucket.put_object(ali_pic, resp)
            ali_md5 = oss_bucket.head_object(ali_pic).headers['Content-MD5']
            aliyun_md5 = binascii.hexlify(
                base64.decodebytes(ali_md5.encode('utf-8'))).decode()

            if aliyun_md5 != upyun_md5:
                logger.error(
                    'md5 not equal aliyun: %s upyun: %s', ali_pic, up_pic
                )
            else:
                logger.info('successfully put %s', up_pic)
        except:
            logger.error('download or put error %s', up_pic)


if __name__ == '__main__':
    fix()
