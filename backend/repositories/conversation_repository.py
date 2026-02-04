from typing import Optional, List
from sqlmodel import Session, select
from uuid import UUID
from models.conversation import Conversation, ConversationCreate, ConversationUpdate
from models.user import User


class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID"""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.session.exec(statement).first()

    def get_by_user(self, user_id: UUID, offset: int = 0, limit: int = 100) -> List[Conversation]:
        """Get all conversations for a user"""
        statement = select(Conversation).where(Conversation.user_id == user_id).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def create(self, conversation_create: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation.model_validate(conversation_create)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def update(self, conversation_id: UUID, conversation_update: ConversationUpdate) -> Optional[Conversation]:
        """Update a conversation"""
        conversation = self.get_by_id(conversation_id)
        if conversation:
            update_data = conversation_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(conversation, key, value)
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation"""
        conversation = self.get_by_id(conversation_id)
        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False

    def get_or_create_by_user_and_title(self, user_id: UUID, title: str) -> Conversation:
        """Get or create a conversation by user and title"""
        statement = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.title == title
        )
        conversation = self.session.exec(statement).first()

        if not conversation:
            conversation = Conversation(user_id=user_id, title=title)
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)

        return conversation