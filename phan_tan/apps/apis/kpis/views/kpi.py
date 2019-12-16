from database_new import session_scope
from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import KPIRepository
from phan_tan.common.flask_decorators import validate_body
from phan_tan.common.errors import UUnprocessableEntity
from ..validators.kpi import UpdateKPIRequest


class KPI(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.kpi_repo = KPIRepository(self.session)

    @validate_body(UpdateKPIRequest)
    def put(self, id):
        body = self.body
        criterias = body.get('criterias', [])
        self._validate_criteria(criterias)
        kpi_orm = self.kpi_repo.first_or_fail(id=id)

        with session_scope(self.session):
            kpi_orm = self.kpi_repo.update(
                kpi_orm,
                criterias=criterias
            )

            return to_dict(kpi_orm)

    @staticmethod
    def _validate_criteria(criterias):
        total_ratio = sum([c['ratio'] for c in criterias])
        if round(total_ratio, 3) != 1:
            raise UUnprocessableEntity('Total ratio must be equal 1')

        for c in criterias:
            c['name'] = c['name'].strip()
