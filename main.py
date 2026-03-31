from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Marcus", available_minutes=90)

dog = Pet(name="Rex", species="Dog", age=3)
cat = Pet(name="Luna", species="Cat", age=5)

dog.add_task(Task(name="Morning walk",      duration=30, priority=5, category="walk", recurring=True))
dog.add_task(Task(name="Feed breakfast",    duration=10, priority=5, category="feed", recurring=True))
dog.add_task(Task(name="Enrichment puzzle", duration=20, priority=2, category="enrichment"))

cat.add_task(Task(name="Give medication",   duration=5,  priority=5, category="med", recurring=True))
cat.add_task(Task(name="Brush coat",        duration=15, priority=3, category="grooming"))
cat.add_task(Task(name="Playtime",          duration=20, priority=2, category="enrichment"))

owner.add_pet(dog)
owner.add_pet(cat)

# --- Conflict detection ---
scheduler = Scheduler(owner)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
    print()

# --- Schedule ---
scheduler.generate_plan()
print("=" * 45)
print("         🐾  TODAY'S SCHEDULE  🐾")
print("=" * 45)
print(scheduler.explain_plan())
print("=" * 45)

# --- Filter demos ---
print("\n📋 Rex's tasks only:")
for t in owner.get_tasks_by_pet("Rex"):
    print(f"  - {t.name} (priority {t.priority})")

print("\n✅ Incomplete tasks across all pets:")
for t in owner.get_incomplete_tasks():
    print(f"  - {t.name} [{t.category}]")

# --- Recurring reset demo ---
print("\n🔁 Marking all tasks complete, then resetting recurring ones...")
for t in owner.get_all_tasks():
    t.mark_complete()
owner.reset_day()

print("Incomplete after reset (should only be recurring tasks):")
for t in owner.get_incomplete_tasks():
    print(f"  - {t.name}")