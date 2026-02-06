"""Update Task Tool for MCP Server"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from mcp.tool import ToolResult
import httpx
from urllib.parse import urljoin
import os
from utils.response_formatter import tool_response_formatter
from utils.validation import validate_task_updates


class UpdateTaskUpdates(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class UpdateTaskInput(BaseModel):
    task_id: str
    task_identifier: Optional[str] = None  # Alternative way to identify task
    updates: UpdateTaskUpdates


async def update_task_fn(input: UpdateTaskInput) -> ToolResult:
    """
    Update properties of an existing task.
    """
    try:
        # Validate update parameters
        update_dict = input.updates.dict(exclude_unset=True)
        validation_result = validate_task_updates(update_dict)

        if not validation_result.is_valid:
            formatted_response = tool_response_formatter.format_validation_error(
                errors=validation_result.errors,
                action="update_task"
            )

            return ToolResult(
                content=f"Validation failed for update parameters: {'; '.join(validation_result.errors)}",
                metadata=formatted_response
            )

        # Get backend API URL from environment
        backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

        # If task_identifier is provided but not task_id, we need to find the task first
        actual_task_id = input.task_id
        if not actual_task_id and input.task_identifier:
            # Search for task by identifier
            search_url = urljoin(backend_url, "/api/tasks")

            async with httpx.AsyncClient(timeout=30.0) as client:
                search_response = await client.get(search_url, params={"search": input.task_identifier})

            if search_response.status_code == 200:
                search_results = search_response.json()
                tasks = search_results.get("tasks", [])

                if tasks:
                    actual_task_id = tasks[0]["id"]
                else:
                    formatted_response = tool_response_formatter.format_error(
                        error_msg=f"No task found with identifier '{input.task_identifier}'.",
                        action="update_task"
                    )

                    return ToolResult(
                        content=f"No task found with identifier '{input.task_identifier}'.",
                        metadata=formatted_response
                    )
            else:
                formatted_response = tool_response_formatter.format_error(
                    error_msg="Failed to search for task by identifier.",
                    action="update_task"
                )

                return ToolResult(
                    content="Failed to search for task by identifier.",
                    metadata=formatted_response
                )

        # Prepare update data
        update_data = {}
        if input.updates.title is not None:
            update_data["title"] = input.updates.title
        if input.updates.description is not None:
            update_data["description"] = input.updates.description
        if input.updates.due_date is not None:
            update_data["due_date"] = input.updates.due_date
        if input.updates.priority is not None:
            update_data["priority"] = input.updates.priority
        if input.updates.status is not None:
            # Map status to completed boolean if needed
            if input.updates.status.lower() in ["completed", "done", "finished"]:
                update_data["completed"] = True
            elif input.updates.status.lower() in ["pending", "incomplete", "not done"]:
                update_data["completed"] = False
            else:
                update_data["status"] = input.updates.status

        # Check if there are any updates to apply
        if not update_data:
            formatted_response = tool_response_formatter.format_error(
                error_msg="No updates provided to apply.",
                action="update_task"
            )

            return ToolResult(
                content="No updates provided to apply.",
                metadata=formatted_response
            )

        # Construct the API endpoint for updating the task
        api_url = urljoin(backend_url, f"/api/tasks/{actual_task_id}")

        # Make request to backend API to update the task
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(api_url, json=update_data)

        if response.status_code == 200:
            result_data = response.json()

            # Prepare updates description for the response
            updates_list = []
            if input.updates.title is not None:
                updates_list.append(f"title to '{input.updates.title}'")
            if input.updates.description is not None:
                updates_list.append(f"description to '{input.updates.description}'")
            if input.updates.due_date is not None:
                updates_list.append(f"due date to '{input.updates.due_date}'")
            if input.updates.priority is not None:
                updates_list.append(f"priority to '{input.updates.priority}'")
            if input.updates.status is not None:
                updates_list.append(f"status to '{input.updates.status}'")

            updates_str = ", ".join(updates_list)

            # Format the success response
            formatted_response = tool_response_formatter.format_success(
                data=result_data,
                action="update_task",
                metadata={
                    "task_id": actual_task_id,
                    "title": result_data.get("title"),
                    "updates_applied": updates_list
                }
            )

            return ToolResult(
                content=f"Successfully updated task: {result_data.get('title', 'Unknown Task')} (ID: {actual_task_id}). Changes applied: {updates_str}",
                metadata=formatted_response
            )
        elif response.status_code == 404:
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Task with ID {actual_task_id} not found.",
                action="update_task"
            )

            return ToolResult(
                content=f"Task with ID {actual_task_id} not found.",
                metadata=formatted_response
            )
        else:
            error_detail = response.text
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Backend API error: {error_detail}",
                action="update_task"
            )

            return ToolResult(
                content=f"Failed to update task: {error_detail}",
                metadata=formatted_response
            )

    except httpx.ConnectError:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Cannot connect to backend API. Please check if the backend service is running.",
            action="update_task"
        )

        return ToolResult(
            content="Cannot connect to backend API. Please check if the backend service is running.",
            metadata=formatted_response
        )
    except httpx.TimeoutException:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Request to backend API timed out.",
            action="update_task"
        )

        return ToolResult(
            content="Request to backend API timed out.",
            metadata=formatted_response
        )
    except Exception as e:
        formatted_response = tool_response_formatter.format_error(
            error_msg=f"Unexpected error updating task: {str(e)}",
            action="update_task"
        )

        return ToolResult(
            content=f"Error updating task: {str(e)}",
            metadata=formatted_response
        )