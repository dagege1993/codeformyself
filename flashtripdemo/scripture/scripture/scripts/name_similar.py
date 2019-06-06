#!python
# coding: utf8

# import os
from pymongo import MongoClient
from gensim import corpora, models, similarities
from scripture import settings
from scripture.utils.jsetadditional import JsetAdditional

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

logger = logging.getLogger('similar.name')

m = MongoClient('mongodb://127.0.0.1:27017')
mc = MongoClient(settings.MONGO)
db = m.scripture.rxml_onlines

cities = {
    'Amsterdam': '17607',
    'Barcelona': '18350',
    'Berlin': '16534',
    'Boston': '19402',
    'Chicago': '19455',
    'Hong Kong': '16772',
    'Kyoto': '17246',
    'London': '52612',
    'Los Angeles': '19704',
    'Macau': '17366',
    'Melbourne': '15340',
    'Munich': '16609',
    'Osaka': '17286',
    'Paris': '16471',
    'Rome': '17149',
    'San Francisco': '19919',
    'Seattle': '19943',
    'Seoul': '18326',
    'Singapore': '18196',
    'Sydney': '15375',
    'Tokyo': '17303',
    'Washington D.C.': '20071',
    'Zurich': '18671'
}


def comb_address(hotel):
    _addr = []
    address = hotel['address']
    addr1 = address.get('address1', '')
    if addr1:
        _addr.extend([addr.title() for addr in addr1.split(',')])
    addr2 = address.get('address2', '')
    if addr2:
        _addr.extend([addr.title() for addr in addr2.split(',')])
    addr3 = address.get('address3', '')
    if addr3:
        _addr.extend([addr.title() for addr in addr3.split(',')])
    # city = address.get('city')
    # if city:
    #     _addr.append(city.title())
    # state = address.get('state')
    # if state:
    #     _addr.append(state.title())
    # country = address.get('country')
    # if country:
    #     _addr.append(country.title())
    return _addr


def get_address():
    for hotel in db.find():
        yield comb_address(hotel)


def get_names_by_city(city):
    city_id = cities[city]
    c = db.find({'region.city_id': city_id})
    logger.warn('Found %d hotels in %s', c.count(), city)
    for hotel in c:
        yield split(hotel['name'])


class Corpus:
    def __init__(self, dic, city):
        self.dic = dic
        self.city = city

    def __iter__(self):
        # for addr in get_address():
        for addr in get_names_by_city(self.city):
            yield self.dic.doc2bow(addr)


def split(s):
    return s.title().replace('.', '').replace('-', ' ').split(',')[0] \
        .split('(')[0].replace('&amp;', 'and').replace('&', 'and').split()


def addr_vec(dic, addr):
    return dic.doc2bow(
        (x.strip() for x in filter(
            lambda x: x != '',
            (a.strip() for a in split(addr))
        ))
    )


class Index:

    __by_cities__ = {}

    def set_dic(self, dic):
        self.dic = dic

    def save_dic(self, filename):
        self.dic.save(filename)

    def set_corpus(self, corpus):
        self.corpus = corpus

    @classmethod
    def loads(cls, city):
        if city in cls.__by_cities__:
            return cls.__by_cities__[city]

        idx = Index()
        # if os.path.isfile(city + 'name.dic'):
        #     idx.set_dic(corpora.Dictionary.load(city + 'name.dic'))
        # else:
        dic = corpora.Dictionary(get_names_by_city(city))
        # dic.filter_extremes(no_above=0.1)

        idx.set_dic(dic)
        #     idx.set_dic(corpora.Dictionary(get_names_by_city(city)))
        #     idx.save_dic(city + 'name.dic')

        # if os.path.isfile(city + 'name.mm'):
        #     idx.set_corpus(corpora.MmCorpus(city + 'name.mm'))
        # else:
        idx.set_corpus(Corpus(dic, city))
        #     idx.set_corpus(Corpus(idx.dic))
        #     corpora.MmCorpus.serialize(city + 'name.mm', idx.corpus)

        idx.city = city

        idx.creat_index()

        cls.__by_cities__[city] = idx
        return idx

    def creat_index(self):
        self.tfidf = models.TfidfModel(self.corpus)
        # self.lsi = models.LsiModel(
        #     self.tfidf[self.corpus], id2word=self.dic, num_topics=50
        # )
        self._index = similarities.SparseMatrixSimilarity(
            self.tfidf[self.corpus], num_features=200000
        )
        # self._index = similarities.MatrixSimilarity(
        #     self.lsi[self.tfidf[self.corpus]]
        # )

    def top10(self, addr):
        vec = addr_vec(self.dic, addr)
        tfidf_vec = self.tfidf[vec]
        # sims = self._index[self.lsi[tfidf_vec]]
        sims = self._index[tfidf_vec]
        em = sorted(enumerate(sims), key=lambda item: -item[1])
        return filter(
            lambda x: x[1] != 0,
            map(
                lambda item: [roomsxml(item[0], self.city), item[1] * 100],
                em[:10]
            )
        )


def roomsxml(idx, city=None):
    if city:
        q = {'region.city_id': cities[city]}
    else:
        q = {}
    return db.find(q)[idx]['hotel_id']

# query = {'loc': 1, 'jset_id': 1, 'geocode.geometry.formatted_address': 1}
for jset in mc.scripture.jsets.find({}):
    try:
        addition = JsetAdditional(jset['origin_body'])
    except:
        logger.error('Body is empty %s!', jset['jset_id'])
        continue
    city = addition.city().split(',')[0].strip().title()
    if city.startswith('Washington'):
        city = 'Washington D.C.'
    if city not in cities:
        continue
    # if not addr:
    #     try:
    #         addr = jset['geocode']['geometry']['formatted_address']
    #     except:
    #         print(jset)
    #         continue
    if 'how_to_get_there' in jset:
        name = jset['how_to_get_there'][0]
    else:
        name = jset['name'].split('(')[0].split('|')[0]

    inst = m.scripture.jset_name_similarities2.insert_one({
        'jset_id': jset['jset_id'],
        'name': name,
        'city': city,
        'similarity': list(Index.loads(city).top10(name))
    })
    logger.debug(inst.inserted_id)
