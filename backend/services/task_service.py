from sqlmodel import Session
from models.task import Task, TaskCreate, TaskUpdate
from typing import List, Optional
from uuid import UUID

async def create_task(user_id: UUID, task_data: TaskCreate, session: Session) -> Task:
    """Create a new task for a user"""
    db_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

async def get_tasks(user_id: UUID, session: Session) -> List[Task]:
    """Get all tasks for a user"""
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    return tasks

async def get_task(user_id: UUID, task_id: UUID, session: Session) -> Optional[Task]:
    """Get a specific task for a user"""
    task = session.query(Task).filter(Task.user_id == user_id, Task.id == task_id).first()
    return task

async def update_task(user_id: UUID, task_id: UUID, task_data: TaskUpdate, session: Session) -> Optional[Task]:
    """Update a specific task for a user"""
    task = await get_task(user_id, task_id, session)
    if not task:
        return None

    # Update fields if they are provided
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

async def delete_task(user_id: UUID, task_id: UUID, session: Session) -> bool:
    """Delete a specific task for a user"""
    task = await get_task(user_id, task_id, session)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

async def toggle_task_completion(user_id: UUID, task_id: UUID, completed: bool, session: Session) -> Optional[Task]:
    """Toggle completion status of a task for a user"""
    task = await get_task(user_id, task_id, session)
    if not task:
        return None

    task.completed = completed
    session.add(task)
    session.commit()
    session.refresh(task)

    return task