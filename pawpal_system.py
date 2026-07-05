"""PawPal+ — core class skeleton.

Skeleton generated from diagrams/uml.mmd. Attributes are defined; method
bodies are intentionally left as stubs for you to implement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


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
    # Back-reference to the owning Pet; set by Pet.add_task(). Excluded from
    # repr/eq to avoid recursive representation and identity coupling.
    pet: Pet | None = field(default=None, repr=False, compare=False)

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
    # Back-reference to the owning Owner; set by Owner.add_pet().
    owner: Owner | None = field(default=None, repr=False, compare=False)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet and set task.pet back to self."""
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
        """Register a new pet under this owner and set pet.owner back to self."""
        raise NotImplementedError

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner by its id."""
        raise NotImplementedError

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        raise NotImplementedError

    def update_contact_info(
        self, email: str | None = None, phone: str | None = None
    ) -> None:
        """Update the owner's contact details (only the fields provided)."""
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
        """Notify the relevant owner about an upcoming or overdue task.

        Resolves the owner via task.pet.owner, so the back-references must be
        set (use Pet.add_task / Owner.add_pet when wiring objects together).
        """
        raise NotImplementedError

    def generate_schedule(
        self, owner: Owner, day: date, available_minutes: int
    ) -> list[Task]:
        """Build an ordered plan for `day`, choosing and ordering the owner's
        tasks by priority/duration within the `available_minutes` budget."""
        raise NotImplementedError
