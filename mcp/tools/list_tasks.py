"""List Tasks Tool for MCP Server"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from mcp.tool import ToolResult
import httpx
from urllib.parse import urljoin, urlencode
import os
from utils.response_formatter import tool_response_formatter


class ListTasksInput(BaseModel):
    status: str = "all"  # "all", "pending", "completed"
    limit: Optional[int] = None
    sort_by: str = "created_at"  # "created_at", "due_date", "priority"


async def list_tasks_fn(input: ListTasksInput) -> ToolResult:
    """
    List tasks from the user's todo list with optional filtering.
    """
    try:
        # Get backend API URL from environment
        backend_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

        # Build query parameters
        params = {}
        if input.status and input.status != "all":
            params["status"] = input.status
        if input.limit is not None and input.limit > 0:
            params["limit"] = input.limit
        if input.sort_by:
            params["sort_by"] = input.sort_by

        # Construct the API endpoint with query parameters
        base_url = urljoin(backend_url, "/api/tasks")
        if params:
            query_string = urlencode(params)
            api_url = f"{base_url}?{query_string}"
        else:
            api_url = base_url

        # Make request to backend API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(api_url)

        if response.status_code == 200:
            result_data = response.json()
            tasks = result_data.get("tasks", [])

            # Format response
            if not tasks:
                response_content = "No tasks found."
            else:
                task_list = []
                for task in tasks:
                    status_icon = "✓" if task.get("completed", False) else "○"
                    task_line = f"{status_icon} {task.get('title', 'Untitled Task')}"

                    if task.get('priority'):
                        task_line += f" (Priority: {task['priority']})"
                    if task.get('due_date'):
                        task_line += f" (Due: {task['due_date']})"
                    if task.get('description'):
                        task_line += f" - {task['description']}"

                    task_list.append(task_line)

                response_content = f"Found {len(tasks)} tasks:\n" + "\n".join([f"- {task}" for task in task_list])

            # Format the success response
            formatted_response = tool_response_formatter.format_success(
                data={"tasks": tasks, "count": len(tasks)},
                action="list_tasks",
                metadata={"task_count": len(tasks), "filter": input.status}
            )

            return ToolResult(
                content=response_content,
                metadata=formatted_response
            )
        else:
            error_detail = response.text
            formatted_response = tool_response_formatter.format_error(
                error_msg=f"Backend API error: {error_detail}",
                action="list_tasks"
            )

            return ToolResult(
                content=f"Failed to list tasks: {error_detail}",
                metadata=formatted_response
            )

    except httpx.ConnectError:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Cannot connect to backend API. Please check if the backend service is running.",
            action="list_tasks"
        )

        return ToolResult(
            content="Cannot connect to backend API. Please check if the backend service is running.",
            metadata=formatted_response
        )
    except httpx.TimeoutException:
        formatted_response = tool_response_formatter.format_error(
            error_msg="Request to backend API timed out.",
            action="list_tasks"
        )

        return ToolResult(
            content="Request to backend API timed out.",
            metadata=formatted_response
        )
    except Exception as e:
        formatted_response = tool_response_formatter.format_error(
            error_msg=f"Unexpected error listing tasks: {str(e)}",
            action="list_tasks"
        )

        return ToolResult(
            content=f"Error listing tasks: {str(e)}",
            metadata=formatted_response
        )