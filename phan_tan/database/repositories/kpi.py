from ._base import CRUD
from phan_tan.database.models import KPI


class KPIRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = KPI

    def get_one(self, **kwargs):
        query = self.session.query(self.model)

        if 'department_id' in kwargs:
            query = query.filter(
                self.model.department_id == kwargs['department_id']
            )

        if 'employee_id' in kwargs:
            query = query.filter(
                self.model.employee_id == kwargs['employee_id']
            )

        if 'project_id' in kwargs:
            query = query.filter(
                self.model.employee_id == kwargs['project_id']
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

        return query.first()
