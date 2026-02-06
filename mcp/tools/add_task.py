"""Add Task Tool for MCP Server"""

from typing import Dict, Any
from pydantic import BaseModel
from mcp.tool import ToolResult
import httpx
from urllib.parse import urljoin
import os
from utils.response_formatter import tool_response_formatter
from utils.validation import validate_task_input


class AddTaskInput(BaseModel):
    title: str
    description: str = ""
    due_date: str = ""
    priority: str = "medium"
    tags: list[str] = []


async def add_task_fn(input: AddTaskInput) -> ToolResult:
    """
    Add a new task to the user's todo list.
    """
    try:
        # Validate input
        validation_result = validate_task_input(
            title=input.title,
            description=input.description,
            priority=input.priority,
            due_date=input.due_date
        )

        if not validation_result.is_valid:
            formatted_response = tool_response_formatter.format_validation_error(
                errors=validation_result.errors,
                action="add_task"
            )

            return ToolResult(
                content=f"Validation failed: {'; '.join(validation_result.errors)}",
                metadata=formatted_response
            )

        # Prepare task data
        task_data = {
            "title": input.title,
            "description": input.description,
            "completed": False
        }

        if input.due_date:
            task_data["due_date"] = input.due_date
        if input.priority:
            task_data["priority"] = input.priority
        if input.tags:
            task_data["tags"] = input.tags

        # Get backend API URL from environment
        backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

        # Construct the API endpoint
        api_url = urljoin(backend_url, "/api/tasks")

        # Make request to backend API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, json=task_data)

        if response.status_code == 200 or response.status_code == 201:
            result_data = response.json()

            # Format the success response
            formatted_response = tool_response_formatter.format_success(
                data=result_data,
                action="add_task",
                metadata={"task_id": result_data.get("id"), "title": input.title}
            )

            return ToolResult(
                content=f"Successfully added task: {input.title}",
                metadata=formatted_response
            )
        else:
            error_detail = response.text
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Backend API error: {error_detail}",
                action="add_task"
            )

            return ToolResult(
                content=f"Failed to add task: {error_detail}",
                metadata=formatted_response
            )

    except httpx.ConnectError:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Cannot connect to backend API. Please check if the backend service is running.",
            action="add_task"
        )

        return ToolResult(
            content="Cannot connect to backend API. Please check if the backend service is running.",
            metadata=formatted_response
        )
    except httpx.TimeoutException:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Request to backend API timed out.",
            action="add_task"
        )

        return ToolResult(
            content="Request to backend API timed out.",
            metadata=formatted_response
        )
    except Exception as e:
        formatted_response = tool_response_formatter.format_error(
            error_msg=f"Unexpected error adding task: {str(e)}",
            action="add_task"
        )

        return ToolResult(
            content=f"Error adding task: {str(e)}",
            metadata=formatted_response
        )