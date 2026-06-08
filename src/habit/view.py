from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from src.habit.infra import get_habit_mapping
from src.habit.model import UnitType, OperationType, RangeType


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
