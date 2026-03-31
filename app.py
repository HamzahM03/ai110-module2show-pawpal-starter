import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Page config ---
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart daily care planner for your pet.")

# ------------------------------------------------------------------ #
# SECTION 1: Owner & Pet Setup
# ------------------------------------------------------------------ #
st.subheader("1. Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input(
        "Time available today (minutes)", min_value=10, max_value=480, value=90
    )
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, age=0)
    owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.tasks = []
    st.success(f"Saved! {owner_name} has {available_minutes} min today for {pet_name}.")

st.divider()

# ------------------------------------------------------------------ #
# SECTION 2: Add Tasks
# ------------------------------------------------------------------ #
st.subheader("2. Add Tasks")

if st.session_state.owner is None:
    st.info("Save an owner and pet above before adding tasks.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task name", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=4)
    with col4:
        category = st.selectbox("Category", ["walk", "feed", "med", "grooming", "enrichment"])
    with col5:
        frequency = st.selectbox("Frequency", ["none", "daily", "weekly"])

    if st.button("Add Task"):
        owner = st.session_state.owner
        task = Task(
            name=task_title,
            duration=int(duration),
            priority=priority,
            category=category,
            frequency=frequency,
            recurring=(frequency != "none")
        )
        owner.pets[0].add_task(task)
        st.session_state.tasks.append({
            "Task": task_title,
            "Duration (min)": int(duration),
            "Priority": priority,
            "Category": category,
            "Frequency": frequency
        })
        st.success(f"Added: {task_title}")

    if st.session_state.tasks:
        st.markdown("**Current tasks:**")
        st.table(st.session_state.tasks)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ------------------------------------------------------------------ #
# SECTION 3: Generate Schedule
# ------------------------------------------------------------------ #
st.subheader("3. Generate Schedule")

if st.button("Generate Schedule", type="primary"):
    if st.session_state.owner is None:
        st.error("Set up an owner and pet first.")
    elif not st.session_state.tasks:
        st.error("Add at least one task before generating a schedule.")
    else:
        owner = st.session_state.owner
        scheduler = Scheduler(owner)

        # --- Conflict detection ---
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        
        # --- Generate plan ---
        plan = scheduler.generate_plan()

        if not plan:
            st.error("No tasks could be scheduled within the available time.")
        else:
            st.success(f"Schedule ready! {scheduler.get_total_duration()} / {owner.get_available_time()} min used.")

            st.markdown("### 📋 Today's Plan")
            for i, task in enumerate(plan, 1):
                recur_badge = f" 🔁 {task.frequency}" if task.frequency != "none" else ""
                st.markdown(
                    f"**{i}. {task.name}**{recur_badge}  \n"
                    f"`{task.category}` · {task.duration} min · Priority {task.priority}/5"
                )

            st.divider()

            # --- Skipped tasks ---
            all_schedulable = [t for t in owner.get_all_tasks() if t.is_schedulable()]
            skipped = [t for t in all_schedulable if t not in plan]
            if skipped:
                st.markdown("### ⏭️ Skipped Tasks")
                st.caption("These tasks didn't fit within your available time.")
                for task in skipped:
                    st.markdown(
                        f"- **{task.name}** — {task.duration} min (priority {task.priority}/5)"
                    )

            st.divider()

            # --- Explanation ---
            st.markdown("### 💡 Why this plan?")
            st.text(scheduler.explain_plan())

            # --- Filter: incomplete tasks ---
            st.divider()
            st.markdown("### 🔍 All Incomplete Tasks")
            incomplete = owner.get_incomplete_tasks()
            if incomplete:
                st.table([{
                    "Task": t.name,
                    "Category": t.category,
                    "Duration (min)": t.duration,
                    "Priority": t.priority,
                    "Due": str(t.due_date)
                } for t in incomplete])
            else:
                st.success("All tasks are complete!")