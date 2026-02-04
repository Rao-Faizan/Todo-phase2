from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from models.message import Message, MessageCreate, MessageUpdate
from models.conversation import Conversation


class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get message by ID"""
        statement = select(Message).where(Message.id == message_id)
        return self.session.exec(statement).first()

    def get_by_conversation(self, conversation_id: UUID, offset: int = 0, limit: int = 100) -> List[Message]:
        """Get all messages for a conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc()).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def get_recent_by_conversation(self, conversation_id: UUID, limit: int = 10) -> List[Message]:
        """Get recent messages for a conversation (for context)"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = self.session.exec(statement).all()
        # Return in chronological order (oldest first)
        return sorted(messages, key=lambda m: m.timestamp)

    def create(self, message_create: MessageCreate) -> Message:
        """Create a new message"""
        message = Message.model_validate(message_create)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def update(self, message_id: UUID, message_update: MessageUpdate) -> Optional[Message]:
        """Update a message"""
        message = self.get_by_id(message_id)
        if message:
            update_data = message_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(message, key, value)
            self.session.add(message)
            self.session.commit()
            self.session.refresh(message)
        return message

    def delete(self, message_id: UUID) -> bool:
        """Delete a message"""
        message = self.get_by_id(message_id)
        if message:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

    def delete_by_conversation(self, conversation_id: UUID) -> int:
        """Delete all messages in a conversation"""
        messages = self.get_by_conversation(conversation_id)
        count = 0
        for message in messages:
            self.session.delete(message)
            count += 1
        self.session.commit()
        return count