from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import DepartmentRepository


class Departments(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.department_repo = DepartmentRepository(self.session)

    def get(self):
        departments = self.department_repo.find()

        return {
            'departments': to_dict(departments)
        }
