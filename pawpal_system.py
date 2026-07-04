"""PawPal+ — core class skeleton.

Skeleton generated from diagrams/uml.mmd. Attributes are defined; method
bodies are intentionally left as stubs for you to implement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """A single pet-care activity (feeding, walk, vet visit, ...)."""

    task_id: str
    title: str
    description: str = ""
    category: str = ""
    due_date: datetime | None = None
    is_complete: bool = False
    is_recurring: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        raise NotImplementedError

    def reschedule(self, new_date: datetime) -> None:
        """Move this task to a new due date."""
        raise NotImplementedError

    def is_overdue(self) -> bool:
        """Return True if the task is past its due date and not complete."""
        raise NotImplementedError


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

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        raise NotImplementedError

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by its id."""
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        raise NotImplementedError

    def get_upcoming_tasks(self) -> list[Task]:
        """Return incomplete tasks ordered by due date."""
        raise NotImplementedError


@dataclass
class Owner:
    """A pet owner who can have one or more pets."""

    owner_id: str
    name: str
    email: str = ""
    phone: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        raise NotImplementedError

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by its id."""
        raise NotImplementedError

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        raise NotImplementedError

    def update_contact_info(self, email: str, phone: str) -> None:
        """Update the owner's contact details."""
        raise NotImplementedError


@dataclass
class PawPalSystem:
    """Top-level coordinator that manages owners, pets, and scheduling."""

    system_id: str = "pawpal"
    owners: list[Owner] = field(default_factory=list)

    def register_owner(self, owner: Owner) -> None:
        """Add an owner to the system."""
        raise NotImplementedError

    def remove_owner(self, owner_id: str) -> None:
        """Remove an owner from the system by id."""
        raise NotImplementedError

    def find_owner(self, owner_id: str) -> Owner | None:
        """Look up an owner by id, or return None if not found."""
        raise NotImplementedError

    def get_all_pets(self) -> list[Pet]:
        """Return every pet across all owners."""
        raise NotImplementedError

    def send_reminder(self, task: Task) -> None:
        """Notify the relevant owner about an upcoming or overdue task."""
        raise NotImplementedError

    def generate_schedule(self, owner: Owner) -> list[Task]:
        """Build an ordered plan of tasks for the given owner."""
        raise NotImplementedError
