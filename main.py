from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

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
for task in scheduler.get_all_tasks():
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