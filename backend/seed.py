import asyncio
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
from database import engine
from models.user import User
from models.conversation import Conversation
from models.message import Message
from models.task import Task


def create_seed_data():
    """Create seed data for initial testing"""
    with Session(engine) as session:
        # Check if seed data already exists
        user_exists = session.exec(select(User).limit(1)).first()
        if user_exists:
            print("Seed data already exists, skipping...")
            return

        # Create a test user
        test_user = User(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            password_hash="$2b$12$VcCDgh2NDk07Jj9WvYWNNOZFnTLvqkHy/U8Nt5a4IjeCT5VsYNF/W"  # bcrypt hash for "password"
        )
        session.add(test_user)

        # Create a conversation
        conversation = Conversation(
            id="123e4567-e89b-12d3-a456-426614174001",
            title="Initial Test Conversation",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)

        # Create a test task
        test_task = Task(
            id="123e4567-e89b-12d3-a456-426614174002",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            title="Sample Task",
            description="This is a sample task for testing",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(test_task)

        # Create messages
        user_message = Message(
            id="123e4567-e89b-12d3-a456-426614174003",
            conversation_id="123e4567-e89b-12d3-a456-426614174001",
            role="user",
            content="Can you help me add a new task?",
            timestamp=datetime.utcnow()
        )
        session.add(user_message)

        assistant_message = Message(
            id="123e4567-e89b-12d3-a456-426614174004",
            conversation_id="123e4567-e89b-12d3-a456-426614174001",
            role="assistant",
            content="Sure! What would you like to add?",
            timestamp=datetime.utcnow()
        )
        session.add(assistant_message)

        # Commit all changes
        session.commit()
        print("Seed data created successfully!")


if __name__ == "__main__":
    create_seed_data()