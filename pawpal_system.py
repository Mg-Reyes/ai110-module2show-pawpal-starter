from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: int

    # Method to return a string with the pet's information
    def get_info(self) -> str:
        return f"{self.name} is a {self.age}-year-old {self.breed} {self.species}."


@dataclass
class Task:
    id: str
    title: str
    pet_id: Optional[str] = None
    description: str = ""
    due_date: Optional[date] = None
    is_completed: bool = False
    priority: str = "medium"  # default to medium

    # Method to set priority with validation
    def set_priority(self, priority: str) -> None:
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be 'low', 'medium', or 'high'.")
        self.priority = priority

    # Method to mark task as completed
    def mark_complete(self) -> None:
        self.is_completed = True

    # Method to check if task is overdue
    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return date.today() > self.due_date


@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    # add check for duplicates 
    def add_pet(self, pet: Pet) -> None:
        # check if pet with same id already exists
        for existing_pet in self.pets:
            if existing_pet.id == pet.id:
                raise ValueError(f"Pet with id {pet.id} already exists.")
            
        # add the pet to the owner's list of pets
        self.pets.append(pet)

    # remove the pet and unassign any tasks associated with that pet
    def remove_pet(self, pet_id: str) -> None:
        # remove the pet with the given id
        for pet in self.pets:
            if pet.id == pet_id:
                self.pets.remove(pet)
                break

        # unassign tasks associated with the removed pet
        for task in self.tasks:
            if task.pet_id == pet_id:
                task.pet_id = None  # unassign tasks from the removed pet
        
    # add a task to the owner's list of tasks
    def add_task(self, task: Task) -> None:
        if task.pet_id is not None:
            # check if the pet_id exists in the owner's list of pets
            if not any(pet.id == task.pet_id for pet in self.pets):
                raise ValueError(f"Pet with id {task.pet_id} does not exist.")
            
        self.tasks.append(task)

    # edit a task's attributes based on the provided updates dictionary
    def edit_task(self, task_id: str, updates: dict) -> None:
        for task in self.tasks:
            if task.id == task_id:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                    else:
                        raise ValueError(f"Task does not have attribute '{key}'.")
                return
        raise ValueError(f"Task with id {task_id} does not exist.")

    # remove a task from the owner's list of tasks based on the provided task_id
    def remove_task(self, task_id: str) -> None:
        if task_id in [task.id for task in self.tasks]:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        else:
            raise ValueError(f"Task with id {task_id} does not exist.")

    # get all tasks associated with a specific pet based on the provided pet_id
    def get_tasks_for_pet(self, pet_id: str) -> list[Task]:
        if pet_id is None:
            raise ValueError("Pet ID cannot be None.")
        
        if pet_id not in [pet.id for pet in self.pets]:
            raise ValueError(f"Pet with id {pet_id} does not exist.")
        
        lst = [task for task in self.tasks if task.pet_id == pet_id]
        return lst

    # get pet based on the provided pet_id
    def get_pet_info(self, pet_id: str) -> Pet:
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        raise ValueError(f"Pet with id {pet_id} does not exist.")


@dataclass
class Scheduler:
    owner: Owner

    # Methods to retrieve tasks based on different criteria
    def get_all_tasks(self) -> list[Task]:
        return self.owner.tasks

    # Method to get tasks that are not completed
    def get_pending_tasks(self) -> list[Task]:
        return [task for task in self.owner.tasks if not task.is_completed]

    # Method to get tasks that are overdue
    def get_overdue_tasks(self) -> list[Task]:
        return [task for task in self.owner.tasks if task.is_overdue() and not task.is_completed]

    # Method to get tasks grouped by pet
    def get_tasks_by_pet(self) -> dict[str, list[Task]]:
        pet_tasks = {pet.id: [] for pet in self.owner.pets}
        for task in self.owner.tasks:
            if task.pet_id in pet_tasks:
                pet_tasks[task.pet_id].append(task)
        return pet_tasks

    # Method to get upcoming tasks within a certain number of days
    def get_upcoming_tasks(self, days_ahead: int) -> list[Task]:
        today = date.today()
        upcoming_tasks = []
        for task in self.owner.tasks:
            if task.due_date and today <= task.due_date <= today + timedelta(days=days_ahead):
                upcoming_tasks.append(task)
        return upcoming_tasks
