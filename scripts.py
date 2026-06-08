from app import *
from src.habit.services import (
    create_habit_input,
    create_habits_bulk_input,
    view_habits,
)
from src.habit.infra import deactivate_habit
from src.activity.services import create_activity_input

app.app_context().push()
db.create_all()
