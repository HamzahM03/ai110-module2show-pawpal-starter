# PawPal+ Project Reflection

## 1. System Design

The three core actions a user should be able to perform are:

Enter owner and pet information — the user provides basic details (owner name, pet name, time available per day) so the scheduler knows the context it's working within.
Add and manage care tasks — the user can create tasks (e.g., walk, feed, give medication) and assign each a duration and priority level, building the pool of tasks the scheduler will work with.
Generate a daily plan — the app takes the task list and constraints and produces a prioritized daily schedule, explaining why tasks were ordered or excluded.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I designed four classes: Task, Pet, Owner, and Scheduler. Task holds a single care action with a name, duration, priority, category, and completed status, it knows whether it can be scheduled and can mark itself done. Pet owns a list of tasks and represents the animal being cared for (name, species, age). Owner holds the person's name, daily available time, and preferences, and maintains a list of pets. Scheduler is the logic layer, it takes a pet and the owner's available time, pulls the task list, and generates an ordered daily plan with an explanation.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the skeleton, I noticed Scheduler was maintaining its own task_list separately from pet.tasks, which would create a sync problem. I removed self.task_list from Scheduler and updated generate_plan() to pull tasks directly from self.pet.get_tasks() instead. I also noted that Owner is not passed into Scheduler — the caller passes available_minutes directly — and documented this as an intentional simplification for now.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two constraints: available time (minutes) and task priority (1–5). Time is a hard constraint — tasks that don't fit are dropped entirely regardless of priority. Priority determines order, so high-priority tasks are always scheduled first. I chose time as the hard constraint because pet care has a fixed daily window and it's better to drop low-priority tasks than to overcommit the owner.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a greedy algorithm: it fills the schedule top-to-bottom by priority and drops any task that doesn't fit in the remaining time, then continues checking the rest. This means a 25-minute low-priority task might get skipped while a 5-minute task behind it still fits. The tradeoff is that the schedule is never truly optimal — a dynamic programming approach could find the maximum-value combination of tasks within the time budget. However, the greedy approach is fast, predictable, and easy to explain to a pet owner. For a daily care app, explainability matters more than perfect optimization.




---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools throughout every phase of this project. In the design phase, I used it to brainstorm classes and generate the initial Mermaid UML diagram. During implementation, I used it to generate method stubs and flesh out the scheduling logic. For testing, I used it to draft pytest functions covering edge cases I hadn't thought of. The most helpful prompts were specific ones that referenced my actual code — asking "based on this skeleton, how should Scheduler retrieve tasks from Owner" got a much better answer than a generic question about schedulers.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I asked AI to suggest a more Pythonic version of generate_plan(), it proposed using itertools.takewhile(). I rejected this because takewhile stops at the first task that doesn't fit, which means a 25-minute low-priority task would block a 5-minute task behind it from being scheduled. My greedy loop correctly skips tasks that don't fit and keeps checking the rest. The AI suggestion was shorter but logically wrong for this use case. I caught it by tracing through a concrete example manually.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion status, pet task count after adding, plan staying within available time, priority sort order, empty pet handling, daily recurrence reset, and conflict detection triggering correctly. These were important because they cover both the happy path and the edge cases most likely to break silently — a scheduler that runs but returns wrong results is worse than one that crashes.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

4/5. The core scheduling logic is well covered. I would next test weekly recurrence, multi-pet conflict scenarios where tasks from different pets compete, and invalid input like negative duration or priority out of range.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The separation between the logic layer (pawpal_system.py) and the UI (app.py) worked well. Because I built and tested the backend in isolation first using main.py, wiring it to Streamlit was straightforward — I wasn't debugging logic and UI at the same time.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a time_of_day field to Task so the scheduler could produce an actual ordered timeline (8am walk, 8:30am feed) rather than just a priority-ranked list. I would also support multiple pets more explicitly in the UI — right now it always assigns tasks to pets[0].

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that AI is a fast first-draft tool, not a decision-maker. It can generate a working implementation in seconds, but it doesn't know your constraints, your design goals, or what "correct" means for your specific problem. The itertools.takewhile suggestion looked clean but was wrong. Being the lead architect means you have to understand the code well enough to catch that — you can't just accept output because it runs.