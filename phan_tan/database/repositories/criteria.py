from ._base import CRUD
from phan_tan.database.models import Criteria


class CriteriaRepository(CRUD):
    def __init__(self, session):
        self.session = session
        self.model = Criteria
