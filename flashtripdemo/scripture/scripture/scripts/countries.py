# coding: utf8
"""Created by: songww
"""

import logging

from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient
from scripture import settings


def update(text):
    """Update cities
    """
    logger = logging.getLogger(__name__)
    scripture = MongoClient(settings.MONGO).scripture

    with open(text) as _file:
        line_count = upserted = 0
        for line in _file:
            line_count += 1
            (
                geo_name_id,
                name,
                ascii_name,
                alternate_names,
                latitude,
                longitude,
                feature_class,
                feature_code,
                country_code,
                cc2,
                admin_code_1,
                admin_code_2,
                admin_code_3,
                admin_code_4,
                population,
                elevation,
                dem,
                timezone_id,
                last_modified
            ) = line.split('\t')
            alternate_names = [an.strip() for an in alternate_names.split(',')]
            alternate_country_codes = [cc.strip() for cc in cc2.split(',')]
            last_modified = datetime.strptime(last_modified.strip(), '%Y-%m-%d')
            upsert = scripture.countries.update_one(
                {'geo_name_id': int(geo_name_id)},
                {
                    '$setOnInsert': {
                        'geo_name_id': int(geo_name_id),
                        'name': name.strip(),
                        'ascii_name': ascii_name.strip(),
                        'alternate_names': alternate_names,
                        'latitude': float(latitude),
                        'longitude': float(longitude),
                        'feature_class': feature_class.strip(),
                        'feature_code': feature_code.strip(),
                        'country_code': country_code.strip(),
                        'alternate_country_codes': alternate_country_codes,
                        'admin_code_1': admin_code_1.strip(),
                        'admin_code_2': admin_code_2.strip(),
                        'admin_code_3': admin_code_3.strip(),
                        'admin_code_4': admin_code_4.strip(),
                        'population': int(population.strip()),
                        'elevation': elevation.strip(),
                        'digital_elevation_model': dem.strip(),
                        'timezone': timezone_id.strip(),
                        'last_modified': last_modified
                    }
                },
                upsert=True
            )
            if hasattr(upsert, 'upserted_id') and \
                    isinstance(upsert.upserted_id, ObjectId):
                upserted += 1
    logger.info("Inserted %d", line_count)
