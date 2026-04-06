from pawpal_system import Owner, Task, Scheduler
from datetime import date, timedelta

def test_mark_complete_changes_status():
    task = Task(id="t1", title="Walk Buddy", description= "First task", due_date=date.today(), is_completed=False, priority='high')
    task.mark_complete()
    assert task.is_completed == True


def test_add_task_increases_count():
    owner = Owner(name="Jordan", email="jordan@example.com")
    task = Task(id="task1", title="Walk Mochi", description= "Initial task", due_date=date.today(), is_completed=False, priority='low')
    owner.add_task(task)
    assert len(owner.tasks) == 1


# --- Sorting Tests ---

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_later = Task(id="t3", title="Vet Visit", due_date=today + timedelta(days=5))
    task_soon = Task(id="t2", title="Feed Cat", due_date=today + timedelta(days=1))
    task_today = Task(id="t1", title="Walk Dog", due_date=today)
    owner.add_task(task_later)
    owner.add_task(task_soon)
    owner.add_task(task_today)
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].id == "t1"
    assert sorted_tasks[1].id == "t2"
    assert sorted_tasks[2].id == "t3"


def test_sort_by_time_tasks_without_due_date_go_last():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_no_date = Task(id="t1", title="Groom Dog", due_date=None)
    task_with_date = Task(id="t2", title="Walk Dog", due_date=today)
    owner.add_task(task_no_date)
    owner.add_task(task_with_date)
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].id == "t2"
    assert sorted_tasks[1].id == "t1"


# --- Recurrence Tests ---

def test_complete_daily_task_creates_next_day_task():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task = Task(id="feed-1", title="Feed Cat", due_date=today, recurrence="daily")
    owner.add_task(task)
    scheduler = Scheduler(owner=owner)

    next_task = scheduler.complete_task("feed-1")

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.recurrence == "daily"
    assert next_task.is_completed == False


def test_complete_daily_task_adds_new_task_to_owner():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task = Task(id="feed-1", title="Feed Cat", due_date=today, recurrence="daily")
    owner.add_task(task)
    scheduler = Scheduler(owner=owner)

    scheduler.complete_task("feed-1")

    assert len(owner.tasks) == 2
    assert owner.tasks[0].is_completed == True
    assert owner.tasks[1].is_completed == False


def test_complete_non_recurring_task_creates_no_new_task():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task = Task(id="t1", title="One-time Vet Visit", due_date=today, recurrence=None)
    owner.add_task(task)
    scheduler = Scheduler(owner=owner)

    result = scheduler.complete_task("t1")

    assert result is None
    assert len(owner.tasks) == 1


# --- Conflict Detection Tests ---

def test_detect_conflicts_flags_overlapping_tasks():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_a = Task(id="t1", title="Walk Dog", due_date=today, start_time="09:00", duration_minutes=60)
    task_b = Task(id="t2", title="Feed Cat", due_date=today, start_time="09:30", duration_minutes=30)
    owner.add_task(task_a)
    owner.add_task(task_b)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk Dog" in warnings[0]
    assert "Feed Cat" in warnings[0]


def test_detect_conflicts_no_warning_for_sequential_tasks():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_a = Task(id="t1", title="Walk Dog", due_date=today, start_time="09:00", duration_minutes=30)
    task_b = Task(id="t2", title="Feed Cat", due_date=today, start_time="09:30", duration_minutes=30)
    owner.add_task(task_a)
    owner.add_task(task_b)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 0


def test_detect_conflicts_ignores_different_days():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_a = Task(id="t1", title="Walk Dog", due_date=today, start_time="09:00", duration_minutes=60)
    task_b = Task(id="t2", title="Walk Dog Again", due_date=today + timedelta(days=1), start_time="09:00", duration_minutes=60)
    owner.add_task(task_a)
    owner.add_task(task_b)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 0


def test_detect_conflicts_ignores_completed_tasks():
    owner = Owner(name="Jordan", email="jordan@example.com")
    today = date.today()
    task_a = Task(id="t1", title="Walk Dog", due_date=today, start_time="09:00", duration_minutes=60, is_completed=True)
    task_b = Task(id="t2", title="Feed Cat", due_date=today, start_time="09:15", duration_minutes=30)
    owner.add_task(task_a)
    owner.add_task(task_b)
    scheduler = Scheduler(owner=owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 0
