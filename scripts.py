from app import *
from src.habit.services import *
from src.activity.services import *

app.app_context().push()
db.create_all()
