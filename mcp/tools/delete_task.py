"""Delete Task Tool for MCP Server"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from mcp.tool import ToolResult
import httpx
from urllib.parse import urljoin
import os
from utils.response_formatter import tool_response_formatter


class DeleteTaskInput(BaseModel):
    task_id: str
    task_identifier: Optional[str] = None  # Alternative way to identify task


async def delete_task_fn(input: DeleteTaskInput) -> ToolResult:
    """
    Delete a task from the user's todo list.
    """
    try:
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
                        action="delete_task"
                    )

                    return ToolResult(
                        content=f"No task found with identifier '{input.task_identifier}'.",
                        metadata=formatted_response
                    )
            else:
                formatted_response = tool_response_formatter.format_error(
                    error_msg="Failed to search for task by identifier.",
                    action="delete_task"
                )

                return ToolResult(
                    content="Failed to search for task by identifier.",
                    metadata=formatted_response
                )

        # Construct the API endpoint for deleting the task
        api_url = urljoin(backend_url, f"/api/tasks/{actual_task_id}")

        # Make request to backend API to delete the task
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(api_url)

        if response.status_code == 200:
            result_data = response.json()

            # Format the success response
            formatted_response = tool_response_formatter.format_success(
                data=result_data,
                action="delete_task",
                metadata={"task_id": actual_task_id, "title": result_data.get("title")}
            )

            return ToolResult(
                content=f"Successfully deleted task: {result_data.get('title', 'Unknown Task')} (ID: {actual_task_id})",
                metadata=formatted_response
            )
        elif response.status_code == 404:
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Task with ID {actual_task_id} not found.",
                action="delete_task"
            )

            return ToolResult(
                content=f"Task with ID {actual_task_id} not found.",
                metadata=formatted_response
            )
        else:
            error_detail = response.text
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Backend API error: {error_detail}",
                action="delete_task"
            )

            return ToolResult(
                content=f"Failed to delete task: {error_detail}",
                metadata=formatted_response
            )

    except httpx.ConnectError:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Cannot connect to backend API. Please check if the backend service is running.",
            action="delete_task"
        )

        return ToolResult(
            content="Cannot connect to backend API. Please check if the backend service is running.",
            metadata=formatted_response
        )
    except httpx.TimeoutException:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Request to backend API timed out.",
            action="delete_task"
        )

        return ToolResult(
            content="Request to backend API timed out.",
            metadata=formatted_response
        )
    except Exception as e:
        formatted_response = tool_response_formatter.format_error(
            error_msg=f"Unexpected error deleting task: {str(e)}",
            action="delete_task"
        )

        return ToolResult(
            content=f"Error deleting task: {str(e)}",
            metadata=formatted_response
        )