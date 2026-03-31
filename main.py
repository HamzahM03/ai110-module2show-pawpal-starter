from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Marcus", available_minutes=90)

dog = Pet(name="Rex", species="Dog", age=3)
cat = Pet(name="Luna", species="Cat", age=5)

# --- Tasks for Rex ---
dog.add_task(Task(name="Morning walk",       duration=30, priority=5, category="walk"))
dog.add_task(Task(name="Feed breakfast",     duration=10, priority=5, category="feed"))
dog.add_task(Task(name="Enrichment puzzle",  duration=20, priority=2, category="enrichment"))

# --- Tasks for Luna ---
cat.add_task(Task(name="Give medication",    duration=5,  priority=5, category="med"))
cat.add_task(Task(name="Brush coat",         duration=15, priority=3, category="grooming"))
cat.add_task(Task(name="Playtime",           duration=20, priority=2, category="enrichment"))

owner.add_pet(dog)
owner.add_pet(cat)

# --- Schedule ---
scheduler = Scheduler(owner)
scheduler.generate_plan()

print("=" * 45)
print("         🐾  TODAY'S SCHEDULE  🐾")
print("=" * 45)
print(scheduler.explain_plan())
print("=" * 45)