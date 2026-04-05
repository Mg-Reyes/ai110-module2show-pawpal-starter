from pawpal_system import Owner, Task
from datetime import date

def test_mark_complete_changes_status():
    task = Task(id="t1", title="Walk Buddy", description= "First task", due_date=date.today(), is_completed=False, priority='high')
    task.mark_complete()
    assert task.is_completed == True


def test_add_task_increases_count():
    owner = Owner(name="Jordan", email="jordan@example.com")
    task = Task(id="task1", title="Walk Mochi", description= "Initial task", due_date=date.today(), is_completed=False, priority='low')
    owner.add_task(task)
    assert len(owner.tasks) == 1
