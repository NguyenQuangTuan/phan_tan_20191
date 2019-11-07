from datetime import datetime
from sqlalchemy import Column, TIMESTAMP


class DateTimestamp():
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.utcnow,
                        default=datetime.utcnow)
