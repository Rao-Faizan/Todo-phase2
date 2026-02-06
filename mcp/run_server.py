#!/usr/bin/env python3
"""MCP Server for Todo Management"""

from mcp.server import Server
from mcp.shared import StdioServerParameters
from mcp.tool import Tool
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and models (will be created later)
from config import config

# Import tools
from tools.add_task import add_task_fn
from tools.list_tasks import list_tasks_fn
from tools.complete_task import complete_task_fn
from tools.delete_task import delete_task_fn
from tools.update_task import update_task_fn


async def run_mcp_server():
    """Run the MCP server"""
    print("Starting MCP Server for Todo Management...")

    # Initialize MCP server
    server = Server(
        name="todo-mcp-server",
        version="1.0.0",
        description="MCP server for managing todo operations"
    )

    # Create tool instances
    add_task_tool = Tool(
        name="add_task",
        description="Add a new task to the user's todo list",
        input_schema={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description (optional)"},
                "due_date": {"type": "string", "description": "Due date in ISO format (optional)"},
                "priority": {"type": "string", "description": "Priority level (low, medium, high) (optional)"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for the task (optional)"}
            },
            "required": ["title"]
        },
        fn=add_task_fn
    )

    list_tasks_tool = Tool(
        name="list_tasks",
        description="List tasks from the user's todo list with optional filtering",
        input_schema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter by status (all, pending, completed)"},
                "limit": {"type": "integer", "description": "Limit number of tasks returned"},
                "sort_by": {"type": "string", "description": "Sort by field (created_at, due_date, priority)"}
            }
        },
        fn=list_tasks_fn
    )

    complete_task_tool = Tool(
        name="complete_task",
        description="Mark a task as completed",
        input_schema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID of the task to complete"},
                "task_identifier": {"type": "string", "description": "Alternative way to identify task, e.g., title"}
            },
            "required": ["task_id"]
        },
        fn=complete_task_fn
    )

    delete_task_tool = Tool(
        name="delete_task",
        description="Delete a task from the user's todo list",
        input_schema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID of the task to delete"},
                "task_identifier": {"type": "string", "description": "Alternative way to identify task, e.g., title"}
            },
            "required": ["task_id"]
        },
        fn=delete_task_fn
    )

    update_task_tool = Tool(
        name="update_task",
        description="Update properties of an existing task",
        input_schema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string", "description": "ID of the task to update"},
                "task_identifier": {"type": "string", "description": "Alternative way to identify task, e.g., title"},
                "updates": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "due_date": {"type": "string"},
                        "priority": {"type": "string"},
                        "status": {"type": "string"}
                    }
                }
            },
            "required": ["task_id", "updates"]
        },
        fn=update_task_fn
    )

    # Register tools with the server
    server.register_tool(add_task_tool)
    server.register_tool(list_tasks_tool)
    server.register_tool(complete_task_tool)
    server.register_tool(delete_task_tool)
    server.register_tool(update_task_tool)

    # Run the server
    params = StdioServerParameters()
    await server.run_stdio(params)


if __name__ == "__main__":
    asyncio.run(run_mcp_server())