from sqlmodel import create_engine, Session
from typing import Generator
from models.user import User
from models.task import Task
import os
from dotenv import load_dotenv

load_dotenv()

# Use in-memory database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, echo=False)

def create_test_db_and_tables():
    """Create test database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_test_session():
    """Get test database session"""
    with Session(engine) as session:
        return session

def get_test_session_generator():
    """Get test database session generator for FastAPI dependency"""
    with Session(engine) as session:
        yield session