from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Finish writing and review the Q1 project proposal document",
                "completed": False
            }
        }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated project proposal",
                "description": "Revised document based on feedback",
                "completed": True
            }
        }

class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, task: 'Task'):
        return cls(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )