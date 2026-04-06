import streamlit as st
import pawpal_system


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_breed = st.text_input("Breed", value="Unknown")
pet_age = st.number_input("Age", min_value=0, max_value=50, value=3)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = pawpal_system.Owner(name=owner_name, email='something@gmail.com', pets=[], tasks=st.session_state.tasks)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.button("Add Pet"):
    petId = str(len(st.session_state.owner.pets) + 1)
    pet = pawpal_system.Pet(id=petId, name=pet_name, species=species, breed=pet_breed, age=pet_age)
    st.session_state.owner.add_pet(pet)

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    
    scheduler = pawpal_system.Scheduler(owner=st.session_state.owner)

    st.markdown("### Pending Tasks")
    for task in scheduler.get_pending_tasks():
        st.write(f"- [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

    st.markdown("### Overdue Tasks")
    for task in scheduler.get_overdue_tasks():
        st.write(f"- [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

    st.markdown("### Upcoming Tasks (next 7 days)")
    for task in scheduler.get_upcoming_tasks(days_ahead=7):
        st.write(f"- [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
