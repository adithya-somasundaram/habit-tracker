from rich.columns import Columns
from rich.panel import Panel

from src.habit.infra import get_habit_mapping
from src.habit.model import UnitType, OperationType, RangeType
from src.view_helpers import format_habit_target, make_table


def _enum_table(title, enum_class):
    table = make_table(("#", {"justify": "right"}), title)
    for i, option in enumerate(enum_class, 1):
        table.add_row(str(i), option.value)
    return table


def make_habit_creation_panel(session):
    habit_map = get_habit_mapping(session)

    habit_table = make_table("Name", "Target")
    for habit in habit_map.values():
        habit_table.add_row(habit.name, format_habit_target(habit))

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
