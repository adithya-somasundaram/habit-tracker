from app import *
from src.habit.services import create_habit_input, view_habits, deactivate_habit
from src.activity.services import create_activity_input

app.app_context().push()
db.create_all()
