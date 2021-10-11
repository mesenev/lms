import os


def cats_sid():
    return os.getenv('cats_sid')


def cats_sid_setter(value):
    os.environ["cats_sid"] = value
