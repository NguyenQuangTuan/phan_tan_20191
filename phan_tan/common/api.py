from flask_restful import Api, Resource
from flask import request as flask_request
import datetime


class UApi(Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def convert_time_int_to_string(self, timestamp: int):
        return datetime.datetime.utcfromtimestamp(timestamp).replace(
            tzinfo=datetime.timezone.utc
        ).isoformat()

    def get_list_from_params(self, params, keyword):
        new_keyword = '{}[]'.format(keyword)
        if new_keyword not in params:
            return []
        return flask_request.args.getlist(keyword)
