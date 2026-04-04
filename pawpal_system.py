from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: int

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    id: str
    title: str
    pet_id: str
    description: str = ""
    due_date: Optional[date] = None
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass

    def is_overdue(self) -> bool:
        pass


@dataclass
class Owner:
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, task_id: str, updates: dict) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks_for_pet(self, pet_id: str) -> list[Task]:
        pass
