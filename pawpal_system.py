from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    name: str
    duration: int          # minutes
    priority: int          # 1 (low) to 5 (high)
    category: str          # "walk" | "feed" | "med" | "grooming" | "enrichment"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def is_schedulable(self) -> bool:
        """Return True if this task can still be added to a plan."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks associated with this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: list[str] = field(default_factory=list)  # e.g. ["morning walks"]
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        pass

    def get_available_time(self) -> int:
        """Return how many minutes the owner has available today."""
        pass


class Scheduler:
    def __init__(self, pet: Pet, available_time: int):
        self.pet = pet
        self.available_time = available_time
        self.task_list: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """Build and return an ordered list of tasks that fit within available_time."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why the plan was scheduled this way."""
        pass

    def get_total_duration(self) -> int:
        """Return the total duration (minutes) of all tasks currently in task_list."""
        pass