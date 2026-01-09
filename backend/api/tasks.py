from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel import Session
from typing import Annotated, List
from uuid import UUID
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse
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

# Create limiter for task routes
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
@limiter.limit("100/minute")
async def read_tasks(
    request: Request,
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for a specific user"""
    # Verify that the authenticated user is accessing their own tasks
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")

    tasks = await get_tasks(user_id, session)
    return [TaskResponse.from_orm(task) for task in tasks]

@router.post("/tasks", response_model=TaskResponse)
@limiter.limit("100/minute")
async def create_new_task(
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

    task = await create_task(user_id, task_data, session)
    return TaskResponse.from_orm(task)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("100/minute")
async def read_task(
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

    task = await get_task(user_id, task_id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_orm(task)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
@limiter.limit("100/minute")
async def update_existing_task(
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

    task = await update_task(user_id, task_id, task_data, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_orm(task)

@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
@limiter.limit("100/minute")
async def toggle_task_complete(
    request: Request,
    user_id: UUID,
    task_id: UUID,
    completed: bool,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle completion status of a specific task for a specific user"""
    # Verify that the authenticated user is toggling their own task
    if not verify_user_owns_resource(user_id, current_user):
        raise HTTPException(status_code=403, detail="Access denied: Cannot update another user's task")

    task = await toggle_task_completion(user_id, task_id, completed, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse.from_orm(task)

@router.delete("/tasks/{task_id}")
@limiter.limit("100/minute")
async def remove_task(
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

    success = await delete_task(user_id, task_id, session)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}