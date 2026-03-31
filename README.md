# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner plan and prioritize daily care tasks for their pet(s). It uses a smart scheduling algorithm to fit the most important tasks into the owner's available time window.

---

## 📸 Demo

<a href="/course_images/ai110/streamlit.png" target="_blank">
  <img src='/course_images/ai110/streamlit.png' title='PawPal App' width='' alt='PawPal App' class='center-block' />
</a>

---

## ✨ Features

- **Priority-based scheduling** — Tasks are sorted by priority (1–5). The scheduler fills the day with the highest-priority tasks first, dropping lower-priority ones if time runs out.
- **Duration tiebreaker** — Among tasks with equal priority, shorter tasks are scheduled first to maximize the number of tasks that fit.
- **Conflict detection** — If all priority-5 (critical) tasks combined exceed the owner's available time, the app displays a warning before generating the plan so the owner knows something will be dropped.
- **Recurring tasks** — Tasks can be marked as `daily` or `weekly`. When completed, their due date automatically advances using `timedelta` so they reappear on the correct day.
- **Filtering** — Tasks can be filtered by pet name or completion status. The UI shows both the scheduled plan and a separate table of all incomplete tasks with due dates.
- **Skipped task visibility** — Tasks that didn't fit in the schedule are shown separately so the owner knows what was left out and why.
- **Plan explanation** — The app explains why each task was chosen and what the total time usage looks like.

---

## 🗂 Project Structure
```
pawpal_system.py   # All backend classes: Task, Pet, Owner, Scheduler
app.py             # Streamlit UI
main.py            # CLI demo and manual testing script
tests/
  test_pawpal.py   # Automated test suite (pytest)
uml_final.png      # Final class diagram
reflection.md      # Design and AI collaboration reflection
```

---

## ⚙️ Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Run the App
```bash
python -m streamlit run app.py
```

---

## 🧪 Testing PawPal+
```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

- **Task completion** — Marking a task complete changes its status correctly
- **Task addition** — Adding a task to a pet increases that pet's task count
- **Time constraint** — Generated plan never exceeds owner's available minutes
- **Priority sorting** — Tasks are returned highest priority first
- **Empty pet** — Scheduler handles a pet with no tasks without crashing
- **Recurring reset** — Daily tasks reset `completed` to False and advance `due_date` by one day
- **Conflict detection** — Scheduler warns when priority-5 tasks alone exceed available time

### Confidence Level

⭐⭐⭐⭐ (4/5) — Core scheduling behaviors are well covered. Edge cases like weekly recurrence, multi-pet conflicts, and invalid input validation would be the next things to test.

---

## 🧠 Smarter Scheduling

PawPal+ includes several algorithmic improvements beyond basic task listing:

- **Priority-based sorting** — Tasks sorted by priority descending, duration ascending as tiebreaker
- **Filtering** — `get_tasks_by_pet()` and `get_incomplete_tasks()` for targeted task views
- **Recurring tasks** — `daily` and `weekly` frequencies with automatic `due_date` advancement via `timedelta`
- **Conflict detection** — Warns when critical tasks alone exceed the available time budget