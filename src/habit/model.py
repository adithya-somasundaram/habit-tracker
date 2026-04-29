from app import db
import enum
from datetime import datetime

from sqlalchemy import Enum, Index, text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String


class UnitType(enum.Enum):
    ML = "ml"
    MINUTES = "minutes"
    HOURS = "hours"
    REPS = "reps"
    MILES = "miles"
    KILOMETERS = "kilometers"
    PAGES = "pages"
    GRAMS = "grams"


class OperationType(enum.Enum):
    GREATER_THAN = "greater_than"  # exists
    LESS_THAN = "less_than"
    EQUAL_TO = "equal_to"
    GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"  # exists
    LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"


class RangeType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Habit(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    target_units = Column(Integer, nullable=True, default=1)
    target_unit_type = Column(Enum(UnitType), nullable=True)
    target_operation_type = Column(Enum(OperationType), nullable=True)
    target_range = Column(Enum(RangeType), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    __table_args__ = (
        # Unique only when is_active = 1 (i.e., true)
        Index(
            "uq_active_account_name",
            "name",
            unique=True,
            sqlite_where=text("is_active = 1"),
        ),
    )
