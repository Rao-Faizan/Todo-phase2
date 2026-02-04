"""Service for managing conversation history"""

from typing import List, Optional
from uuid import UUID
from sqlmodel import Session
from models.conversation import Conversation
from models.message import Message
from ..repositories.conversation_repository import ConversationRepository
from ..repositories.message_repository import MessageRepository


class ConversationHistoryService:
    def __init__(self):
        # Repositories will be initialized with sessions when needed
        self.conversation_repo = None
        self.message_repo = None

    async def get_user_conversations(
        self,
        user_id: UUID,
        session: Session
    ) -> List[Conversation]:
        """Get all conversations for a user"""
        # Initialize repositories with session
        self.conversation_repo = ConversationRepository(session)
        return self.conversation_repo.get_by_user(user_id)

    async def get_conversation_by_id(
        self,
        conversation_id: UUID,
        user_id: UUID,
        session: Session
    ) -> Optional[Conversation]:
        """Get a specific conversation by ID for a user"""
        # Initialize repositories with session
        self.conversation_repo = ConversationRepository(session)
        conversation = self.conversation_repo.get_by_id(conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation
        return None

    async def get_conversation_messages(
        self,
        conversation_id: UUID,
        session: Session
    ) -> List[Message]:
        """Get all messages for a conversation"""
        # Initialize repositories with session
        self.message_repo = MessageRepository(session)
        return self.message_repo.get_by_conversation(conversation_id)

    async def create_new_conversation(
        self,
        user_id: UUID,
        session: Session
    ) -> Conversation:
        """Create a new conversation for a user"""
        # Initialize repositories with session
        self.conversation_repo = ConversationRepository(session)
        from models.conversation import ConversationCreate
        conversation_create_obj = ConversationCreate(user_id=user_id)
        return self.conversation_repo.create(conversation_create_obj)

    async def save_message(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
        session: Session
    ) -> Message:
        """Save a message to a conversation"""
        # Initialize repositories with session
        self.message_repo = MessageRepository(session)
        from models.message import MessageCreate
        message_create_obj = MessageCreate(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        return self.message_repo.create(message_create_obj)


# Global instance
conversation_history_service = ConversationHistoryService()