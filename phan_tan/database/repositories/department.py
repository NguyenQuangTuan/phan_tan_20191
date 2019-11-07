from ._base import CRUD
from phan_tan.database.models import Department


class DepartmentRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = Department
