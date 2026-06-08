from datetime import datetime

from rich.console import Console

from src.activity.infra import create_activity
from src.activity.view import make_activity_bulk_panel
from src.helpers import exit_keys, pacific_timezone

console = Console()


def create_activity_input(session):
    from src.habit.infra import get_habit_mapping

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


def bulk_create_activities(session):
    from src.habit.infra import get_habit_mapping

    print(
        "Let's log some activities! Enter 'quit' or 'exit' at any time to save and exit."
    )

    date_str = input(
        "Enter activity date (YYYY-MM-DD) - Enter to set to today: "
    ).strip()
    if date_str.lower() in exit_keys:
        return
    if not date_str:
        on_date = datetime.now(pacific_timezone).date()
    else:
        try:
            on_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    active_habit_map = get_habit_mapping(session, active_only=True)

    for habit in active_habit_map.values():
        console.clear()
        console.print(make_activity_bulk_panel(session, on_date))

        units_str = input(f"Enter units for {habit.name} (Enter for 0): ").strip()
        if units_str.lower() in exit_keys:
            return

        units = int(units_str) if units_str.isdigit() else 0
        if units == 0 and not habit.target_unit_type:
            continue

        try:
            create_activity(session, on_date, habit.id, units)
        except Exception as e:
            print(f"Error creating activity for {habit.name}: {str(e)}")
            session.rollback()

    console.clear()
    console.print(make_activity_bulk_panel(session, on_date))
    print("Done logging activities for", on_date.strftime("%Y-%m-%d"))
