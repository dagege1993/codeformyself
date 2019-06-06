# coding: utf8

import logging

from gensim import corpora, models, similarities

from scripture.models.corpus import Corpus


class Similarity:
    __cached_by_city__ = {}

    logger = logging.getLogger(__name__)

    def __init__(self, dic=None, corpus=None):
        pass

    def set_dict(self, dic):
        self.dict = dic

    def save_dict(self, filename):
        pass

    def set_corpus(self, corpus):
        self.corpus = corpus

    def save_corpus(self):
        pass

    def set_city(self, city):
        self.city = city

    @classmethod
    def load(cls, city, corpus=None, mongoclient=None, city_id=None):
        if city in cls.__cached_by_city__:
            return cls.__cached_by_city__[city]

        similarity = cls()

        similarity.set_dict(
            corpora.Dictionary(Corpus.names(city, mongoclient, city_id))
        )

        if not corpus:
            corpus = Corpus(similarity.dict, city, mongoclient, city_id)

        similarity.set_corpus(corpus)

        similarity.set_city(city)

        similarity.create_index()

        cls.__cached_by_city__[city] = similarity

        return similarity

    def create_index(self):
        self.tfidf = models.TfidfModel(self.corpus)

        self.index = similarities.SparseMatrixSimilarity(
            self.tfidf[self.corpus], num_features=200000
        )

    def top_n(self,
              string,
              n=10,
              *,
              lte=None,
              gte=None,
              lt=None,
              gt=None,
              eq=None):
        vec = self.corpus.to_vec(string)
        tfidf_vec = self.tfidf[vec]
        sims = self.index[tfidf_vec]
        em = sorted(enumerate(sims), key=lambda i: -i[1])[:n]
        return map(
            lambda i: [self.corpus.to_id(i[0]), i[1] * 100],
            filter(
                self.filter(lte=lte, gte=gte, lt=lt, gt=gt),
                em
            )
        )

    def top_10(self, string, **kwargs):
        return self.top_n(string, n=10, **kwargs)

    def filter(self, *, lte=None, gte=None, lt=None, gt=None, eq=None):
        if lte is not None:
            return lambda x: x[1] <= lte / 100
        if gte is not None:
            return lambda x: x[1] >= gte / 100
        if lt is not None:
            return lambda x: x[1] < lt / 100
        if gt is not None:
            return lambda x: x[1] > gt / 100
        if eq is not None:
            return lambda x: x[1] == gt / 100

        return lambda x: True if x else None
