from habit.model import Habit, UnitType, OperationType, RangeType


def get_active_habits(session, active_only=True):
    query = session.query(Habit)
    if active_only:
        query = query.filter(Habit.is_active == True)
    return query.all()


def create_habit(
    session,
    name,
    target_units=None,
    target_unit_type=None,
    target_operation_type=None,
    target_range=None,
):
    habit = Habit(
        name=name,
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


def _select_enum(prompt, enum_class):
    options = list(enum_class)
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option.value}")
    print("Hit enter to skip")
    choice = input("Select a number: ").strip()
    if not choice or choice == "":
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1].value
    print(f"Invalid selection, skipping.")
    return None


def create_habit_input(session):
    name = input("Enter habit name: ").strip()
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
