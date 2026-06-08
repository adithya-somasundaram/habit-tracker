from rich.table import Table


def make_table(*columns, **kwargs):
    kwargs.setdefault("show_header", True)
    kwargs.setdefault("header_style", "bold")
    kwargs.setdefault("box", None)
    kwargs.setdefault("padding", (0, 2))

    table = Table(**kwargs)
    for column in columns:
        if isinstance(column, tuple):
            name, column_kwargs = column
            table.add_column(name, **column_kwargs)
        else:
            table.add_column(column)

    return table


def format_habit_target(habit):
    if not (
        habit.target_operation_type
        and habit.target_range
        and habit.target_units is not None
    ):
        return ""

    unit = habit.target_unit_type.value if habit.target_unit_type else ""
    operation = habit.target_operation_type.value.replace("_", " ")
    return f"{operation} {habit.target_units} {unit} {habit.target_range.value}"
