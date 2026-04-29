from datetime import datetime

from src.activity.model import Activity
from src.helpers import pacific_timezone


def create_activity_input(session):
    from src.habit.services import get_habit_mapping

    date_str = input(
        "Enter activity date (YYYY-MM-DD) - Enter to set to today: "
    ).strip()
    if not date_str:
        date = datetime.now(pacific_timezone).date()
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    active_habit_map = get_habit_mapping(session, active_only=True)
    print("Select a habit:")
    for habit_id, habit in active_habit_map.items():
        print(f"  ({habit_id}) {habit.name}")
    habit_id_str = input().strip()
    if not habit_id_str.isdigit():
        print("Habit ID must be a number.")
        return None
    habit = active_habit_map.get(int(habit_id_str), None)
    if not habit:
        print("Invalid habit ID selected.")
        return
    habit_id = habit.id

    units_str = input("Enter units (optional - Enter to skip): ").strip()
    units = int(units_str) if units_str.isdigit() else None

    description = (
        input("Enter description (optional - Enter to skip): ").strip() or None
    )

    return create_activity(session, date, habit_id, units, description)


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
