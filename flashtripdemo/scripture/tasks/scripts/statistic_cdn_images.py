# coding: utf-8

import enum
import json
import logging
import random

from typing import Tuple

import oss2
import coloredlogs

from yarl import URL

from tasks import settings
from tasks.utils.database import databases
from tasks.supplier_statics import BaseSupplier, Providers
from tasks.supplier_statics.supplier_images import ImageSaver


LOGGER = logging.getLogger(__name__)
LEVEL_STYLE = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'}
}
coloredlogs.install(
    level='DEBUG', isatty=True, level_styles=LEVEL_STYLE,
    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
)

AGENT = databases('agent')
auth = oss2.Auth(
    settings.OSS_ACCESS_KEY_ID,
    settings.OSS_SECRET_ACCESS_KEY
)
OSS = oss2.Bucket(auth, settings.OSS_ENDPOINT, settings.OSS_BUCKET)


def statistic_cdn_image(provider: enum.Enum) -> Tuple[int, int, str]:
    """ 上传document中cdn_images上传失败的图片，并统计供应商图片个数、成功个数、成功率

    Args:
       provider: 供应商
    Returns:
       图片总数，图片上传成功个数，成功率，cdn_images上传成功率
    """
    count = 0
    success = 0

    table = BaseSupplier(AGENT).table('hotels', provider)
    saver = ImageSaver(provider.value)

    for doc in table.find({'wgstar': {'$gt': 2}}):
        images = doc.get('images') or []
        count += len(images)

        if 'cdn_images' not in doc:
            continue

        ori_images = {URL(image).path: image for image in images}
        new_urls = []

        # 判断images是否存在，若不存在，上传
        for image in ori_images:
            key = f'agents/{provider.value}{image}'
            new_urls.append(str(URL(f'https://img{random.randint(3, 4)}.weegotr.com')
                                .with_path(key)))
            try:
                if OSS.object_exists(key):
                    success += 1
                    continue
                else:
                    saver.save(ori_images[image])
            except Exception as exc:
                LOGGER.error(f'Judge url {image} failed', exc_info=exc)

        # 若存在images中有，但cdn_images中无的image，则需更新cdn_images字段
        cdn_images = set(URL(cdn_image).path.replace(f'/agents/{provider.value}', '', 1)
                         for cdn_image in (doc.get('cdn_images') or []))
        if set(ori_images) - cdn_images:
            table.update_one(
                {'_id': doc['_id']},
                {"$set": {'cdn_images': new_urls}}
            )

        LOGGER.debug(f'[{provider.value}]Has judged {count} pictures, '
                     f'success {success}')
    return count, success, '{:.2%}'.format(success / count)


def main():
    """ 计算每家供应商的上传情况。

    Returns:
        供应商的上传数据

    Examples：
        [
          {
            "provider": "bonotel",
            "total_count": 6954,
            "success_count": 6954,
            "success rate": "100.00%"
          }
        ]
    """
    result = []
    for provider in Providers:
        count, success, rate = statistic_cdn_image(provider)
        LOGGER.info(f'{provider.value} 图片总数 {count}, '
                    f'上传成功图片总数 {success},'
                    f'上传成功比例{rate}')
        result.append({
            'provider': provider.value,
            'total_count': count,
            'success_count': success,
            'success rate': rate
        })
    LOGGER.info('统计上传cdn图片：\n{}'.format(json.dumps(result, indent=2)))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        LOGGER.critical('', exc_info=exc)
