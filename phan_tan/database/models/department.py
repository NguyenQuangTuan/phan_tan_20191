from sqlalchemy import Column, String, Integer, JSON

from .base import DeclarativeBase, Base
from .common.date_timestamp import DateTimestamp


class Department(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    department_name = Column(String, nullable=False)
    positions = Column(JSON, nullable=False, default='[]')
