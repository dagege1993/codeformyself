# coding: utf8

from pymongo import MongoClient
from scripture import settings

import random


m = MongoClient()
mc = MongoClient(settings.MONGO)


def get_address(rx):
    addr = rx['address']['address1'] or ' '
    addr += rx['address']['address2'] or ' '
    addr += rx['address']['address3'] or ' '
    addr += rx['address']['city'] or ' '
    addr += rx['address']['state'] or ' '
    _addr =  rx['name'] + ' | ' + addr
    return _addr.replace('  ', ' ').title()

def _addr(_id):
    addr = mc.scripture.jsets.find_one({'jset_id': _id})['how_to_get_there']
    return ','.join(addr)

q = {
    '$match': {
        'similarity': {'$gt': []},
        'similarity.0.1': {'$gte': 55, '$lt': 60}
    }
}

group = {'$group': {'_id': '$city', 'count': {'$sum': 1}}}


start = 45

while start < 100:
    start += 5
    count = {}

    q['$match']['similarity.0.1']['$gte'] = start
    q['$match']['similarity.0.1']['$lt'] = start + 5

    where = q['$match'].copy()

    agged = m.scripture.jset_name_similarities2.aggregate([q, group])

    for agg in agged:
        city = agg['_id']
        cnt = agg['count']
        where['city'] = city

        try:
            idxes = random.sample(range(0, cnt), 2)
        except:
            idxes = range(0, cnt)

        curs = m.scripture.jset_name_similarities2.find(where)

        # filename = ''  # {city.lower().replace(" ", "-")}'
        filename = f'similarities_{start}-{start+5}.txt'

        for idx in idxes:
            try:
                sim = curs[idx]
            except IndexError:
                print(
                    'Bad index:', idx, 'count:', count[sim['city']], 'start:',
                    start, 'stop:', start + 5)
            # jset_id = sim['jset_id']
            # jset = mc.scripture.jsets.find_one({'jset_id': jset_id})

            splitline = f'{"-"*30} {city.lower().replace(" ", "-")} {"-"*30}\n'
            jsetline = f'Jset name: {sim["name"]} | {_addr(sim["jset_id"])}\n'
            with open(filename, 'a') as records:
                records.write(splitline)
                records.write(jsetline)
            for s in sim['similarity']:
                room = mc.scripture.rxmls.find_one({'hotel_id': s[0]})
                if s[1] < 50:
                    break
                with open(filename, 'a') as records:
                    line = f'Similarity: {s[1]}, Address: {get_address(room)}\n'
                    records.write(line)
