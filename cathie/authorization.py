import os


def cats_sid():
    return os.getenv('cats_sid', '-1')


def cats_sid_setter(value):
    os.environ["cats_sid"] = value
