# coding: utf8


def split(string, *, replace={}, drop={}, delimiter=None):
    for _from, _to in replace.items():
        string = string.replace(_from, _to)

    for _drop, seq in drop.items():
        if seq is not None:
            string = string.split(_drop)[seq]
        else:
            string = string.replace(_drop, '')

    if delimiter:
        return string.split(delimiter)
    return string.split()
