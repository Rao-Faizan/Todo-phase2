from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from models.task import Task, TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        statement = select(Task).where(Task.id == task_id)
        return self.session.exec(statement).first()

    def get_by_user(self, user_id: UUID, offset: int = 0, limit: int = 100, status: str = "all") -> List[Task]:
        """Get all tasks for a user with optional status filtering"""
        statement = select(Task).where(Task.user_id == user_id)

        if status != "all":
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)

        statement = statement.offset(offset).limit(limit).order_by(Task.created_at.desc())
        return self.session.exec(statement).all()

    def create(self, user_id: UUID, task_create: TaskCreate) -> Task:
        """Create a new task"""
        task = Task.model_validate(task_create, update={"user_id": user_id, "completed": False})
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        task = self.get_by_id(task_id)
        if task:
            update_data = task_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task, key, value)
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
        return task

    def delete(self, task_id: UUID) -> bool:
        """Delete a task"""
        task = self.get_by_id(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False

    def mark_completed(self, task_id: UUID) -> Optional[Task]:
        """Mark a task as completed"""
        task = self.get_by_id(task_id)
        if task:
            task.completed = True
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
        return task