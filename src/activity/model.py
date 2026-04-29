from app import db
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, Date, String


class Activity(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    units = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    habit_id = Column(ForeignKey("habit.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
