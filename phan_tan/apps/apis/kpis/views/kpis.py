from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict, clean_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import KPIRepository
from phan_tan.common.flask_decorators import (
    validate_params
)
from phan_tan.common.errors import UUnprocessableEntity, UNotFound
from ..validators.kpi import IndexKPIRequest


class KPIs(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.kpi_repo = KPIRepository(self.session)

    @validate_params(IndexKPIRequest)
    def get(self):
        query = self.query
        employee_id = query.get('employee_id', None)
        department_id = query.get('department_id', None)
        project_id = query.get('project_id', None)

        if not any([k for k in [employee_id, department_id, project_id]]):
            raise UUnprocessableEntity(
                '''At least one of employee_id, department_id, project_id
                must be existed'''
            )

        if employee_id and not any([k for k in [department_id, project_id]]):
            raise UUnprocessableEntity(
                'department_id or project_id is required'
            )

        conditions = clean_dict({
            'department_id': department_id,
            'employee_id': employee_id,
            'project_id': project_id
        })
        kpi = self.kpi_repo.get_one(**conditions)
        if not kpi:
            raise UNotFound('Kpi not found')

        return to_dict(kpi)
