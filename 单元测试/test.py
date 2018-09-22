# -*- coding:utf-8 -*-
import logging as log

log.basicConfig(level=log.DEBUG)
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='jkbigdata:9092')
producer.send('test', '11111')
producer.flush()
producer.close()
