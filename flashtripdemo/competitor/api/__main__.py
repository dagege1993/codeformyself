# coding: utf-8

import logging.config

from api.types.application import Application
from api.competitor.routers import routers
from api.settings import LOG_CONFIG


def run():
    app = Application(routers)
    logging.config.dictConfig(LOG_CONFIG)
    app.start_server()


if __name__ == "__main__":
    run()
