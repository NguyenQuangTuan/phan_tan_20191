# flake8: noqa
from .dict_ultility import clean_dict, to_dict, deep_get


def empty_obj():
    import types
    return types.SimpleNamespace()
