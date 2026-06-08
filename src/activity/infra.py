from src.activity.model import Activity


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
