from enum import Enum


def deep_get(dictionary, keys, default=None):
    from functools import reduce
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split('.'), dictionary)


def clean_dict(obj):
    return {
        key: value for key, value in obj.items() if (
            value and value != ['']
        )
    }


def _handling_specific_type(value):
    from datetime import datetime, date

    if isinstance(value, datetime):
        datetime_str = value.isoformat()
        return datetime_str if value.tzinfo else f'{datetime_str}+00:00'

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, Enum):
        return value.value


def _isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def to_dict(obj):
    if(_isnamedtupleinstance(obj)):
        return to_dict(obj._asdict())

    if isinstance(obj, dict):
        data = {}
        for (key, value) in obj.items():
            data[key] = to_dict(value)
        return data

    if hasattr(obj, '_ast'):
        return to_dict(obj._ast())

    if hasattr(obj, '__iter__') and not isinstance(obj, str):
        return [to_dict(value) for value in obj]

    if hasattr(obj, '__dict__'):
        return dict([
            (key, to_dict(_handling_specific_type(value) or value))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')
        ])

    return _handling_specific_type(obj) or obj
