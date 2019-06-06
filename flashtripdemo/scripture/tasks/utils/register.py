# coding: utf8

import importlib


def register(name):
    importlib.import_module(name)
