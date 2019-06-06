# coding: utf8

from typing import List


def dupefilter(_list: List) -> List:
    if not _list:
        return _list
    return list(set(_list))
