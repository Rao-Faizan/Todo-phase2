import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from backend.services.task_service import create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
from backend.models.task import TaskCreate, TaskUpdate
from backend.models.user import User, UserCreate
from backend.services.auth_service import create_user
from uuid import UUID

# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    from backend.models.user import SQLModel
    from backend.models.task import SQLModel as TaskSQLModel
    # Import SQLModel from both to ensure all models are registered

    # We need to import the base SQLModel from user to register all models
    from backend.models.user import SQLModel as BaseSQLModel
    BaseSQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

def test_create_task_success(session):
    """Test successful task creation"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create a task for the user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.user_id == user.id

def test_get_tasks_for_user(session):
    """Test getting tasks for a specific user"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create another user
    user2_data = UserCreate(email="test2@example.com", password="password123")
    user2 = create_user(user2_data, session)

    # Create a task for the first user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    # Create a task for the second user
    task2_data = TaskCreate(title="Test Task 2", description="Test Description 2", completed=True)
    task2 = create_task(user2.id, task2_data, session)

    # Get tasks for first user
    user_tasks = get_tasks(user.id, session)
    assert len(user_tasks) == 1
    assert user_tasks[0].id == task.id

    # Get tasks for second user
    user2_tasks = get_tasks(user2.id, session)
    assert len(user2_tasks) == 1
    assert user2_tasks[0].id == task2.id

def test_get_specific_task(session):
    """Test getting a specific task"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create a task for the user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    # Get the specific task
    retrieved_task = get_task(user.id, task.id, session)
    assert retrieved_task is not None
    assert retrieved_task.id == task.id
    assert retrieved_task.title == "Test Task"

def test_update_task(session):
    """Test updating a task"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create a task for the user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    # Update the task
    update_data = TaskUpdate(title="Updated Task", completed=True)
    updated_task = update_task(user.id, task.id, update_data, session)

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.completed == True

def test_delete_task(session):
    """Test deleting a task"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create a task for the user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    # Verify task exists
    retrieved_task = get_task(user.id, task.id, session)
    assert retrieved_task is not None

    # Delete the task
    delete_result = delete_task(user.id, task.id, session)
    assert delete_result == True

    # Verify task is deleted
    retrieved_task = get_task(user.id, task.id, session)
    assert retrieved_task is None

def test_toggle_task_completion(session):
    """Test toggling task completion status"""
    # Create a user first
    user_data = UserCreate(email="test@example.com", password="password123")
    user = create_user(user_data, session)

    # Create a task for the user
    task_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
    task = create_task(user.id, task_data, session)

    # Verify task is initially not completed
    assert task.completed == False

    # Toggle completion to True
    toggled_task = toggle_task_completion(user.id, task.id, True, session)
    assert toggled_task is not None
    assert toggled_task.completed == True

    # Toggle completion to False
    toggled_task = toggle_task_completion(user.id, task.id, False, session)
    assert toggled_task is not None
    assert toggled_task.completed == False