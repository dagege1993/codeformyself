# coding: utf8

import oss2
import fire
from pathlib import Path


class __G:
    bucket = None


def __init(ak, sk, endpoint, bucket):
    auth = oss2.Auth(ak, sk)
    __G.bucket = oss2.Bucket(auth, endpoint, bucket)


def upload(src, dst):
    resp = __G.bucket.put_object_from_file(dst, Path(src))
    assert resp.status == 200


def main(ak, sk, endpoint='', bucket='', src=None, dst=None):
    __init(ak, sk, endpoint, bucket)
    return upload(src, dst)


if __name__ == '__main__':
    fire.Fire(main)
