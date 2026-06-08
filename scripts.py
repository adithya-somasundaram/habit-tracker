from app import *
from src.habit.services import *
from src.activity.services import *

app.app_context().push()
db.create_all()

print(
    "Available functions:\n"
    "  - view_habits(session): list your habits\n"
    "  - create_habits_bulk_input(session): add multiple habits in one go\n"
    "  - create_activities_bulk_input(session): log activities for a date across all habits"
)
