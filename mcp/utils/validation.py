"""Validation utilities for MCP tools"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, validator
import re


class TaskValidationResult(BaseModel):
    """Result of task validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = []


def validate_task_title(title: str) -> TaskValidationResult:
    """Validate task title"""
    errors = []
    warnings = []

    if not title or not title.strip():
        errors.append("Task title cannot be empty")
    elif len(title.strip()) > 200:
        errors.append("Task title must be 200 characters or less")

    if title and len(title.strip()) < 3:
        warnings.append("Task title seems very short (< 3 characters)")

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_task_priority(priority: str) -> TaskValidationResult:
    """Validate task priority"""
    errors = []
    warnings = []

    valid_priorities = ["low", "medium", "high"]

    if priority and priority.lower() not in valid_priorities:
        errors.append(f"Priority must be one of: {', '.join(valid_priorities)}")

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_task_due_date(due_date: str) -> TaskValidationResult:
    """Validate task due date format"""
    errors = []
    warnings = []

    if due_date:
        # Check if it's in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        iso_date_pattern = r'^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?)?$'

        if not re.match(iso_date_pattern, due_date):
            errors.append("Due date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_task_tags(tags: List[str]) -> TaskValidationResult:
    """Validate task tags"""
    errors = []
    warnings = []

    if tags:
        for tag in tags:
            if not tag or not tag.strip():
                errors.append("Tags cannot be empty")
            elif len(tag.strip()) > 50:
                errors.append(f"Tag '{tag}' is too long (max 50 characters)")
            elif not re.match(r'^[a-zA-Z0-9_-]+$', tag.strip()):
                warnings.append(f"Tag '{tag}' contains special characters (recommended: letters, numbers, hyphens, underscores only)")

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_task_updates(updates: Dict[str, Any]) -> TaskValidationResult:
    """Validate task update parameters"""
    errors = []
    warnings = []

    # Validate title if provided
    if "title" in updates and updates["title"] is not None:
        title_result = validate_task_title(updates["title"])
        errors.extend(title_result.errors)
        warnings.extend(title_result.warnings)

    # Validate priority if provided
    if "priority" in updates and updates["priority"] is not None:
        priority_result = validate_task_priority(updates["priority"])
        errors.extend(priority_result.errors)
        warnings.extend(priority_result.warnings)

    # Validate due date if provided
    if "due_date" in updates and updates["due_date"] is not None:
        due_date_result = validate_task_due_date(updates["due_date"])
        errors.extend(due_date_result.errors)
        warnings.extend(due_date_result.warnings)

    # Validate tags if provided
    if "tags" in updates and updates["tags"] is not None:
        tags_result = validate_task_tags(updates["tags"])
        errors.extend(tags_result.errors)
        warnings.extend(tags_result.warnings)

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def validate_task_input(title: str, description: str = "", priority: str = "", due_date: str = "") -> TaskValidationResult:
    """Validate complete task input"""
    errors = []
    warnings = []

    # Validate title
    title_result = validate_task_title(title)
    errors.extend(title_result.errors)
    warnings.extend(title_result.warnings)

    # Validate priority
    if priority:
        priority_result = validate_task_priority(priority)
        errors.extend(priority_result.errors)
        warnings.extend(priority_result.warnings)

    # Validate due date
    if due_date:
        due_date_result = validate_task_due_date(due_date)
        errors.extend(due_date_result.errors)
        warnings.extend(due_date_result.warnings)

    # Validate description length
    if description and len(description) > 1000:
        errors.append("Description must be 1000 characters or less")

    return TaskValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )