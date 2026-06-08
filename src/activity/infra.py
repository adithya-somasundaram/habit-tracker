import calendar
from datetime import timedelta

from sqlalchemy import func

from src.activity.model import Activity
from src.habit.model import RangeType


def get_period_bounds(on_date, range_type):
    if range_type == RangeType.WEEKLY:
        start = on_date - timedelta(days=on_date.weekday())
        end = start + timedelta(days=6)
    elif range_type == RangeType.MONTHLY:
        start = on_date.replace(day=1)
        end = on_date.replace(day=calendar.monthrange(on_date.year, on_date.month)[1])
    elif range_type == RangeType.YEARLY:
        start = on_date.replace(month=1, day=1)
        end = on_date.replace(month=12, day=31)
    else:
        start = end = on_date

    return start, end


def get_period_progress(session, habit, on_date):
    if not habit.target_range:
        return None, None, None

    start, end = get_period_bounds(on_date, habit.target_range)

    query = session.query(Activity).filter(
        Activity.habit_id == habit.id,
        Activity.date >= start,
        Activity.date <= end,
    )

    if habit.target_unit_type:
        total = query.with_entities(func.coalesce(func.sum(Activity.units), 0)).scalar()
    else:
        total = query.count()

    return total, start, end


def create_activity(session, date, habit_id, units=None, description=None):
    activity = Activity(
        date=date,
        habit_id=habit_id,
        units=units,
        description=description,
    )
    session.add(activity)
    session.commit()
    return activity
