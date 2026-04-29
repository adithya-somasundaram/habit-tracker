from app import *
from src.habit.services import create_habit_input, view_habits, deactivate_habit

app.app_context().push()
db.create_all()
