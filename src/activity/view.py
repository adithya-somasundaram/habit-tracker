from rich.panel import Panel
from rich.table import Table

from src.activity.infra import get_period_progress
from src.habit.infra import get_habit_mapping


def make_activity_bulk_panel(session, on_date):
    habit_map = get_habit_mapping(session, active_only=True)

    table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
    table.add_column("Habit")
    table.add_column("Target")
    table.add_column(f"This {on_date.strftime('%Y-%m-%d')}'s period", justify="right")

    for habit in habit_map.values():
        target = ""
        if habit.target_operation_type and habit.target_range and habit.target_units:
            unit = habit.target_unit_type.value if habit.target_unit_type else ""
            target = f"{habit.target_operation_type.value.replace('_', ' ')} {habit.target_units} {unit} {habit.target_range.value}"

        progress, start, end = get_period_progress(session, habit, on_date)
        progress_str = ""
        if progress is not None:
            unit = habit.target_unit_type.value if habit.target_unit_type else "times"
            progress_str = f"{progress} {unit} ({start.strftime('%m/%d')}-{end.strftime('%m/%d')})"

        table.add_row(habit.name, target, progress_str)

    return Panel(table, title=f"Log activities for {on_date.strftime('%Y-%m-%d')}")
