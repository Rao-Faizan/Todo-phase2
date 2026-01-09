import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from backend.services.auth_service import create_user, authenticate_user
from backend.models.user import UserCreate
from backend.database import get_session

# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session

def test_create_user_success(session):
    """Test successful user creation"""
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    assert user.email == "test@example.com"
    assert user.id is not None

def test_create_duplicate_user_fails(session):
    """Test that creating a duplicate user fails"""
    user_data = UserCreate(email="test@example.com", password="password123")

    # Create the first user
    create_user(user_data, session)

    # Try to create a user with the same email
    with pytest.raises(ValueError, match="Email already registered"):
        create_user(user_data, session)

def test_authenticate_user_success(session):
    """Test successful user authentication"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    created_user = create_user(user_data, session)

    # Authenticate the user
    authenticated_user = authenticate_user("test@example.com", "password123", session)

    assert authenticated_user is not None
    assert authenticated_user.id == created_user.id

def test_authenticate_user_wrong_password(session):
    """Test authentication with wrong password"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    create_user(user_data, session)

    # Try to authenticate with wrong password
    authenticated_user = authenticate_user("test@example.com", "wrongpassword", session)

    assert authenticated_user is None

def test_authenticate_nonexistent_user(session):
    """Test authentication with nonexistent user"""
    authenticated_user = authenticate_user("nonexistent@example.com", "password123", session)

    assert authenticated_user is None