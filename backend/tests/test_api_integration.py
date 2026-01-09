import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from backend.main import app
from backend.database import get_session
from backend.models.user import User
from backend.models.task import Task
from backend.services.auth_service import get_password_hash

# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    from backend.models.user import SQLModel as UserSQLModel
    from backend.models.task import SQLModel as TaskSQLModel
    # Import SQLModel from both to ensure all models are registered
    UserSQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_signup_endpoint(client: TestClient):
    """Test the signup endpoint"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

def test_signin_endpoint(client: TestClient, session: Session):
    """Test the signin endpoint"""
    # First create a user
    from backend.models.user import UserCreate
    from backend.services.auth_service import create_user

    user_data = UserCreate(email="testsignin@example.com", password="password123")
    user = create_user(user_data, session)

    # Now try to sign in
    response = client.post(
        "/api/auth/signin",
        json={"email": "testsignin@example.com", "password": "password123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == "testsignin@example.com"

def test_tasks_crud_operations(client: TestClient, session: Session):
    """Test CRUD operations for tasks"""
    # First create a user and get a token
    signup_response = client.post(
        "/api/auth/signup",
        json={"email": "tasktest@example.com", "password": "password123"}
    )

    assert signup_response.status_code == 200
    token = signup_response.json()["token"]
    user_id = signup_response.json()["user"]["id"]

    # Set up authorization header
    headers = {"Authorization": f"Bearer {token}"}

    # Test creating a task
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers
    )

    assert create_response.status_code == 200
    created_task = create_response.json()["task"]
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "Test Description"
    task_id = created_task["id"]

    # Test getting all tasks
    get_all_response = client.get(f"/api/{user_id}/tasks", headers=headers)
    assert get_all_response.status_code == 200
    tasks = get_all_response.json()["tasks"]
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id

    # Test getting a specific task
    get_one_response = client.get(f"/api/{user_id}/tasks/{task_id}", headers=headers)
    assert get_one_response.status_code == 200
    task = get_one_response.json()["task"]
    assert task["id"] == task_id
    assert task["title"] == "Test Task"

    # Test updating a task
    update_response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Updated Description"},
        headers=headers
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()["task"]
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Task"

    # Test toggling task completion
    toggle_response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        json={"completed": True},
        headers=headers
    )
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()["task"]
    assert toggled_task["id"] == task_id
    assert toggled_task["completed"] == True

    # Test deleting a task
    delete_response = client.delete(f"/api/{user_id}/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200

    # Verify the task was deleted
    get_deleted_response = client.get(f"/api/{user_id}/tasks/{task_id}", headers=headers)
    assert get_deleted_response.status_code == 404

def test_cross_user_access_prevention(client: TestClient, session: Session):
    """Test that users cannot access each other's tasks"""
    # Create first user
    signup_response1 = client.post(
        "/api/auth/signup",
        json={"email": "user1@example.com", "password": "password123"}
    )
    assert signup_response1.status_code == 200
    token1 = signup_response1.json()["token"]
    user1_id = signup_response1.json()["user"]["id"]

    # Create second user
    signup_response2 = client.post(
        "/api/auth/signup",
        json={"email": "user2@example.com", "password": "password123"}
    )
    assert signup_response2.status_code == 200
    token2 = signup_response2.json()["token"]
    user2_id = signup_response2.json()["user"]["id"]

    # First user creates a task
    headers1 = {"Authorization": f"Bearer {token1}"}
    create_response = client.post(
        f"/api/{user1_id}/tasks",
        json={"title": "User1's Task", "description": "Private Task"},
        headers=headers1
    )
    assert create_response.status_code == 200
    task_id = create_response.json()["task"]["id"]

    # Second user tries to access first user's task (should fail)
    headers2 = {"Authorization": f"Bearer {token2}"}
    get_response = client.get(f"/api/{user1_id}/tasks/{task_id}", headers=headers2)
    assert get_response.status_code == 403  # Forbidden

    # Second user tries to create task for first user (should fail)
    create_other_response = client.post(
        f"/api/{user1_id}/tasks",
        json={"title": "Attempted Hijacking", "description": "Should fail"},
        headers=headers2
    )
    assert create_other_response.status_code == 403  # Forbidden