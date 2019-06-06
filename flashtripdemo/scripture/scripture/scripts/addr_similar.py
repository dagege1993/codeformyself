#!python
# coding: utf8

import os
from pymongo import MongoClient
from gensim import corpora, models, similarities
from scripture import settings

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

m = MongoClient('mongodb://127.0.0.1:27017')
mc = MongoClient(settings.MONGO)
db = m.scripture.rxml_onlines


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


class Corpus:
    def __init__(self, dic):
        self.dic = dic

    def __iter__(self):
        for addr in get_address():
            yield self.dic.doc2bow(addr)


def addr_vec(dic, addr):
    return dic.doc2bow(
        (x.strip() for x in filter(
            lambda x: x != '',
            (a.strip() for a in addr.title().split(','))
        ))
    )


class Index:
    def loads(self):
        if os.path.isfile('address.dic'):
            self.dic = corpora.Dictionary.load('address.dic')
        else:
            self.dic = corpora.Dictionary(get_address())
            self.dic.save('address.dic')

        if os.path.isfile('address.mm'):
            self.corpus = corpora.MmCorpus('address.mm')
        else:
            self.corpus = Corpus(self.dic)
            corpora.MmCorpus.serialize('address.mm', self.corpus)

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
                lambda item: [roomsxml(item[0]), item[1] * 100],
                em[:10]
            )
        )


def roomsxml(idx):
    return db.find()[idx]['hotel_id']

idx = Index()
idx.loads()
idx.creat_index()

# query = {'loc': 1, 'jset_id': 1, 'geocode.geometry.formatted_address': 1}
for jset in mc.scripture.jsets.find({}, {'origin_body': False}):
    if 'how_to_get_there' not in jset:
        print(jset)
    addr = ','.join(jset['how_to_get_there'])
    city = jset['name'].split('(')[-1].split(',')[0].strip()
    if not addr:
        try:
            addr = jset['geocode']['geometry']['formatted_address']
        except:
            print(jset)
            continue
    inst = m.scripture.jset_similarities.insert_one({
        'jset_id': jset['jset_id'],
        'city': city,
        'similarity': list(idx.top10(addr))
    })
    print(inst.inserted_id)
