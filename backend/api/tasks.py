from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from typing import Annotated, List
from uuid import UUID
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from pydantic import BaseModel
from services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from database import get_session
from middleware.user_validation import get_current_user, verify_user_owns_resource
from slowapi import Limiter
from slowapi.util import get_remote_address

# Response models to match test expectations
class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

class TaskSingleResponse(BaseModel):
    task: TaskResponse

class TaskSuccessResponse(BaseModel):
    success: bool
    task: TaskResponse = None

# Create limiter for task routes
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

from fastapi.responses import JSONResponse

@router.get("/tasks", response_model=TaskListResponse)
@limiter.limit("100/minute")
def read_tasks(
    request: Request,
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for a specific user"""
    # Verify that the authenticated user is accessing their own tasks
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")

    tasks = get_tasks(user_id, session)
    return TaskListResponse(tasks=[TaskResponse.from_orm(task) for task in tasks])

@router.post("/tasks", response_model=TaskSingleResponse)
@limiter.limit("100/minute")
def create_new_task(
    request: Request,
    user_id: UUID,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for a specific user"""
    # Verify that the authenticated user is creating tasks for themselves
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot create tasks for another user")

    task = create_task(user_id, task_data, session)
    return TaskSingleResponse(task=TaskResponse.from_orm(task))

@router.get("/tasks/{task_id}", response_model=TaskSingleResponse)
@limiter.limit("100/minute")
def read_task(
    request: Request,
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for a specific user"""
    # Verify that the authenticated user is accessing their own task
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's task")

    task = get_task(user_id, task_id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSingleResponse(task=TaskResponse.from_orm(task))

@router.put("/tasks/{task_id}", response_model=TaskSingleResponse)
@limiter.limit("100/minute")
def update_existing_task(
    request: Request,
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for a specific user"""
    # Verify that the authenticated user is updating their own task
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot update another user's task")

    task = update_task(user_id, task_id, task_data, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSingleResponse(task=TaskResponse.from_orm(task))

class TaskCompletionUpdate(BaseModel):
    completed: bool

@router.patch("/tasks/{task_id}/complete", response_model=TaskSingleResponse)
@limiter.limit("100/minute")
def toggle_task_complete(
    request: Request,
    user_id: UUID,
    task_id: UUID,
    task_completion: TaskCompletionUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle completion status of a specific task for a specific user"""
    # Verify that the authenticated user is toggling their own task
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot update another user's task")

    task = toggle_task_completion(user_id, task_id, task_completion.completed, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSingleResponse(task=TaskResponse.from_orm(task))

@router.delete("/tasks/{task_id}")
@limiter.limit("100/minute")
def remove_task(
    request: Request,
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for a specific user"""
    # Verify that the authenticated user is deleting their own task
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot delete another user's task")

    success = delete_task(user_id, task_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}