from sqlmodel import Session
from models.user import User, UserCreate
from passlib.context import CryptContext
from typing import Optional
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plaintext password"""
    return pwd_context.hash(password)

async def create_user(user_data: UserCreate, session: Session) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Validate password strength (minimum 8 characters)
    if len(user_data.password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Hash the password
    password_hash = get_password_hash(user_data.password)

    # Create the user
    db_user = User(
        email=user_data.email,
        password_hash=password_hash
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

async def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    """Authenticate user by email and password"""
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user