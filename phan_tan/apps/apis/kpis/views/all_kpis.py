from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import KPIRepository
from phan_tan.common.flask_decorators import (
    validate_params
)
from ..validators.kpi import IndexAllKPIRequest


class AllKPIs(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.kpi_repo = KPIRepository(self.session)

    @validate_params(IndexAllKPIRequest)
    def get(self):
        query = self.query
        type = query.get('type', None)

        kpis = self.kpi_repo.find(type=type)

        return {
            'kpis': to_dict(kpis)
        }
