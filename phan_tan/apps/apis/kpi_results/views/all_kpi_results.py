import datetime
import pytz
from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict, clean_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import KPIResultRepository
from phan_tan.common.flask_decorators import (
    validate_params
)
from phan_tan.common.errors import UUnprocessableEntity
from ..validators.kpi import IndexAllKPIResultRequest


class AllKPIResults(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.kpi_result_repo = KPIResultRepository(self.session)

    @validate_params(IndexAllKPIResultRequest)
    def get(self):
        query = self.query
        start_time, end_time = self._validate_time(query)
        type = query.get('type', None)

        conditions = clean_dict({
            'start_time': start_time,
            'end_time': end_time
        })
        total, kpi_results = self.kpi_result_repo.get_all(type, **conditions)

        return {
            'total': total,
            'kpi_results': to_dict(kpi_results)
        }

    @staticmethod
    def _validate_time(query):
        start_time = query.get('start_time', None)
        end_time = query.get('end_time', None)
        try:
            # 2019-10-02 00:00:00
            if start_time:
                start_time = datetime.datetime.strptime(
                    start_time, '%Y-%m-%d %H:%M:%S').astimezone(pytz.utc)
            if end_time:
                end_time = datetime.datetime.strptime(
                    end_time, '%Y-%m-%d %H:%M:%S').astimezone(pytz.utc)
            return start_time, end_time
        except Exception:
            raise UUnprocessableEntity('Time invalid')
