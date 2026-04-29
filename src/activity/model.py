from app import db
import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, Index, text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String, Date


class Activity(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    units = Column(Integer, nullable=True)
    habit_id = Column(ForeignKey("habit.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
