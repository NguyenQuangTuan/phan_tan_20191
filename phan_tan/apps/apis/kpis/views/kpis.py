from database_new import session_scope
from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict, clean_dict
from phan_tan.common.api import UResource
from phan_tan.database.models import KPIType
from phan_tan.database.repositories import KPIRepository
from phan_tan.common.flask_decorators import (
    validate_params, validate_body
)
from phan_tan.common.errors import UUnprocessableEntity, UNotFound
from ..validators.kpi import IndexKPIRequest, CreateKPIRequest


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
        period = query.get('period', 'YEAR')

        self._validate_id(employee_id, department_id, project_id)
        conditions = clean_dict({
            'department_id': department_id,
            'employee_id': employee_id,
            'project_id': project_id,
            'period': period
        })
        kpi = self.kpi_repo.get_one(**conditions)
        if not kpi:
            raise UNotFound('Kpi not found')

        return to_dict(kpi)

    @validate_body(CreateKPIRequest)
    def post(self):
        body = self.body
        employee_id = body.get('employee_id', None)
        department_id = body.get('department_id', None)
        project_id = body.get('project_id', None)
        criterias = body.get('criterias', None)
        period = body.get('period', 'YEAR')

        self._validate_id(employee_id, department_id, project_id)
        self._validate_criteria(criterias)
        type = self._get_kpi_type(employee_id, department_id, project_id)

        with session_scope(self.session):
            kpi_orm = self.kpi_repo.create(
                type=type,
                criterias=criterias,
                employee_id=employee_id,
                department_id=department_id,
                project_id=project_id,
                period=period
            )

            return to_dict(kpi_orm)

    @staticmethod
    def _validate_id(employee_id=None, department_id=None, project_id=None):
        if not any([k for k in [employee_id, department_id, project_id]]):
            raise UUnprocessableEntity(
                '''At least one of employee_id, department_id, project_id
                must be existed'''
            )

        if employee_id and not any([k for k in [department_id, project_id]]):
            raise UUnprocessableEntity(
                'department_id or project_id is required'
            )

    @staticmethod
    def _validate_criteria(criterias):
        total_ratio = sum([c['ratio'] for c in criterias])
        if round(total_ratio, 3) != 1:
            raise UUnprocessableEntity('Total ratio must be equal 1')
        for c in criterias:
            c['name'] = c['name'].strip()

    @staticmethod
    def _get_kpi_type(employee_id=None, department_id=None, project_id=None):
        type = None
        if employee_id:
            type = KPIType.EMPLOYEE.value
        if department_id:
            type = KPIType.DEPARTMENT.value
        if project_id:
            type = KPIType.PROJECT.value
        return type
