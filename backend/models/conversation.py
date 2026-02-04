from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String, DateTime
from .user import User


class ConversationBase(SQLModel):
    title: Optional[str] = None
    user_id: UUID


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: Optional[str] = Field(sa_column=Column(String(200), nullable=True))
    user_id: UUID = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False, index=True)  # Add index for performance
    created_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(DateTime, index=True))  # Add index for performance
    updated_at: datetime = Field(default=datetime.utcnow(), sa_column=Column(DateTime))

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="conversations")
    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", cascade_delete=True)


class ConversationCreate(ConversationBase):
    title: Optional[str] = None
    user_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Todo Discussion",
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class ConversationUpdate(SQLModel):
    title: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Conversation Title"
            }
        }


class ConversationResponse(SQLModel):
    id: UUID
    title: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, conversation: "Conversation"):
        return cls(
            id=conversation.id,
            title=conversation.title,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )