from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from src.habit.model import Habit, UnitType, OperationType, RangeType
from src.helpers import exit_keys

console = Console()


def get_habit_mapping(session, active_only=True):
    habits = session.query(Habit)
    if active_only:
        habits = habits.filter(Habit.is_active == True)

    habits = habits.all()
    return {i: habit for i, habit in enumerate(habits, 1)}


def view_habits(session, active_only=True):
    habit_map = get_habit_mapping(session, active_only)

    for habit in habit_map.values():
        output = f"{habit.name}: "
        if habit.target_operation_type and habit.target_range and habit.target_units:
            output += f"{habit.target_operation_type.value.replace('_', ' ')} {habit.target_units} {habit.target_unit_type.value if habit.target_unit_type else ''} {habit.target_range.value if habit.target_range else ''}"
        print(f"{output} (created on {habit.created_at.strftime('%Y-%m-%d')})")


def create_habit(
    session,
    name,
    target_units=None,
    target_unit_type=None,
    target_operation_type=None,
    target_range=None,
):
    habit = Habit(
        name=name.strip().upper(),
        target_units=target_units,
        target_unit_type=UnitType(target_unit_type) if target_unit_type else None,
        target_operation_type=(
            OperationType(target_operation_type) if target_operation_type else None
        ),
        target_range=RangeType(target_range) if target_range else None,
    )
    session.add(habit)
    session.commit()
    return habit


def deactivate_habit(session, habit_name):
    habit = session.query(Habit).filter(Habit.name == habit_name).first()
    if not habit:
        print(f"No habit found with name {habit_name}.")
        return None
    habit.is_active = False
    session.commit()
    return habit


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


def _enum_table(title, enum_class):
    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    table.add_column("#", justify="right")
    table.add_column(title)
    for i, option in enumerate(enum_class, 1):
        table.add_row(str(i), option.value)
    return table


def make_habit_creation_panel(session):
    habit_map = get_habit_mapping(session)

    habit_table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    habit_table.add_column("Name")
    habit_table.add_column("Target")
    for habit in habit_map.values():
        target = ""
        if habit.target_operation_type and habit.target_range and habit.target_units:
            unit = habit.target_unit_type.value if habit.target_unit_type else ""
            target = f"{habit.target_operation_type.value.replace('_', ' ')} {habit.target_units} {unit} {habit.target_range.value}"
        habit_table.add_row(habit.name, target)

    return Panel(
        Columns(
            [
                habit_table,
                _enum_table("Unit Type", UnitType),
                _enum_table("Operation Type", OperationType),
                _enum_table("Range", RangeType),
            ]
        ),
        title="Habits",
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
