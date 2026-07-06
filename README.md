# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule for Jordan - Saturday, July 04, 2026
(time budget: 90 min)
--------------------------------------------------------------------
Time    Pet      Task             Priority  Mins  Status
--------------------------------------------------------------------
08:00   Mochi    Morning walk     high      30    Pending
09:00   Luna     Litter box       high      10    Pending
14:00   Mochi    Vet checkup      medium    45    Pending
--------------------------------------------------------------------

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
