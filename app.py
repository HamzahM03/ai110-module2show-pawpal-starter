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

# --- Owner + Pet setup ---
st.subheader("Owner & Pet Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input("Time available today (minutes)", min_value=10, max_value=480, value=90)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, age=0)
    owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.tasks = []
    st.success(f"Saved {owner_name} with pet {pet_name}!")

st.divider()

# --- Task entry ---
st.subheader("Add Tasks")

if st.session_state.owner is None:
    st.info("Save an owner and pet above before adding tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=4)
    with col4:
        category = st.selectbox("Category", ["walk", "feed", "med", "grooming", "enrichment"])

    if st.button("Add Task"):
        owner = st.session_state.owner
        task = Task(name=task_title, duration=int(duration), priority=priority, category=category)
        owner.pets[0].add_task(task)
        st.session_state.tasks.append({
            "Task": task_title,
            "Duration (min)": int(duration),
            "Priority": priority,
            "Category": category
        })
        st.success(f"Added: {task_title}")

    if st.session_state.tasks:
        st.write("Current tasks:")
        st.table(st.session_state.tasks)
    else:
        st.info("No tasks yet.")

st.divider()

# --- Schedule generation ---
st.subheader("Generate Schedule")

if st.button("Generate Schedule"):
    if st.session_state.owner is None:
        st.error("Set up an owner and pet first.")
    elif not st.session_state.tasks:
        st.error("Add at least one task before generating a schedule.")
    else:
        owner = st.session_state.owner
        scheduler = Scheduler(owner)
        plan = scheduler.generate_plan()

        if not plan:
            st.warning("No tasks could be scheduled within the available time.")
        else:
            st.success("Schedule generated!")
            st.markdown("### Today's Plan")
            for i, task in enumerate(plan, 1):
                st.markdown(
                    f"**{i}. {task.name}** — {task.duration} min | "
                    f"Priority {task.priority}/5 | `{task.category}`"
                )
            st.divider()
            st.markdown("### Explanation")
            st.text(scheduler.explain_plan())