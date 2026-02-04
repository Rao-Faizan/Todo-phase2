from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import String, DateTime, Text
from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: UUID
    role: str  # 'user' or 'assistant' or 'system'
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", ondelete="CASCADE", nullable=False, index=True)  # Add index for performance
    role: str = Field(sa_column=Column(String(20), nullable=False, index=True))  # 'user' or 'assistant' or 'system', add index for filtering
    content: str = Field(sa_column=Column(Text, nullable=False))
    timestamp: datetime = Field(default=datetime.utcnow(), sa_column=Column(DateTime, index=True))  # Add index for ordering/filtering
    tool_calls: Optional[str] = Field(sa_column=Column(Text, nullable=True))  # Store tool calls as JSON string
    tool_responses: Optional[str] = Field(sa_column=Column(Text, nullable=True))  # Store tool responses as JSON string

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    conversation_id: UUID
    role: str
    content: str
    tool_calls: Optional[str] = None
    tool_responses: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "user",
                "content": "Add a new task to buy groceries",
                "tool_calls": None,
                "tool_responses": None
            }
        }


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    tool_calls: Optional[str] = None
    tool_responses: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Updated message content",
                "tool_calls": '{"tool_name": "add_task", "params": {...}}',
                "tool_responses": '{"result": "success", "task_id": "..."}'
            }
        }


class MessageResponse(SQLModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    timestamp: datetime
    tool_calls: Optional[str]
    tool_responses: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, message: "Message"):
        return cls(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp,
            tool_calls=message.tool_calls,
            tool_responses=message.tool_responses
        )