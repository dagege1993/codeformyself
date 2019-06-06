# coding: utf-8

# Standard Library
import random
import string

_choices = random.choices
_letters = string.ascii_letters + string.digits
_join = "".join


def generate(length=8):
    return _join(_choices(_letters, k=length))


def short():
    return generate()


def long():
    return generate(24)
