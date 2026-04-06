from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date
'''
owner1 = Owner(name="Jordan", email="something@gmail.com", pets=[], tasks=[])

pet1 = Pet(id="100", name="Mochi", species="cat", breed="Siamese", age=3)
pet2 = Pet(id="123", name="Buddy", species="dog", breed="Labrador", age=5)

owner1.add_pet(pet1)
owner1.add_pet(pet2)    

owner1.add_task(Task(id="t1", title="Morning walk", pet_id=pet2.id, description="Take Buddy for a walk in the park", due_date=date(2026, 4, 4), priority="high"))
owner1.add_task(Task(id="t1", title="Vet appointment", pet_id=pet2.id, description="Take Buddy to the vet", due_date=date(2026, 4, 5), priority="medium"))

owner1.add_task(Task(id="t2", title="Morning walk", pet_id=pet1.id, description="Take Mochi on a walk", due_date=date(2026, 3, 5), priority="low"))
owner1.add_task(Task(id="t2", title="Feed Mochi", pet_id=pet1.id, description="Feed Mochi her breakfast", due_date=date(2026, 5, 8), priority="medium"))
owner1.add_task(Task(id="t3", title="Vet appointment", pet_id=pet1.id, description="Take Mochi to the vet for her annual checkup", due_date=date(2026, 4, 7), priority="high"))

print(pet1.get_info())
print(pet2.get_info())

scheduler = Scheduler(owner=owner1)
print("All tasks:")

for task in scheduler.sort_by_time():
    print(f"- {task.title} Pet Name: {owner1.get_pet_info(task.pet_id).name}, Due: {task.due_date}, Priority: {task.priority}")

print("\n=== Pending Tasks ===")
for task in scheduler.get_pending_tasks():
    print(f"  [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

print("\n=== Overdue Tasks ===")
for task in scheduler.get_overdue_tasks():
    print(f"  [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

print("\n=== Tasks by Pet ===")
for pet_id, tasks in scheduler.get_tasks_by_pet().items():
    pet = owner1.get_pet_info(pet_id)
    print(f"  {pet.name}:")
    for task in tasks:
        print(f"    - [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

print("\n=== Upcoming Tasks (next 1 day) ===")
for task in scheduler.get_upcoming_tasks(days_ahead=1):
    print(f"  [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

print("\n=== Filter: Incomplete tasks for Mochi ===")
for task in scheduler.filter_tasks(is_completed=False, pet_name="Mochi"):
    print(f"  [{task.priority.upper()}] {task.title} | Due: {task.due_date}")

print("\n=== Filter: All tasks for Buddy ===")
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  [{task.priority.upper()}] {task.title} | Due: {task.due_date}")
'''
# --- Conflict Detection Tests ---
owner2 = Owner(name="Alex", email="alex@gmail.com", pets=[], tasks=[])
pet3 = Pet(id="200", name="Luna", species="dog", breed="Poodle", age=2)
pet4 = Pet(id="201", name="Pepper", species="cat", breed="Persian", age=4)
owner2.add_pet(pet3)
owner2.add_pet(pet4)

# Overlapping: both tasks on same day, Luna 08:00-08:30, Pepper 08:20-08:50 → conflict
owner2.add_task(Task(id="c1", title="Morning walk", pet_id=pet3.id, due_date=date(2026, 4, 10), start_time="08:00", duration_minutes=30))
owner2.add_task(Task(id="c2", title="Feeding time", pet_id=pet4.id, due_date=date(2026, 4, 10), start_time="08:20", duration_minutes=30))
# Non-overlapping: Luna 09:00-09:30, Pepper 09:30-10:00 → no conflict
owner2.add_task(Task(id="c3", title="Grooming",     pet_id=pet3.id, due_date=date(2026, 4, 10), start_time="09:00", duration_minutes=30))
owner2.add_task(Task(id="c4", title="Playtime",     pet_id=pet4.id, due_date=date(2026, 4, 10), start_time="09:30", duration_minutes=30))

scheduler2 = Scheduler(owner=owner2)

print("\n=== Conflict Detection ===")
conflicts = scheduler2.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts detected.")

# --- Recurrence Tests ---
owner3 = Owner(name="Sam", email="sam@gmail.com", pets=[], tasks=[])
pet5 = Pet(id="300", name="Biscuit", species="dog", breed="Beagle", age=1)
owner3.add_pet(pet5)

owner3.add_task(Task(id="r1", title="Daily walk",   pet_id=pet5.id, due_date=date(2026, 4, 5), recurrence="daily",  priority="high"))
owner3.add_task(Task(id="r2", title="Weekly bath",  pet_id=pet5.id, due_date=date(2026, 4, 5), recurrence="weekly", priority="medium"))
owner3.add_task(Task(id="r3", title="One-time vet", pet_id=pet5.id, due_date=date(2026, 4, 5), recurrence=None,     priority="low"))

scheduler3 = Scheduler(owner=owner3)

print("\n=== Recurrence: Complete daily task (expect next day scheduled) ===")
next_task = scheduler3.complete_task("r1")
print(f"  Next occurrence: '{next_task.title}' due {next_task.due_date}" if next_task else "  No next occurrence.")

print("\n=== Recurrence: Complete weekly task (expect next week scheduled) ===")
next_task = scheduler3.complete_task("r2")
print(f"  Next occurrence: '{next_task.title}' due {next_task.due_date}" if next_task else "  No next occurrence.")

print("\n=== Recurrence: Complete one-time task (expect no next occurrence) ===")
next_task = scheduler3.complete_task("r3")
print(f"  Next occurrence: '{next_task.title}' due {next_task.due_date}" if next_task else "  No next occurrence.")