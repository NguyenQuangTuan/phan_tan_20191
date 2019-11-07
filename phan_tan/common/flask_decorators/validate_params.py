import re
import pandas as pd
from flask import request as flask_request
from flask_restful import request
from functools import wraps


def validate_params(validate_schema):
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
            data = validate_schema().load(params)
            args[0].query = data

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


def validate_spreadsheet(validate_schema):
    def validate_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            req_file = request.files['file']
            sheet = pd.read_excel(req_file.stream)
            cols = [col for col in sheet]
            data = [
                tuple(sheet[col][i] for col in cols)
                for i in sheet.index
            ]
            validate_schema().load({
                'number_of_columns': len(cols)
            })
            args[0].sheet_data = data

            return func(*args, **kwargs)

        return func_wrapper

    return validate_decorator
