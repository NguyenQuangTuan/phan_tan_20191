from sqlalchemy import Column, String, Integer, JSON

from .base import DeclarativeBase, Base
from .common.date_timestamp import DateTimestamp


class KPI(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'kpis'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    criterias = Column(JSON, nullable=False, default='[]')
    department_id = Column(String, nullable=True)
    employee_id = Column(String, nullable=True)
