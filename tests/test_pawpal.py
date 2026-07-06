"""Simple pytest tests for the PawPal+ backend."""

from datetime import datetime, timedelta

from pawpal_system import PawPalSystem, Pet, Task


def test_task_completion():
    """A task starts incomplete and becomes complete after mark_complete()."""
    task = Task("t1", "Morning walk")
    assert task.is_complete is False

    task.mark_complete()
    assert task.is_complete is True


def test_task_addition():
    """Adding a task to a pet updates the list and the back-reference."""
    pet = Pet("p1", "Mochi", species="dog")
    task = Task("t1", "Morning walk")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert task.pet is pet


def test_sort_by_time():
    """sort_by_time() returns tasks in chronological order (earliest first)."""
    system = PawPalSystem()
    # Added out of order on purpose: 14:00, 08:00, 12:00.
    afternoon = Task("t1", "Vet checkup", due_date=datetime(2026, 7, 5, 14, 0))
    morning = Task("t2", "Morning walk", due_date=datetime(2026, 7, 5, 8, 0))
    midday = Task("t3", "Feed lunch", due_date=datetime(2026, 7, 5, 12, 0))

    ordered = system.sort_by_time([afternoon, morning, midday])

    assert ordered == [morning, midday, afternoon]


def test_recurring_daily_creates_next_day():
    """Completing a daily recurring task creates the next task one day later."""
    system = PawPalSystem()
    pet = Pet("p1", "Mochi", species="dog")
    task = Task(
        "t1",
        "Morning walk",
        due_date=datetime(2026, 7, 5, 8, 0),
        is_recurring=True,
        frequency="daily",
    )
    pet.add_task(task)

    next_task = system.complete_task(task)

    assert task.is_complete is True
    assert next_task is not None
    assert next_task.is_complete is False
    assert next_task.due_date == task.due_date + timedelta(days=1)
    # The new occurrence is attached back to the same pet.
    assert next_task in pet.tasks


def test_detect_conflicts_same_time():
    """Two tasks at the exact same due_date produce a conflict warning."""
    system = PawPalSystem()
    same_time = datetime(2026, 7, 5, 8, 0)
    walk = Task("t1", "Morning walk", due_date=same_time)
    litter = Task("t2", "Litter box", due_date=same_time)

    warnings = system.detect_conflicts([walk, litter])

    assert len(warnings) == 1
