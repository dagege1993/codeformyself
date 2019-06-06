from bson import ObjectId
from pysolr import Solr
from web import settings
from web.api.webhooks import solr

fake_hotel = [
    {
        'id': '59e74dd46fdf1e7a80a78f69',
        'name': 'test_fake_hotel',
        'name_cn': '测试solr用例',
        'supplier': 'hotelbeds',
        'address': 'beijing_shanghai ',
        'wgstar': 3,
        'wg_country_id': '5abdbff7fc0e264f9bb1d38e',
        'wg_province_id': '5acc8264ca92bfc8efb33352',
        'wg_destination_id': ObjectId('5acf1324d8705559c9bf0eea')
    }
]


def solr_search(query):
    solr = Solr(
        "/".join([settings.SOLR.rstrip("/"), "solr", "hotels"])
    )
    return solr.search(query)


def test_solr():
    before_add = len(solr_search(query='test_fake_hotel'))
    assert before_add == 0
    solr._solr_add(fake_hotel, "hotels")
    after_add = len(solr_search(query='test_fake_hotel'))
    assert after_add == 1
    solr._solr_del("hotels", ['59e74dd46fdf1e7a80a78f69', ])
    after_del = len(solr_search(query='test_fake_hotel'))
    assert after_del == 0
