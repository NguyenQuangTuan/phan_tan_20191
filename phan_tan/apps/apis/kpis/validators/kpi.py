from marshmallow import EXCLUDE, fields
from marshmallow.validate import Range
from phan_tan.common.validator import USchema


class IndexKPIRequest(USchema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Integer(validate=Range(min=1))
    offset = fields.Integer(validate=Range(min=0))
    department_id = fields.Int()
    employee_id = fields.Int()
    project_id = fields.Int()
    start_time = fields.Str()
    end_time = fields.Str()
