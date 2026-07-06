# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Ans: My initial UML design for PawPal+ included four main classes: `Owner`, `Pet`, `Task`, and `PawPalSystem`. The `Owner` class represents the user and stores the pets they care for. The `Pet` class stores details about each pet, such as name, species, breed, age, weight, and its list of care tasks. The `Task` class represents a pet care activity, such as feeding, walking, grooming, or a vet visit. The `PawPalSystem` class acts as the main coordinator for the app by managing owners, finding pets, sending reminders, and generating a daily schedule.

The main relationships in my design are that one `Owner` can have many `Pet` objects, and one `Pet` can have many `Task` objects. The three core user actions are adding pets, creating pet care tasks, and generating or viewing a daily schedule of tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Ans: Yes, my design changed after reviewing the first skeleton. The original design only had one-way relationships from `PawPalSystem` to `Owner`, from `Owner` to `Pet`, and from `Pet` to `Task`. I updated the design to include back-references so that a `Task` can reference its `Pet`, and a `Pet` can reference its `Owner`. This makes features like `send_reminder(task)` easier because the system can quickly find the correct owner through `task.pet.owner` instead of scanning through every owner, pet, and task.

I also updated the `Task` class to include `priority` and `duration_minutes` because the app needs those fields to generate a useful schedule. Without them, `generate_schedule()` would not know which tasks are most important or how long each task takes. Finally, I changed `generate_schedule()` to accept an `owner`, a `day`, and `available_minutes` so it can create a daily plan within a time budget.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Ans: My scheduler considers three constraints in `generate_schedule()`: the day a task is due, the task's priority (high, medium, or low), and how much time the owner has available. It first gathers the incomplete tasks that are due on the chosen day, sorts them so higher priority comes first (breaking ties by earliest due time), and then greedily adds tasks until the time budget runs out. I decided that priority and available time mattered most because a busy pet owner usually cannot do everything in one day, so the app should make sure the most important tasks are planned first and that the plan actually fits the time they have. I did not implement owner "preferences" as a real constraint yet, even though the scenario mentions it, so I tried to be honest about that in the design rather than pretend the app does more than it does.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Ans: One tradeoff my scheduler makes is in how it detects conflicts. Right now `detect_conflicts()` only checks for tasks that have the exact same `due_date`/time. It does not use each task's duration to figure out if two tasks actually overlap, so a 30-minute walk at 8:00 and a feeding at 8:15 would not be flagged as a conflict even though they clash in real life. I decided to keep it this way because exact-time matching is simple to write and easy to read, and it still catches the most obvious problem of booking two tasks at the same start time. The downside is that it can miss overlapping tasks, so if I had more time I would extend it to compare start and end times using `duration_minutes`.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
Ans: I used an AI coding assistant across every phase of the project: brainstorming the UML design, turning the diagram into class skeletons, implementing the scheduler logic in small steps, writing tests, and polishing the UI and documentation. The AI features that helped me most were the ones where the assistant could read my actual files before answering, explain a plan before making any edits, and then run `python main.py` and `pytest` to show me the real output. Being able to verify changes right away, instead of guessing, gave me a lot more confidence.

The prompts that worked best were specific ones. Asking "inspect these files but do not edit yet, then explain the plan" kept the assistant from making big changes I didn't want. Asking "which of these changes are actually worth making for a beginner project?" was also very helpful, because it stopped me from adding complicated code I didn't really need.

Another thing that helped me stay organized was using separate chat sessions for different phases (design, backend logic, the algorithmic layer, testing, and UI/documentation). Keeping each phase in its own session meant I only had to share the files that mattered for that step, the context stayed focused, and it was easier to go back and remember what I had decided in each part of the project.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
Ans: One moment where I did not accept a suggestion as-is was during the recurring task feature. When reviewing `complete_task()`, the assistant suggested I could shorten the code by using `dataclasses.replace()` to copy the task instead of writing out each field in the `Task(...)` constructor. It would have been fewer lines, but it hid which fields actually change when a task repeats. Since this is a learning project, I chose to keep the explicit constructor so the code clearly shows that only the due date changes and the completion status resets. I made similar calls elsewhere, like keeping a simple `for` loop in `filter_tasks()` instead of a denser list comprehension, and keeping conflict detection based on exact times instead of adding more complex overlap math.

The main way I verified AI suggestions was by running the code. After each change I ran `python main.py` to see the printed tasks, schedule, and conflict warnings, and I ran `python -m pytest` to make sure my five tests still passed. If the output matched what I expected, I kept the change; if something looked off, I asked the assistant to explain it before moving on. I treated the AI's output as a draft to check, not as an answer to trust automatically.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
Ans: I wrote five automated tests in `tests/test_pawpal.py`. They check basic task completion, adding a task to a pet (including the back-reference), sorting tasks into chronological order with `sort_by_time()`, recurring task creation where completing a daily task makes a new task for the next day, and conflict detection when two tasks share the exact same time. These tests were important because they cover the core behaviors a user depends on: if sorting, recurrence, or conflict detection broke, the schedule would quietly show wrong information. To keep the tests reliable, I used fixed datetimes like `datetime(2026, 7, 5, 8, 0)` instead of the current time so the results are the same every time they run.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
Ans: I am fairly confident (about 4 out of 5) that the core backend works correctly, because the important behaviors are covered by passing tests and I also checked them by hand through the CLI demo and the Streamlit app. I am less sure about edge cases that I have not tested yet. If I had more time, I would add tests for a pet with no tasks, tasks with no due date, filtering by both pet name and completion status at once, weekly recurrence (not just daily), and overlapping durations rather than only exact-time conflicts. I would also add a few tests for the Streamlit UI, since right now my tests only cover the backend logic.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Ans: I am most satisfied with the algorithmic layer I added on top of the core classes. Building `sort_by_time()`, `filter_tasks()`, `complete_task()`, and `detect_conflicts()` one at a time, and then connecting sorting and conflict warnings into the Streamlit UI, made the app feel like a real planning tool instead of just a list of tasks. I am also happy that the back-reference design from early on paid off, because it made features like reminders and conflict messages (which show the pet's name) simple to build.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Ans: If I had another iteration, I would improve conflict detection so it uses each task's `duration_minutes` to catch overlapping tasks, not just tasks that start at the exact same time. I would also make recurring tasks easier to use in the Streamlit UI by adding a "complete task" button that calls `complete_task()`, so a user could actually see the next occurrence appear. Finally, I would try to add real owner preferences as a scheduling constraint, since the scenario mentions them but my scheduler does not use them yet.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Ans: The most important thing I learned is that I am the lead architect and the AI is a tool that works for me, not the other way around. The assistant was great at generating options, explaining tradeoffs, and writing boilerplate quickly, but I still had to make the real decisions: what classes to use, how conflict detection should behave, which suggestions to accept, and when simpler code was better than clever code. Giving clear, specific instructions and then verifying the results by running the code taught me that good judgment and a clear design vision matter more than just getting an AI to produce a lot of code.
