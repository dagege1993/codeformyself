# coding: utf8

from datetime import datetime

from tasks import supplier_statics
from tasks.utils.database import databases

db = databases('scripture')

models = (
    supplier_statics.Bonotel(db),
    supplier_statics.HotelBeds(db),
    supplier_statics.HotelsPro(db)
)

for model in models:
    for hotel in model.table('hotels').find():
        print(hotel.get('images'))
        has = list(
            filter(
                lambda img: 'weegotr.com' in img,
                hotel.get('images', [])
            )
        )
        if 'cdn_images' in hotel:
            continue
        model.save_images(None, hotel)
        doc = {'cdn_images': hotel.get('images', [])}
        uresult = model.table('hotels').update_one(
            {'code': hotel['code']},
            {
                '$set': model.ensure_serializable(doc),
                '$setOnInsert': {'created_at': datetime.now()},
                '$currentDate': {'last_modified': True}
            }
        )
        model.pprint(uresult)
