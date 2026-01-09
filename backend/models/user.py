from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Relationship

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(sa_column=Column(pg.VARCHAR(255), unique=True, nullable=False))
    password_hash: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=False))
    created_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(pg.TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(pg.TIMESTAMP(timezone=True)))

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securePassword123!"
            }
        }

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )