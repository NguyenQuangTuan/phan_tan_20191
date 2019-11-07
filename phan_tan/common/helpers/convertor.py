import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj.__class__, DeclarativeMeta):
            return json.JSONEncoder.default(self, obj)

        # an SQLAlchemy class
        fields = {}
        obj_data = [x for x in dir(obj)
                    if not x.startswith('_') and x != 'metadata']
        for field in obj_data:
            data = obj.__getattribute__(field)
            try:
                # this will fail on non-encodable values, like other classes
                json.dumps(data)
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields
