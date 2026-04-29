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


def create_habit_input(session):
    name = input("Enter habit name: ")
    if not name or name == "":
        print("Habit name cannot be empty.")
        return None

    target_units = input("Enter target units (optional): ")
    target_unit_type = input(
        f"Enter target unit type ({', '.join([e.value for e in UnitType])}) (optional): "
    )
    target_operation_type = input(
        f"Enter target operation type ({', '.join([e.value for e in OperationType])}) (optional): "
    )
    target_range = input(
        f"Enter target range ({', '.join([e.value for e in RangeType])}) (optional): "
    )

    return create_habit(
        session,
        name,
        int(target_units) if target_units else None,
        target_unit_type if target_unit_type else None,
        target_operation_type if target_operation_type else None,
        target_range if target_range else None,
    )
