from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# --- existing tests ---

def test_mark_complete_changes_status():
    task = Task(name="Morning walk", duration=30, priority=5, category="walk")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Rex", species="Dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Feed breakfast", duration=10, priority=4, category="feed"))
    assert len(pet.get_tasks()) == 1


# --- new tests ---

def test_generate_plan_respects_available_time():
    owner = Owner(name="Marcus", available_minutes=30)
    dog = Pet(name="Rex", species="Dog", age=3)
    dog.add_task(Task(name="Long walk",      duration=25, priority=5, category="walk"))
    dog.add_task(Task(name="Feed breakfast", duration=10, priority=4, category="feed"))
    owner.add_pet(dog)

    plan = Scheduler(owner).generate_plan()
    total = sum(t.duration for t in plan)
    assert total <= 30


def test_generate_plan_sorts_by_priority():
    owner = Owner(name="Marcus", available_minutes=60)
    dog = Pet(name="Rex", species="Dog", age=3)
    dog.add_task(Task(name="Playtime",       duration=10, priority=1, category="enrichment"))
    dog.add_task(Task(name="Give medication",duration=10, priority=5, category="med"))
    dog.add_task(Task(name="Brush coat",     duration=10, priority=3, category="grooming"))
    owner.add_pet(dog)

    plan = Scheduler(owner).generate_plan()
    priorities = [t.priority for t in plan]
    assert priorities == sorted(priorities, reverse=True)


def test_no_tasks_returns_empty_plan():
    owner = Owner(name="Marcus", available_minutes=60)
    owner.add_pet(Pet(name="Rex", species="Dog", age=3))

    plan = Scheduler(owner).generate_plan()
    assert plan == []


def test_daily_recurring_resets_after_complete():
    task = Task(name="Feed breakfast", duration=10, priority=5,
                category="feed", frequency="daily")
    task.mark_complete()

    assert task.completed is False
    assert task.due_date == date.today() + timedelta(days=1)


def test_conflict_detection_warns_when_critical_tasks_overflow():
    owner = Owner(name="Marcus", available_minutes=20)
    dog = Pet(name="Rex", species="Dog", age=3)
    dog.add_task(Task(name="Walk",      duration=15, priority=5, category="walk"))
    dog.add_task(Task(name="Medication",duration=10, priority=5, category="med"))
    owner.add_pet(dog)

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) > 0
    assert "Conflict" in warnings[0]