from rich.console import Console

from src.habit.infra import get_habit_mapping, create_habit, deactivate_habit
from src.habit.model import UnitType, OperationType, RangeType
from src.habit.view import make_habit_creation_panel
from src.helpers import exit_keys
from src.view_helpers import format_habit_target

console = Console()


def view_habits(session, active_only=True):
    habit_map = get_habit_mapping(session, active_only)

    for habit in habit_map.values():
        output = f"{habit.name}: {format_habit_target(habit)}"
        print(f"{output} (created on {habit.created_at.strftime('%Y-%m-%d')})")


def _select_enum(prompt, enum_class):
    options = list(enum_class)
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  ({i}) {option.value}")
    print("Hit enter to skip")
    choice = input("Select a number: ").strip()
    if not choice or choice == "":
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1].value
    print(f"Invalid selection, skipping.")
    return None


def create_habit_input(session):
    name = input(
        f"Enter habit name (or {'/'.join(sorted(exit_keys))} to finish): "
    ).strip()
    if name.lower() in exit_keys:
        return "exit"
    if not name:
        print("Habit name cannot be empty.")
        return None

    target_units = input("Enter target units (optional): ").strip()
    target_unit_type = _select_enum("Select target unit type:", UnitType)
    target_operation_type = _select_enum("Select target operation type:", OperationType)
    target_range = _select_enum("Select target range:", RangeType)

    return create_habit(
        session,
        name,
        int(target_units) if target_units else None,
        target_unit_type,
        target_operation_type,
        target_range,
    )


def _select_enum_by_number(prompt_text, enum_class):
    options = list(enum_class)
    choice = input(prompt_text).strip()
    if choice.lower() in exit_keys:
        return "exit"
    if choice == "":
        return None
    try:
        return options[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection, skipping.")
        return None


def create_habits_bulk_input(session):
    print("Let's create some habits! Enter 'quit' or 'exit' at any time to save and exit.")

    while True:
        console.clear()
        console.print(make_habit_creation_panel(session))

        name = input("Enter habit name (or 'quit'/'exit' to finish): ").strip()
        if name.lower() in exit_keys:
            return
        if not name:
            print("Habit name cannot be empty.")
            continue

        target_units = input("Enter target units (optional): ").strip()
        if target_units.lower() in exit_keys:
            return

        target_unit_type = _select_enum_by_number(
            "Enter target unit type number, click 'Enter' to skip: ", UnitType
        )
        if target_unit_type == "exit":
            return

        target_operation_type = _select_enum_by_number(
            "Enter target operation type number, click 'Enter' to skip: ", OperationType
        )
        if target_operation_type == "exit":
            return

        target_range = _select_enum_by_number(
            "Enter target range number, click 'Enter' to skip: ", RangeType
        )
        if target_range == "exit":
            return

        try:
            create_habit(
                session,
                name,
                int(target_units) if target_units else None,
                target_unit_type.value if target_unit_type else None,
                target_operation_type.value if target_operation_type else None,
                target_range.value if target_range else None,
            )
        except Exception as e:
            print(f"Error creating new habit: {str(e)}")
            session.rollback()
