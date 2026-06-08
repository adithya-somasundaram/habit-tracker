from src.habit.model import Habit, UnitType, OperationType, RangeType


def get_habit_mapping(session, active_only=True):
    habits = session.query(Habit)
    if active_only:
        habits = habits.filter(Habit.is_active == True)

    habits = habits.all()
    return {i: habit for i, habit in enumerate(habits, 1)}


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
