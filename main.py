from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup with intentional conflict ---
owner = Owner(name="Marcus", available_minutes=40)  # tight on time

dog = Pet(name="Rex", species="Dog", age=3)

# These three priority-5 tasks = 50 min total, but owner only has 40
dog.add_task(Task(name="Morning walk",   duration=20, priority=5, category="walk",     frequency="daily"))
dog.add_task(Task(name="Feed breakfast", duration=20, priority=5, category="feed",     frequency="daily"))
dog.add_task(Task(name="Give medication",duration=10, priority=5, category="med",      frequency="daily"))
dog.add_task(Task(name="Brush coat",     duration=15, priority=3, category="grooming", frequency="weekly"))

owner.add_pet(dog)

scheduler = Scheduler(owner)

# --- Conflict check first ---
print("🔍 Checking for conflicts...")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("✅ No conflicts detected.")

print()

# --- Generate and display plan ---
scheduler.generate_plan()
print("=" * 45)
print("         🐾  TODAY'S SCHEDULE  🐾")
print("=" * 45)
print(scheduler.explain_plan())
print("=" * 45)