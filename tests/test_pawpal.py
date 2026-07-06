"""Simple pytest tests for the PawPal+ backend."""

from pawpal_system import Pet, Task


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
