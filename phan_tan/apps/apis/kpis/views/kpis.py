from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict, clean_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import KPIRepository
from phan_tan.common.flask_decorators import (
    validate_params
)
from ..validators.kpi import IndexKPIRequest


class KPIs(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.kpi_repo = KPIRepository(self.session)

    @validate_params(IndexKPIRequest)
    def get(self):
        query = self.query
        conditions = clean_dict({
            'limit': query.get('limit'),
            'offset': query.get('offset'),
            'department_id': query.get('department_id'),
            'employee_id': query.get('employee_id'),
            'start_time': query.get('start_time'),
            'end_time': query.get('end_time'),
        })
        kpis = self.kpi_repo.index(**conditions)

        return {
            'kpis': to_dict(kpis)
        }
