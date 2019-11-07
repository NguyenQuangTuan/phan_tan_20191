import re
from functools import wraps
from flask_restful import request
from flask import request as flask_request


class ParamTypeError(Exception):
    pass


def params_handler(pick=None, keyword_mapping=None, strict_type_mapping=None):
    pick = pick or []
    keyword_mapping = keyword_mapping or []
    strict_type_mapping = strict_type_mapping or {}

    def validate_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            params = request.args.to_dict()
            param_keys = list(params.keys())
            nested_regex = re.compile(r'\w+(\[\w+\])+')
            for key in param_keys:
                if key[-2:] == '[]':
                    params[key[:-2]] = flask_request.args.getlist(key)
                    del params[key]
                    continue
                if nested_regex.match(key):
                    value = params.pop(key, None)
                    params = merge_nested_params(params, key, value)
                    continue

            args[0].query = build_params_dict(
                params, pick, keyword_mapping, strict_type_mapping)

            return func(*args, **kwargs)

        return func_wrapper

    return validate_decorator


def parse_nested_params(key, value):
    '''
    key will have format a[b][c][d]
    '''
    elements = key.split('[')
    number_elements = len(elements)

    nested_param = {}
    nested_keys = []
    handling_params = nested_param
    for index, element in enumerate(elements):
        if element[-1] == ']':
            element = element[:-1]
        nested_keys.append(element)
        if index == number_elements - 1:
            handling_params[element] = value
            continue
        nested_param[element] = handling_params = {}

    return nested_keys, nested_param


def merge_nested_params(params, key, value):
    '''
    key will have format a[b][c][d]
    '''
    nested_keys, nested_param = parse_nested_params(key, value)

    handling_params = params
    handling_nested = nested_param
    for nested_key in nested_keys:
        handling_nested = handling_nested[nested_key]
        if nested_key not in handling_params:
            handling_params[nested_key] = handling_nested
            break
        handling_params = handling_params[nested_key]
        if not isinstance(handling_params, dict):
            break

    return params


def build_params_dict(
        param_dict,
        pick=None,
        keyword_mapping=None,
        strict_type_mapping=None):
    pick = pick or []
    keyword_mapping = keyword_mapping or []
    strict_type_mapping = strict_type_mapping or {}

    picked_params = _pick_param(param_dict, pick)

    pagination = _handle_pagination(
        param_dict.get('limit', 10), param_dict.get('offset', 0))

    order_by = _handle_order_by(
        param_dict.get('sort_by', 'id'), param_dict.get('sort_type', 'desc'))
    conditions = _handle_conditions(
        picked_params, keyword_mapping, strict_type_mapping)

    param = {
        **pagination,
        **order_by,
        **conditions
    }

    select = param_dict.get('select', None)
    if isinstance(select, str) and select.strip():
        param['select'] = select.split(',')

    return param


def _pick_param(param_dict, pick):
    if len(pick) == 0:
        return param_dict

    return {
        key: value for key, value in param_dict.items() if key in pick
    }


def _handle_pagination(limit, offset, default_limit=10, default_offset=0):
    try:
        limit = int(limit)
        offset = int(offset)

        return {
            'pagination': {
                'limit': limit if limit > 0 else default_limit,
                'offset': offset if offset > 0 else default_offset
            }
        }
    except Exception:
        return {
            'pagination': {
                'limit': default_limit,
                'offset': default_offset
            }
        }


def _handle_order_by(
        sort_by, sort_type, default_sort_by='id', default_sort_type='asc'):
    valid_sort_by = isinstance(sort_by, str) and sort_by.strip()
    valid_sort_type = (
        isinstance(sort_type, str)
        and str.lower(sort_type) in ['desc', 'asc']
    )

    return {
        'order_by': [
            sort_by if valid_sort_by else default_sort_by,
            str.lower(sort_type) if valid_sort_type else default_sort_type
        ]
    }


def _to_bool(v):
    return str(v).lower() in ('yes', 'true', 't', '1')


def _handle_parser_type(key, value, parser_types):
    try:
        parser_type = parser_types.get(key, None)
        if parser_type is None:
            return value

        if isinstance(parser_type(), bool):
            return _to_bool(value)

        if isinstance(value, list):
            return list(map(lambda x: parser_type(x), value))

        return parser_type(value)
    except Exception:
        raise ParamTypeError


def _handle_conditions(param_dict, keyword_mapping, strict_type_mapping):
    conditions = {}
    keywords = {}

    def _dispatch(key, value):
        converted_value = _handle_parser_type(key, value, strict_type_mapping)
        if key in keyword_mapping:
            keywords[key] = converted_value
        else:
            conditions[key] = converted_value

    param_type = ['limit', 'offset', 'sort_by', 'sort_type', 'select']

    _ = {
        _dispatch(key, value) for key, value in param_dict.items()
        if key not in param_type
    }

    return {
        'conditions': conditions,
        'keywords': keywords
    }
