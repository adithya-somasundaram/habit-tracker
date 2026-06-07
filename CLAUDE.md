# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Flask + SQLAlchemy CLI habit tracker backed by SQLite. There is no web UI yet — interaction happens through input-driven service functions run via a Python shell/script.

## Commands

Activate the venv first (it lives in `env/`):

```
source env/bin/activate
```

Initialize/create the database tables (run once, or after model changes):

```
python -c "from scripts import *"
```

Run the Flask app (port 9876):

```
python app.py
```

There is no test suite, linter, or build step configured currently.

## Architecture

- `app.py` defines the shared Flask `app`, SQLAlchemy `db`, and `session` objects. All models and services import `db`/`session` from here — there's a circular-import pattern (`app.py` doesn't import models; models import `db` from `app`), so always go through `app_context().push()` before querying (see `scripts.py`).
- `src/<domain>/` modules (`habit/`, `activity/`) each contain `model.py` (SQLAlchemy models) and `services.py` (business logic + interactive `*_input` functions that prompt via `input()`).
- `Habit` (`src/habit/model.py`) defines the target schema for a habit using three enums — `UnitType`, `OperationType`, `RangeType` — plus `target_units`, combined to express things like "greater than 30 minutes daily". Habit names are stored uppercased and have a partial-unique index enforcing uniqueness only among active habits (`is_active = 1`), allowing a deactivated habit's name to be reused.
- `Activity` (`src/activity/model.py`) records a single occurrence against a `Habit` via `habit_id`, with a date, optional `units`, and optional `description`.
- `src/activity/services.py` imports `get_habit_mapping` from `src/habit/services.py` lazily (inside the function) to avoid a circular import between the two domains.
- `get_habit_mapping` returns a 1-indexed `{index: habit}` dict, which the interactive `_input` flows use to let users select a habit by number.
- `src/helpers.py` provides `pacific_timezone` (via `pytz`), used to default activity dates to "today" in Pacific time.
- `scripts.py` is the entry point for ad-hoc setup/usage: it pushes an app context, calls `db.create_all()`, and exposes the interactive service functions (`create_habit_input`, `view_habits`, `deactivate_habit`, `create_activity_input`) for use in a REPL.
