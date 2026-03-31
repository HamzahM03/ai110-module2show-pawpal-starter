from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int          # minutes
    priority: int          # 1 (low) to 5 (high)
    category: str          # "walk" | "feed" | "med" | "grooming" | "enrichment"
    completed: bool = False

    def __post_init__(self):
        if not (1 <= self.priority <= 5):
            raise ValueError(f"Priority must be 1–5, got {self.priority}")
        if self.duration <= 0:
            raise ValueError(f"Duration must be positive, got {self.duration}")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_schedulable(self) -> bool:
        """Return True if this task hasn't been completed yet."""
        return not self.completed


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


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.available_time = owner.get_available_time()
        self._plan: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """
        Build a daily plan by sorting all schedulable tasks by priority (high first),
        then greedily adding tasks until available_time is exhausted.
        """
        all_tasks = self.owner.get_all_tasks()
        schedulable = [t for t in all_tasks if t.is_schedulable()]

        # Sort by priority descending (5 = highest)
        schedulable.sort(key=lambda t: t.priority, reverse=True)

        plan = []
        time_remaining = self.available_time

        for task in schedulable:
            if task.duration <= time_remaining:
                plan.append(task)
                time_remaining -= task.duration

        self._plan = plan
        return self._plan

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
            lines.append(
                f"  {i}. {task.name} [{task.category}] — {task.duration} min "
                f"(priority {task.priority}/5)"
            )

        lines.append("")
        lines.append(f"Total scheduled: {total} min / {self.available_time} min available")
        lines.append("Tasks are ordered by priority. Lower-priority tasks were dropped if time ran out.")
        return "\n".join(lines)

    def get_total_duration(self) -> int:
        """Return the total duration (minutes) of all tasks in the current plan."""
        return sum(task.duration for task in self._plan)