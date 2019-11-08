from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import CriteriaRepository


class Criterias(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.criteria_repo = CriteriaRepository(self.session)

    def get(self):
        criterias = self.criteria_repo.find()

        return {
            'criterias': to_dict(criterias)
        }
