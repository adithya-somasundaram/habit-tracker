from rich.panel import Panel

from src.activity.infra import get_period_progress
from src.habit.infra import get_habit_mapping
from src.view_helpers import format_habit_target, make_table


def make_activity_bulk_panel(session, on_date):
    habit_map = get_habit_mapping(session, active_only=True)

    table = make_table(
        "Habit", "Target", (f"This {on_date.strftime('%Y-%m-%d')}'s period", {"justify": "right"})
    )

    for habit in habit_map.values():
        progress, start, end = get_period_progress(session, habit, on_date)
        progress_str = ""
        if progress is not None:
            unit = habit.target_unit_type.value if habit.target_unit_type else "times"
            progress_str = f"{progress} {unit} ({start.strftime('%m/%d')}-{end.strftime('%m/%d')})"

        table.add_row(habit.name, format_habit_target(habit), progress_str)

    return Panel(table, title=f"Log activities for {on_date.strftime('%Y-%m-%d')}")
