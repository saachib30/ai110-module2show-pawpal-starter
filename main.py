"""PawPal+ CLI demo — exercises the backend logic in pawpal_system.py.

Run with:  python main.py
"""

from datetime import date, datetime, time

from pawpal_system import Owner, PawPalSystem, Pet, Task


def at(day: date, hour: int, minute: int = 0) -> datetime:
    """Return a datetime on `day` at the given hour/minute."""
    return datetime.combine(day, time(hour, minute))


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a titled, aligned table of tasks."""
    print()
    print(title)
    print("-" * 60)
    print(f"{'Time':<7} {'Pet':<8} {'Task':<16} {'Priority':<9} Status")
    print("-" * 60)
    if not tasks:
        print("(no tasks)")
    else:
        for task in tasks:
            pet_name = task.pet.name if task.pet else "-"
            when = f"{task.due_date:%H:%M}" if task.due_date else "--:--"
            status = "Done" if task.is_complete else "Pending"
            print(f"{when:<7} {pet_name:<8} {task.title:<16} "
                  f"{task.priority:<9} {status}")


def main() -> None:
    today = date.today()

    # 1. System + owner
    system = PawPalSystem()
    owner = Owner("o1", "Jordan", email="jordan@example.com", phone="555-0100")
    system.register_owner(owner)

    # 2. Two pets, added to the owner
    mochi = Pet("p1", "Mochi", species="dog")
    luna = Pet("p2", "Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # 3. Tasks added intentionally OUT of time order (2pm, then 8am, ...)
    mochi.add_task(Task("t2", "Vet checkup", priority="medium",
                        duration_minutes=45, due_date=at(today, 14)))
    mochi.add_task(Task("t1", "Morning walk", priority="high",
                        duration_minutes=30, due_date=at(today, 8)))
    luna.add_task(Task("t3", "Feed lunch", priority="low",
                       duration_minutes=15, due_date=at(today, 12)))
    # Scheduled at 08:00 on purpose — clashes with Mochi's 08:00 walk.
    luna.add_task(Task("t4", "Litter box", priority="high",
                       duration_minutes=10, due_date=at(today, 8)))

    # Mark one task complete so the completion filter has something to show.
    mochi.tasks[0].mark_complete()  # Vet checkup -> Done

    # Collect every task across all pets.
    all_tasks = [task for pet in system.get_all_pets() for task in pet.get_tasks()]

    print()
    print(f"PawPal+ Demo for {owner.name} - {today:%A, %B %d, %Y}")

    # 4a. Unsorted list (in the order tasks were added).
    print_tasks("Unsorted tasks (as added)", all_tasks)

    # 4b. Sorted by time using sort_by_time().
    sorted_tasks = system.sort_by_time(all_tasks)
    print_tasks("Sorted by time", sorted_tasks)

    # 4c. Filter: only incomplete tasks, still sorted by time.
    incomplete = system.filter_tasks(sorted_tasks, completed=False)
    print_tasks("Filtered: incomplete tasks only", incomplete)

    # 4d. Filter: only Luna's tasks.
    luna_tasks = system.filter_tasks(sorted_tasks, pet_name="Luna")
    print_tasks("Filtered: Luna's tasks only", luna_tasks)

    # 5. Conflict detection: any tasks sharing the exact same time.
    print()
    print("Conflict Warnings")
    print("-" * 60)
    conflicts = system.detect_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"! {warning}")
    else:
        print("No conflicts found.")

    print()


if __name__ == "__main__":
    main()
