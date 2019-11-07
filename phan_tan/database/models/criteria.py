from sqlalchemy import Column, Integer, JSON

from .base import DeclarativeBase, Base
from .common.date_timestamp import DateTimestamp


class Criteria(DeclarativeBase, Base, DateTimestamp):
    __tablename__ = 'criterias'

    id = Column(Integer, primary_key=True)
    criterias = Column(JSON, nullable=False, default='[]')
