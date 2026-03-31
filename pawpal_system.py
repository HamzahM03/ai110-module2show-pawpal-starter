from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    name: str
    duration: int          # minutes
    priority: int          # 1 (low) to 5 (high)
    category: str          # "walk" | "feed" | "med" | "grooming" | "enrichment"
    completed: bool = False
    recurring: bool = False
    frequency: str = "none"   # "none" | "daily" | "weekly"
    due_date: date = field(default_factory=date.today)

    def __post_init__(self):
        if not (1 <= self.priority <= 5):
            raise ValueError(f"Priority must be 1–5, got {self.priority}")
        if self.duration <= 0:
            raise ValueError(f"Duration must be positive, got {self.duration}")
        if self.frequency not in ("none", "daily", "weekly"):
            raise ValueError(f"Frequency must be 'none', 'daily', or 'weekly', got {self.frequency}")

    def mark_complete(self) -> None:
        """Mark task complete and advance due_date if recurring."""
        self.completed = True
        if self.frequency == "daily":
            self.due_date = date.today() + timedelta(days=1)
            self.completed = False   # auto-reset for tomorrow
        elif self.frequency == "weekly":
            self.due_date = date.today() + timedelta(weeks=1)
            self.completed = False   # auto-reset for next week

    def reset(self) -> None:
        """Manually reset a recurring task (used by reset_day)."""
        if self.recurring:
            self.completed = False

    def is_schedulable(self) -> bool:
        """Return True if task is incomplete and due today or earlier."""
        return not self.completed and self.due_date <= date.today()


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks associated with this pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> list[Task]:
        """Return only tasks that haven't been completed."""
        return [t for t in self.tasks if not t.completed]

    def reset_recurring(self) -> None:
        """Reset all recurring tasks for a new day."""
        for task in self.tasks:
            task.reset()


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_available_time(self) -> int:
        """Return how many minutes the owner has available today."""
        return self.available_minutes

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_tasks_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks for a specific pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def get_incomplete_tasks(self) -> list[Task]:
        """Return all incomplete tasks across all pets."""
        return [t for t in self.get_all_tasks() if not t.completed]

    def reset_day(self) -> None:
        """Reset all recurring tasks across all pets for a new day."""
        for pet in self.pets:
            pet.reset_recurring()


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.available_time = owner.get_available_time()
        self._plan: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """
        Sort schedulable tasks by priority descending, duration ascending as tiebreaker,
        then greedily add tasks until available_time is exhausted.
        """
        schedulable = [t for t in self.owner.get_all_tasks() if t.is_schedulable()]
        schedulable.sort(key=lambda t: (-t.priority, t.duration))

        plan = []
        time_remaining = self.available_time

        for task in schedulable:
            if task.duration <= time_remaining:
                plan.append(task)
                time_remaining -= task.duration

        self._plan = plan
        return self._plan

    def detect_conflicts(self) -> list[str]:
        """Warn if all priority-5 tasks together exceed available time."""
        warnings = []
        critical = [t for t in self.owner.get_all_tasks() if t.priority == 5 and t.is_schedulable()]
        critical_total = sum(t.duration for t in critical)

        if critical_total > self.available_time:
            warnings.append(
                f"⚠️ Conflict: Your {len(critical)} critical tasks need {critical_total} min "
                f"but you only have {self.available_time} min. "
                f"Some priority-5 tasks will be dropped."
            )
        return warnings

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        if not self._plan:
            return "No plan generated yet. Call generate_plan() first."

        total = self.get_total_duration()
        lines = [
            f"Plan for {self.owner.name} ({self.available_time} min available):",
            ""
        ]

        for i, task in enumerate(self._plan, 1):
            recur_label = f" 🔁 {task.frequency}" if task.frequency != "none" else ""
            lines.append(
                f"  {i}. {task.name} [{task.category}] — {task.duration} min "
                f"(priority {task.priority}/5){recur_label}"
            )

        lines.append("")
        lines.append(f"Total scheduled: {total} min / {self.available_time} min available")
        lines.append("Tasks ordered by priority. Duration used as tiebreaker (shorter first).")
        return "\n".join(lines)

    def get_total_duration(self) -> int:
        """Return the total duration (minutes) of all tasks in the current plan."""
        return sum(task.duration for task in self._plan)