from phan_tan import db
from phan_tan.common.helpers.dict_ultility import to_dict
from phan_tan.common.api import UResource
from phan_tan.database.repositories import DepartmentRepository


class Department(UResource):
    def __init__(self):
        self.session = db.session_factory
        self.department_repo = DepartmentRepository(self.session)

    def get(self, id):
        department = self.department_repo.first_or_fail(id=id)

        return {
            'department': to_dict(department)
        }
