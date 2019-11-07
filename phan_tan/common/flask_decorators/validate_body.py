from flask_restful import request
from functools import wraps


def validate_body(validate_schema, many=False):
    def is_form(content_type):
        return (
            'application/x-www-form-urlencoded' in content_type
            or 'multipart/form-data' in content_type
        )

    def validate_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            content_type = request.headers.get('Content-Type', '')

            if is_form(content_type):
                data = validate_schema().load(request.form)
                args[0].body = data
            else:
                json_data = request.get_json(force=True)
                data = validate_schema(many=many).load(json_data)
                args[0].body = data

            return func(*args, **kwargs)

        return func_wrapper

    return validate_decorator
