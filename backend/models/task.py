from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String, DateTime, Text
from sqlmodel import Relationship
from .user import User

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[str] = None
    priority: Optional[str] = "medium"

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    title: str = Field(sa_column=Column(String(200), nullable=False))
    description: Optional[str] = Field(sa_column=Column(Text))
    completed: bool = Field(default=False)
    due_date: Optional[str] = Field(sa_column=Column(String(50), nullable=True))
    priority: Optional[str] = Field(default="medium", sa_column=Column(String(20), nullable=True))
    created_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(DateTime))
    updated_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(DateTime))

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

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

class TaskUpdate(SQLModel):
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
    due_date: Optional[str]
    priority: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, task: Task):
        return cls(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date,
            priority=task.priority,
            created_at=task.created_at,
            updated_at=task.updated_at
        )