from enum import Enum
from sqlalchemy import Column, String, Integer, JSON
from .base import DeclarativeBase, Base
from .common.date_timestamp import DateTimestamp


class KPIResultType(Enum):
    DEPARTMENT = 'DEPARTMENT'
    EMPLOYEE = 'EMPLOYEE'
    PROJECT = 'PROJECT'


class KPIResult(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'kpi_results'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    criterias = Column(JSON, nullable=False, default='[]')
    department_id = Column(Integer, nullable=True)
    employee_id = Column(Integer, nullable=True)
    project_id = Column(Integer)
