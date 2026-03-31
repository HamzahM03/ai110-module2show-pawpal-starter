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

The scheduler considers two constraints: available time (minutes) and task priority (1–5). I decided time was the hard constraint — tasks that don't fit get dropped entirely. Priority determines order, so high-priority tasks always get scheduled first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a greedy approach: it fills the schedule top-to-bottom by priority until time runs out. This means a lower-priority task that would fit gets skipped if a higher-priority task ahead of it already consumed the remaining time. This is reasonable because pet care has real priorities — medication matters more than playtime — and the owner would rather have the most important tasks done than a "fuller" schedule with less critical ones.




---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
