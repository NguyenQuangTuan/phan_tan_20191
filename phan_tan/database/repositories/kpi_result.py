from ._base import CRUD
from phan_tan.database.models import KPIResult, KPIType


class KPIResultRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = KPIResult

    def get_all(self, type, **kwargs):
        query = self.session.query(self.model)

        if type == KPIType.DEPARTMENT.value:
            query = query.filter(
                self.model.department_id.isnot(None)
            )

        if type == KPIType.EMPLOYEE.value:
            query = query.filter(
                self.model.employee_id.isnot(None)
            )

        if type == KPIType.PROJECT.value:
            query = query.filter(
                self.model.project_id.isnot(None)
            )

        if 'start_time' in kwargs:
            query = query.filter(
                self.model.created_at >= kwargs['start_time']
            )

        if 'end_time' in kwargs:
            query = query.filter(
                self.model.created_at <= kwargs['end_time']
            )

        query = query.order_by(self.model.id.desc())
        count = query.count()

        if 'limit' in kwargs:
            query = query.limit(kwargs['limit'])
        if 'offset' in kwargs:
            query = query.offset(kwargs['offset'])

        return count, query.all()

    def index(self, **kwargs):
        query = self.session.query(self.model)

        if 'department_id' in kwargs and 'employee_id' not in kwargs:
            query = query.filter(
                self.model.department_id == kwargs['department_id'],
                self.model.employee_id.is_(None)
            )

        if 'employee_id' in kwargs:
            query = query.filter(
                self.model.employee_id == kwargs['employee_id'])
            if 'department_id' in kwargs:
                query = query.filter(
                    self.model.department_id == kwargs['department_id'])
            if 'project_id' in kwargs:
                query = query.filter(
                    self.model.project_id == kwargs['project_id'])

        if 'project_id' in kwargs and 'employee_id' not in kwargs:
            query = query.filter(
                self.model.project_id == kwargs['project_id'],
                self.model.employee_id.is_(None)
            )

        if 'start_time' in kwargs:
            st = kwargs['start_time']
            query = query.filter(
                self.model.created_at >= st
            )

        if 'end_time' in kwargs:
            et = kwargs['end_time']
            query = query.filter(
                self.model.created_at <= et
            )

        query = query.order_by(self.model.id.desc())
        count = query.count()

        if 'limit' in kwargs:
            query = query.limit(kwargs['limit'])
        if 'offset' in kwargs:
            query = query.offset(kwargs['offset'])

        return count, query.all()
