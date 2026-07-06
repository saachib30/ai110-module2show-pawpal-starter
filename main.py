"""PawPal+ CLI demo — exercises the backend logic in pawpal_system.py.

Run with:  python main.py
"""

from datetime import date, datetime, time

from pawpal_system import Owner, PawPalSystem, Pet, Task


def at(day: date, hour: int, minute: int = 0) -> datetime:
    """Return a datetime on `day` at the given hour/minute."""
    return datetime.combine(day, time(hour, minute))


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

    # 3. Tasks with different times, priorities, and durations
    mochi.add_task(Task("t1", "Morning walk", priority="high",
                        duration_minutes=30, due_date=at(today, 8)))
    mochi.add_task(Task("t2", "Vet checkup", priority="medium",
                        duration_minutes=45, due_date=at(today, 14)))
    luna.add_task(Task("t3", "Feed lunch", priority="low",
                       duration_minutes=15, due_date=at(today, 12)))
    luna.add_task(Task("t4", "Litter box", priority="high",
                       duration_minutes=10, due_date=at(today, 9)))

    # 4. Generate today's schedule within a time budget
    available_minutes = 90
    schedule = system.generate_schedule(owner, today, available_minutes)

    # 5. Print a clean, readable schedule
    print()
    print(f"Today's Schedule for {owner.name} - {today:%A, %B %d, %Y}")
    print(f"(time budget: {available_minutes} min)")
    print("-" * 68)
    print(f"{'Time':<7} {'Pet':<8} {'Task':<16} {'Priority':<9} {'Mins':<5} Status")
    print("-" * 68)

    if not schedule:
        print("No tasks fit today's schedule.")
    else:
        total = 0
        for task in schedule:
            pet_name = task.pet.name if task.pet else "-"
            when = f"{task.due_date:%H:%M}" if task.due_date else "--:--"
            status = "Done" if task.is_complete else "Pending"
            total += task.duration_minutes
            print(f"{when:<7} {pet_name:<8} {task.title:<16} "
                  f"{task.priority:<9} {task.duration_minutes:<5} {status}")
        print("-" * 68)
        print(f"{len(schedule)} task(s) planned, {total} of {available_minutes} min used.")
    print()


if __name__ == "__main__":
    main()
