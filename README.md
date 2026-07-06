# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

PawPal+ helps a pet owner plan and organize daily care tasks. The finished app supports:

- **Add pets** — register one or more pets (name, species, and more) under an owner.
- **Add tasks** — create care tasks with a title, category, priority, duration, and due time.
- **Generate schedules** — build a daily plan that picks tasks by priority within a time budget.
- **Sort by time** — display tasks and schedules in chronological order (`sort_by_time`).
- **Filter tasks** — view tasks for a specific pet or by completion status (`filter_tasks`).
- **Recurring tasks** — completing a daily or weekly task automatically creates the next one (`complete_task`).
- **Conflict warnings** — flag tasks scheduled for the exact same time (`detect_conflicts`).

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Run the command-line demo to see the scheduler in action:

```bash
python main.py
```

It prints the same tasks unsorted, then sorted by time, then filtered, and
finally lists any scheduling conflicts (see the full output in
[Demo Walkthrough](#-demo-walkthrough) below).

## 🧪 Testing PawPal+

Run the automated tests with:

```bash
python -m pytest
```

The tests cover the core backend behaviors:

- **Task completion** — a task becomes complete after `mark_complete()`.
- **Task addition** — adding a task to a pet updates its list and back-reference.
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order.
- **Recurring task creation** — completing a daily task creates the next day's task.
- **Conflict detection** — two tasks at the same time produce a warning.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.9.2, pytest-8.4.2, pluggy-1.6.0
rootdir: C:\Users\ssbhi\Desktop\ai110-module2show-pawpal-starter
collected 5 items

tests\test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.03s ==============================
```

**Confidence: ★★★★☆ (4 / 5)** — The main backend behaviors are tested and passing, but more UI-level tests for the Streamlit app could be added later.

## 📐 Smarter Scheduling

Phase 4 adds an algorithmic layer on top of the core classes. All four methods
live on the `PawPalSystem` class and take a plain list of `Task` objects.

- **Sorting — `sort_by_time(tasks)`**: Returns the tasks ordered by `due_date`,
  earliest first. Tasks with no due date are placed at the end.
- **Filtering — `filter_tasks(tasks, pet_name=None, completed=None)`**: Returns
  only the tasks that match the filters you pass. You can filter by pet name, by
  completion status, or both at once. Leaving a filter as `None` skips it.
- **Recurring tasks — `complete_task(task)`**: Marks a task complete (using the
  simple `mark_complete()` method). If the task is recurring, it also creates the
  next occurrence — moving the date forward by 1 day for `"daily"` or 7 days for
  `"weekly"` — and adds that new task back to the same pet.
- **Conflict detection — `detect_conflicts(tasks)`**: Returns a list of warning
  strings when two or more tasks share the exact same `due_date`/time. Each
  warning lists the clashing task titles and their pet names. It returns an empty
  list when there are no conflicts (it never raises an error).

## 🎬 Demo Walkthrough

### Main UI features

Launch the Streamlit app with `streamlit run app.py`. From the UI you can:

- Enter an **owner** name and add one or more **pets** (name + species).
- Add **tasks** to a chosen pet with a title, category, priority, duration, due time, and completion status.
- See each pet's tasks in a table, **sorted by time**, showing pet, title, priority, duration, due time, and status.
- Choose a day and a **time budget**, then generate today's **schedule**.
- Read **conflict warnings** when two tasks share the same time.

### Example workflow

1. **Add a pet** — type a name (e.g. `Mochi`), pick a species, and click **Add pet**.
2. **Add a task** — select the pet, fill in the task details (e.g. `Morning walk`, high priority, 30 min, due 08:00), and click **Add task**.
3. **View today's schedule** — set the time budget (e.g. 90 minutes) and click **Generate schedule** to see the ordered plan for the day.

### Key scheduler behaviors

- **Sorted tasks** — both the task table and the generated schedule are shown earliest-first using `sort_by_time()`.
- **Conflict warnings** — if two tasks are booked for the exact same time, the app shows an `st.warning`; otherwise it confirms there are no conflicts.
- **Recurring tasks** — completing a daily or weekly task creates the next occurrence automatically via `complete_task()`.

### Sample CLI output

Running `python main.py` demonstrates the same logic in the terminal:

```
PawPal+ Demo for Jordan - Sunday, July 05, 2026

Unsorted tasks (as added)
------------------------------------------------------------
Time    Pet      Task             Priority  Status
------------------------------------------------------------
14:00   Mochi    Vet checkup      medium    Done
08:00   Mochi    Morning walk     high      Pending
12:00   Luna     Feed lunch       low       Pending
08:00   Luna     Litter box       high      Pending

Sorted by time
------------------------------------------------------------
Time    Pet      Task             Priority  Status
------------------------------------------------------------
08:00   Mochi    Morning walk     high      Pending
08:00   Luna     Litter box       high      Pending
12:00   Luna     Feed lunch       low       Pending
14:00   Mochi    Vet checkup      medium    Done

Filtered: incomplete tasks only
------------------------------------------------------------
Time    Pet      Task             Priority  Status
------------------------------------------------------------
08:00   Mochi    Morning walk     high      Pending
08:00   Luna     Litter box       high      Pending
12:00   Luna     Feed lunch       low       Pending

Filtered: Luna's tasks only
------------------------------------------------------------
Time    Pet      Task             Priority  Status
------------------------------------------------------------
08:00   Luna     Litter box       high      Pending
12:00   Luna     Feed lunch       low       Pending

Conflict Warnings
------------------------------------------------------------
! Conflict at 2026-07-05 08:00: 'Morning walk' (Mochi), 'Litter box' (Luna)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
