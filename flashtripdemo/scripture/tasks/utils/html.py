# coding: utf-8
def take_first(page, path):
    return page.xpath(path)[0] if page.xpath(path) else ''


def take_last(page, path):
    return page.xpath(path)[-1] if page.xpath(path) else ''


def strip_str(s):
    return s.strip().strip(':') if isinstance(s, str) else ''


def strip_list(seq):
    if isinstance(seq, list):
        return [i.strip().strip(':') for i in seq if i.strip()]
    return []


def slice_list(seq, i):
    """
    slice list to two parts
    :param seq: list need to be slice
    :param i: index to slice
    :return: tuple of sliced list
        >>> slice_list([1, 2, 3], 1)
        [1], [2, 3]
        >>> slice_list([1, 2, 3], 4)
        [], []
    """
    if isinstance(seq, list) and len(seq) < abs(i):
        return [], []
    return seq[:i], seq[i:]


def unpack(seq, num_args=2):
    if isinstance(seq, list) and len(seq) == num_args:
        return seq
    return ['' for _ in range(num_args)]


def to_dict(seq_keys, seq_values):
    result = []
    if seq_keys and seq_values:
        for k, v in zip(seq_keys, seq_values):
            if v:
                if isinstance(v, list):
                    v = strip_list(v)
                elif isinstance(v, str):
                    v = strip_str(v)
                else:
                    pass
            result.append({
                'name': k.strip() if k else '',
                'value': v
            })
    return result


def group(seq, step=2, is_zip=True):
    if seq:
        a = [seq[i::step] for i in range(step)]
        if is_zip:
            return a
        else:
            x = []
            y = []
            for i in a:
                x.append(i[0])
                y.append(i[1])
            return x, y
    return ['' for _ in range(step)]


def filter_dict_value(seq):
    if isinstance(seq, list):
        return [i for i in seq if isinstance(i, dict) and i.get('value')]
    return []


def remove_space(s):
    return ' '.join(s.split()).strip() if isinstance(s, str) else ''