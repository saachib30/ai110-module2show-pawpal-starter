"""PawPal+ — core classes.

Implements the pet-care domain model from diagrams/uml.mmd: Task, Pet,
Owner, and the PawPalSystem coordinator/scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

# Higher number = more important. Used to order the daily schedule.
PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """A single pet-care activity (feeding, walk, vet visit, ...)."""

    task_id: str
    title: str
    description: str = ""
    category: str = ""
    priority: str = "medium"  # "low" | "medium" | "high"
    duration_minutes: int = 0
    due_date: datetime | None = None
    is_complete: bool = False
    is_recurring: bool = False
    frequency: str = "none"  # "none" | "daily" | "weekly"
    # Back-reference to the owning Pet; set by Pet.add_task(). Excluded from
    # repr/eq to avoid recursive representation and identity coupling.
    pet: Pet | None = field(default=None, repr=False, compare=False)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_complete = True

    def reschedule(self, new_date: datetime) -> None:
        """Move this task to a new due date."""
        self.due_date = new_date

    def is_overdue(self) -> bool:
        """Return True if the task is past its due date and not complete."""
        if self.is_complete or self.due_date is None:
            return False
        return self.due_date < datetime.now()


@dataclass
class Pet:
    """A pet owned by an Owner, with its own list of care tasks."""

    pet_id: str
    name: str
    species: str
    breed: str = ""
    age: int = 0
    weight: float = 0.0
    tasks: list[Task] = field(default_factory=list)
    # Back-reference to the owning Owner; set by Owner.add_pet().
    owner: Owner | None = field(default=None, repr=False, compare=False)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet and link it back to self."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by its id."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_upcoming_tasks(self) -> list[Task]:
        """Return incomplete tasks ordered by due date (undated ones last)."""
        upcoming = [t for t in self.tasks if not t.is_complete]
        return sorted(upcoming, key=lambda t: (t.due_date is None, t.due_date or datetime.max))


@dataclass
class Owner:
    """A pet owner who can have one or more pets."""

    owner_id: str
    name: str
    email: str = ""
    phone: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner and link it back to self."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by its id."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def update_contact_info(
        self, email: str | None = None, phone: str | None = None
    ) -> None:
        """Update the owner's contact details (only the fields provided)."""
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone


@dataclass
class PawPalSystem:
    """Top-level coordinator that manages owners, pets, and scheduling."""

    system_id: str = "pawpal"
    owners: list[Owner] = field(default_factory=list)

    def register_owner(self, owner: Owner) -> None:
        """Add an owner to the system."""
        self.owners.append(owner)

    def remove_owner(self, owner_id: str) -> None:
        """Remove an owner from the system by id."""
        self.owners = [o for o in self.owners if o.owner_id != owner_id]

    def find_owner(self, owner_id: str) -> Owner | None:
        """Look up an owner by id, or return None if not found."""
        for owner in self.owners:
            if owner.owner_id == owner_id:
                return owner
        return None

    def get_all_pets(self) -> list[Pet]:
        """Return every pet across all owners."""
        return [pet for owner in self.owners for pet in owner.pets]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by due_date (undated tasks go last)."""
        return sorted(
            tasks, key=lambda t: (t.due_date is None, t.due_date or datetime.max)
        )

    def filter_tasks(
        self,
        tasks: list[Task],
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching the given pet name and/or completion status."""
        result = []
        for task in tasks:
            if pet_name is not None and (task.pet is None or task.pet.name != pet_name):
                continue
            if completed is not None and task.is_complete != completed:
                continue
            result.append(task)
        return result

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks that share the exact same due date/time."""
        # Group tasks by their due_date (skip tasks that have no date).
        by_time: dict[datetime, list[Task]] = {}
        for task in tasks:
            if task.due_date is not None:
                by_time.setdefault(task.due_date, []).append(task)

        warnings = []
        for due_date, clashing in by_time.items():
            if len(clashing) > 1:
                labels = [
                    f"'{t.title}' ({t.pet.name if t.pet else 'no pet'})"
                    for t in clashing
                ]
                warnings.append(
                    f"Conflict at {due_date:%Y-%m-%d %H:%M}: " + ", ".join(labels)
                )
        return warnings

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete and, if recurring, create its next occurrence."""
        task.mark_complete()

        # Only recurring tasks with a known due date can roll forward.
        if not task.is_recurring or task.due_date is None:
            return None

        if task.frequency == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.due_date + timedelta(days=7)
        else:
            return None

        # Copy the task's details, but reset completion and use the new date.
        next_task = Task(
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            category=task.category,
            priority=task.priority,
            duration_minutes=task.duration_minutes,
            due_date=next_date,
            is_complete=False,
            is_recurring=True,
            frequency=task.frequency,
        )

        # Attach the new task back to the same pet, if there is one.
        if task.pet is not None:
            task.pet.add_task(next_task)
        return next_task

    def send_reminder(self, task: Task) -> str:
        """Build a reminder message for the owner of the task's pet."""
        pet = task.pet
        owner = pet.owner if pet else None
        who = owner.name if owner else "the owner"
        contact = owner.email if owner and owner.email else "no contact on file"
        return f"Reminder for {who} ({contact}): '{task.title}' is due for {pet.name if pet else 'a pet'}."

    def generate_schedule(
        self, owner: Owner, day: date, available_minutes: int
    ) -> list[Task]:
        """Plan the owner's due-today tasks by priority within a time budget."""
        # Gather every incomplete task for this owner's pets that is due on `day`.
        candidates = [
            task
            for pet in owner.pets
            for task in pet.tasks
            if not task.is_complete
            and task.due_date is not None
            and task.due_date.date() == day
        ]

        # Highest priority first; break ties by earliest due time.
        candidates.sort(
            key=lambda t: (-PRIORITY_ORDER.get(t.priority, 0), t.due_date or datetime.max)
        )

        # Greedily include tasks that still fit in the remaining time budget.
        schedule: list[Task] = []
        remaining = available_minutes
        for task in candidates:
            if task.duration_minutes <= remaining:
                schedule.append(task)
                remaining -= task.duration_minutes
        return schedule
