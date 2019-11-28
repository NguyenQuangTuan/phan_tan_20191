from marshmallow import EXCLUDE, fields
from marshmallow.validate import Range, OneOf
from phan_tan.common.validator import USchema

list_type = ['DEPARTMENT', 'EMPLOYEE', 'PROJECT']


class IndexKPIResultRequest(USchema):
    class Meta:
        unknown = EXCLUDE

    limit = fields.Integer(validate=Range(min=1))
    offset = fields.Integer(validate=Range(min=0))
    department_id = fields.Int()
    employee_id = fields.Str()
    project_id = fields.Str()
    start_time = fields.Str()
    end_time = fields.Str()


class Criteria(USchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True)
    ratio = fields.Float(required=True)
    complete_rating = fields.Float(required=True)
    note = fields.Str(required=True, allow_none=True)


class CreateKPIResultRequest(USchema):
    class Meta:
        unknown = EXCLUDE

    criterias = fields.List(
        fields.Nested(Criteria, required=True),
        required=True
    )
    department_id = fields.Int(required=True, allow_none=True)
    employee_id = fields.Str(required=True, allow_none=True)
    project_id = fields.Str(required=True, allow_none=True)


class IndexAllKPIResultRequest(USchema):
    class Meta:
        unknown = EXCLUDE

    type = fields.Str(validate=OneOf(list_type))
    start_time = fields.Str()
    end_time = fields.Str()
