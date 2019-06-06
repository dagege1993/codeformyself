# coding: utf8

from celery import Celery


class CeleryTask(object):
    def __init__(self, broker, backend):
        self.celery_task = Celery(broker=broker, backend=backend)

    def __call__(self, name, *args, **kwargs):
        return self.celery_task.send_task(name, *args, **kwargs)
