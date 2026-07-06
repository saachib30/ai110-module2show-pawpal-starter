import streamlit as st
from datetime import date, datetime, time

from pawpal_system import Owner, PawPalSystem, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Create the system and owner once, then reuse them across reruns.
if "system" not in st.session_state:
    st.session_state.system = PawPalSystem()
    st.session_state.owner = Owner("owner-1", owner_name)
    st.session_state.system.register_owner(st.session_state.owner)
    st.session_state.pet_counter = 0  # always-increasing, for unique pet ids
    st.session_state.task_counter = 0  # always-increasing, for unique task ids

system = st.session_state.system
owner = st.session_state.owner
owner.name = owner_name  # keep the owner's name in sync with the input above

# Add the pet from the inputs above.
if st.button("Add pet"):
    st.session_state.pet_counter += 1
    pet_id = f"pet-{st.session_state.pet_counter}"
    new_pet = Pet(pet_id, pet_name, species)
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name} ({new_pet.species}).")

pets = owner.get_pets()
if pets:
    st.write("Pets: " + ", ".join(p.name for p in pets))
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These are stored on the selected pet and feed into the scheduler.")

pets = owner.get_pets()
if not pets:
    st.info("Add a pet first, then you can add tasks.")
else:
    pet_choice = st.selectbox("For which pet?", [p.name for p in pets])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        category = st.text_input("Category", value="exercise")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    description = st.text_input("Description", value="")

    col4, col5, col6 = st.columns(3)
    with col4:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col5:
        due_time = st.time_input("Due time (today)", value=time(8, 0))
    with col6:
        is_complete = st.checkbox("Already done?", value=False)

    if st.button("Add task"):
        selected_pet = next(p for p in pets if p.name == pet_choice)
        st.session_state.task_counter += 1
        task_id = f"task-{st.session_state.task_counter}"
        due = datetime.combine(date.today(), due_time)
        new_task = Task(
            task_id,
            task_title,
            description=description,
            category=category,
            priority=priority,
            duration_minutes=int(duration),
            due_date=due,
            is_complete=is_complete,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added '{new_task.title}' for {selected_pet.name}.")

    # Show the tasks for the currently selected pet, sorted chronologically.
    selected_pet = next(p for p in pets if p.name == pet_choice)
    sorted_tasks = system.sort_by_time(selected_pet.get_tasks())
    task_rows = [
        {
            "pet": selected_pet.name,
            "title": t.title,
            "category": t.category,
            "priority": t.priority,
            "duration_minutes": t.duration_minutes,
            "due": t.due_date.strftime("%H:%M") if t.due_date else "-",
            "done": t.is_complete,
        }
        for t in sorted_tasks
    ]
    if task_rows:
        st.write(f"Current tasks for {selected_pet.name}:")
        st.table(task_rows)
    else:
        st.info("No tasks yet for this pet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates today's plan from your pets' tasks, ordered by priority within a time budget.")

col_day, col_mins = st.columns(2)
with col_day:
    selected_day = st.date_input("Day to plan", value=date.today())
with col_mins:
    available_minutes = st.number_input(
        "Time available (minutes)", min_value=1, max_value=1440, value=90
    )

if st.button("Generate schedule"):
    schedule = st.session_state.system.generate_schedule(
        st.session_state.owner, selected_day, int(available_minutes)
    )
    if not schedule:
        st.info("No tasks fit this day's schedule. Add tasks for that day or increase the time budget.")
    else:
        st.write("### Schedule")
        # Display the planned tasks in chronological order.
        ordered_schedule = system.sort_by_time(schedule)
        schedule_rows = [
            {
                "when": t.due_date.strftime("%Y-%m-%d %H:%M") if t.due_date else "-",
                "pet": t.pet.name if t.pet else "-",
                "task": t.title,
                "priority": t.priority,
                "duration_minutes": t.duration_minutes,
                "status": "Done" if t.is_complete else "Pending",
            }
            for t in ordered_schedule
        ]
        st.table(schedule_rows)

        # Warn about any tasks scheduled for the exact same time.
        conflicts = system.detect_conflicts(ordered_schedule)
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("No scheduling conflicts found.")
