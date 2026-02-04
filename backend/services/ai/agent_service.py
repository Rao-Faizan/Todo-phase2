"""AI Agent Service for processing chat messages with OpenAI and MCP tools"""

import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlmodel import Session
from openai import AsyncOpenAI
try:
    from mcp.client import Client
except ImportError:
    # MCP client may not be available in all environments
    Client = None
from repositories.task_repository import TaskRepository
from models.conversation import Conversation
from models.message import Message
from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository
from services.nlp.intent_detection_service import intent_detection_service, TaskIntent
from services.nlp.task_extraction_service import task_extraction_service
from datetime import datetime


class AgentService:
    def __init__(self):
        self.openai_client = None  # Initialize only when needed to avoid API key requirement
        # Initialize MCP client
        self.mcp_client = None  # Will be initialized when needed
        # Repositories will be initialized with sessions when needed
        self.task_repo = None
        self.conversation_repo = None
        self.message_repo = None

    async def process_message(
        self,
        user_id: UUID,
        message_content: str,
        conversation_id: Optional[UUID] = None,
        session: Session = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and return the AI response

        Args:
            user_id: The ID of the user
            message_content: The message content from the user
            conversation_id: Optional conversation ID, creates new if None
            session: Database session

        Returns:
            Dictionary containing the AI response and any tool results
        """
        try:
            # Initialize repositories with the session
            self.task_repo = TaskRepository(session)
            self.conversation_repo = ConversationRepository(session)
            self.message_repo = MessageRepository(session)

            # Get or create conversation
            if conversation_id is None:
                from models.conversation import ConversationCreate
                conversation_create_obj = ConversationCreate(user_id=user_id)
                conversation = self.conversation_repo.create(
                    conversation_create_obj
                )
                conversation_id = conversation.id
            else:
                conversation = self.conversation_repo.get_by_id(conversation_id)
                if not conversation or conversation.user_id != user_id:
                    raise ValueError("Conversation not found or unauthorized")

            # Initialize OpenAI/Gemini client for task extraction and general chat
            if self.openai_client is None:
                from openai import AsyncOpenAI
                import os
                
                # Check for Gemini API Key first
                gemini_api_key = os.getenv("GEMINI_API_KEY")
                openai_api_key = os.getenv("OPENAI_API_KEY")
                
                if gemini_api_key and "your-gemini-api-key" not in gemini_api_key:
                    # Configure for Gemini (Google) via OpenAI SDK compatibility
                    self.openai_client = AsyncOpenAI(
                        api_key=gemini_api_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
                    )
                    self.model_name = "gemini-1.5-flash"
                elif openai_api_key and "your-openai-api-key" not in openai_api_key:
                    # Configure for standard OpenAI
                    self.openai_client = AsyncOpenAI(api_key=openai_api_key)
                    self.model_name = "gpt-3.5-turbo"

            # Save user message
            from models.message import MessageCreate
            message_create_obj = MessageCreate(
                conversation_id=conversation_id,
                role="user",
                content=message_content
            )
            user_message = self.message_repo.create(
                message_create_obj
            )

            # Detect intent from user message
            intent_result = await intent_detection_service.detect_intent(message_content)

            # Handle different intents
            if intent_result.intent == TaskIntent.ADD_TASK:
                response = await self._handle_add_task(user_id, message_content, session)
            elif intent_result.intent == TaskIntent.LIST_TASKS:
                response = await self._handle_list_tasks(user_id, message_content, session)
            elif intent_result.intent == TaskIntent.COMPLETE_TASK:
                response = await self._handle_complete_task(user_id, message_content, session)
            elif intent_result.intent == TaskIntent.UPDATE_TASK:
                response = await self._handle_update_task(user_id, message_content, session)
            elif intent_result.intent == TaskIntent.DELETE_TASK:
                response = await self._handle_delete_task(user_id, message_content, session)
            else:
                # Use OpenAI for general conversation
                response = await self._get_openai_response(user_id, message_content, conversation_id, session)

            # Save AI response
            ai_message = self.message_repo.create(
                MessageCreate(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=response
                )
            )

            return {
                "response": response,
                "conversation_id": conversation_id,
                "message_id": ai_message.id
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error in process_message: {str(e)}")
            raise e

    async def _handle_add_task(self, user_id: UUID, message_content: str, session: Session) -> str:
        """Handle adding a task based on user message"""
        try:
            # Extract task details from message
            extracted_task = await task_extraction_service.extract_task_details(message_content, agent_service=self)

            # Validate required fields
            if not extracted_task.title:
                return "I need a task title to create a task. Please specify what you'd like to add."

            # Create task
            task_data = {
                "title": extracted_task.title,
                "description": extracted_task.description or "",
                "completed": False
            }

            if extracted_task.due_date:
                task_data["due_date"] = extracted_task.due_date
            if extracted_task.priority:
                task_data["priority"] = extracted_task.priority

            from models.task import TaskCreate
            task_create_obj = TaskCreate(**task_data)

            # Create task with the initialized repository
            new_task = self.task_repo.create(user_id, task_create_obj)

            return f"I've added the task '{new_task.title}' to your list. Task ID: {new_task.id}"
        except Exception as e:
            return f"Sorry, I couldn't add the task. Error: {str(e)}"

    async def _handle_list_tasks(self, user_id: UUID, message_content: str, session: Session) -> str:
        """Handle listing tasks based on user message"""
        try:
            # Get all tasks for the user
            all_tasks = self.task_repo.get_by_user(user_id)

            if not all_tasks:
                return "You don't have any tasks right now. Would you like to add one?"

            # Filter tasks based on request (all, completed, pending, etc.)
            filter_completed = None
            if "completed" in message_content.lower():
                filtered_tasks = [t for t in all_tasks if t.completed]
            elif "pending" in message_content.lower() or "incomplete" in message_content.lower():
                filtered_tasks = [t for t in all_tasks if not t.completed]
            else:
                filtered_tasks = all_tasks  # Show all tasks

            if not filtered_tasks:
                if "completed" in message_content.lower():
                    return "You don't have any completed tasks right now."
                else:
                    return "You don't have any pending tasks right now."

            # Format response
            task_list = []
            for i, task in enumerate(filtered_tasks, 1):
                status = "✓" if task.completed else "○"
                task_str = f"{i}. [{status}] {task.title}"
                if task.description:
                    task_str += f" - {task.description}"
                if task.due_date:
                    task_str += f" (Due: {task.due_date})"
                task_list.append(task_str)

            response = f"You have {len(filtered_tasks)} task(s):\n" + "\n".join(task_list)
            return response
        except Exception as e:
            return f"Sorry, I couldn't retrieve your tasks. Error: {str(e)}"

    async def _handle_complete_task(self, user_id: UUID, message_content: str, session: Session) -> str:
        """Handle completing a task based on user message"""
        try:
            # Extract task information from message
            # Look for task identifiers in the message
            all_tasks = self.task_repo.get_by_user(user_id)

            # Find task by title or description (case-insensitive partial match)
            target_task = None
            message_lower = message_content.lower()

            for task in all_tasks:
                if task.title.lower() in message_lower or (task.description and task.description.lower() in message_lower):
                    target_task = task
                    break

            # If no exact match, try partial matching
            if not target_task:
                for task in all_tasks:
                    if message_lower in task.title.lower() or (task.description and message_lower in task.description.lower()):
                        target_task = task
                        break

            if not target_task:
                # If still no match, ask for clarification
                return f"I couldn't find a task matching '{message_content}'. Could you please specify which task you want to complete?"

            # Update task as completed
            from models.task import TaskUpdate
            task_update = TaskUpdate(completed=True)
            updated_task = self.task_repo.update(target_task.id, task_update)

            if updated_task:
                return f"I've marked the task '{updated_task.title}' as completed!"
            else:
                return "Sorry, I couldn't update that task. It may not exist or you may not have permission to modify it."

        except Exception as e:
            return f"Sorry, I couldn't complete the task. Error: {str(e)}"

    async def _handle_update_task(self, user_id: UUID, message_content: str, session: Session) -> str:
        """Handle updating a task based on user message"""
        try:
            # Extract task information and update details
            all_tasks = self.task_repo.get_by_user(user_id)

            # For simplicity, we'll look for "update task 'title' to 'new value'"
            # In a real implementation, we'd have more sophisticated parsing
            import re

            # Look for patterns like "update task 'old title' to 'new title'"
            update_pattern = r"update task ['\"]([^'\"]+)['\"](?:\s+to|\s+set\s+to|\s+change\s+to)?\s*['\"]([^'\"]+)['\"]"
            match = re.search(update_pattern, message_content, re.IGNORECASE)

            if match:
                old_title = match.group(1)
                new_value = match.group(2)

                # Find task by title
                target_task = None
                for task in all_tasks:
                    if old_title.lower() in task.title.lower():
                        target_task = task
                        break

                if target_task:
                    # Update the task title
                    from models.task import TaskUpdate
                    task_update = TaskUpdate(title=new_value)
                    updated_task = self.task_repo.update(target_task.id, task_update)

                    if updated_task:
                        return f"I've updated the task '{target_task.title}' to '{updated_task.title}'."
                    else:
                        return "Sorry, I couldn't update that task."
                else:
                    return f"I couldn't find a task with title containing '{old_title}'."
            else:
                return "I couldn't understand the update request. Please specify which task you want to update and what changes to make."

        except Exception as e:
            return f"Sorry, I couldn't update the task. Error: {str(e)}"

    async def _handle_delete_task(self, user_id: UUID, message_content: str, session: Session) -> str:
        """Handle deleting a task based on user message with confirmation"""
        try:
            # Extract task information from message
            all_tasks = self.task_repo.get_by_user(user_id)

            # Look for the task to delete based on message content
            target_task = None
            message_lower = message_content.lower()

            # First, try exact matches
            for task in all_tasks:
                if task.title.lower() in message_lower or (task.description and task.description.lower() in message_lower):
                    target_task = task
                    break

            # If no exact match, try partial matching
            if not target_task:
                for task in all_tasks:
                    if message_lower in task.title.lower() or (task.description and message_lower in task.description.lower()):
                        target_task = task
                        break

            if not target_task:
                # If still no match, ask for clarification
                return f"I couldn't find a task matching '{message_content}'. Could you please specify which task you want to delete?"

            # Add confirmation for deletion to prevent accidental deletions
            confirmation_needed = True
            confirmation_keywords = ["confirm", "sure", "yes", "delete"]

            # Check if user already provided confirmation
            for keyword in confirmation_keywords:
                if keyword in message_lower:
                    confirmation_needed = False
                    break

            if confirmation_needed:
                # Return a confirmation request instead of deleting
                return f"Are you sure you want to delete the task '{target_task.title}'? Please confirm by saying 'yes, delete' or 'confirm delete'."

            # Proceed with deletion if confirmed
            deleted = self.task_repo.delete(target_task.id)

            if deleted:
                return f"I've deleted the task '{target_task.title}'. The task has been removed from your list."
            else:
                return "Sorry, I couldn't delete that task. It may not exist or you may not have permission to delete it."

        except Exception as e:
            return f"Sorry, I couldn't delete the task. Error: {str(e)}"

    async def _get_openai_response(self, user_id: UUID, message_content: str, conversation_id: UUID, session: Session) -> str:
        """Get response from OpenAI for general conversation"""
        try:
            # Check if client was initialized (should be done in process_message)
            if self.openai_client is None:
                 return (
                    "I'm unable to process your request because the AI service is not configured properly. "
                    "Please set a valid GEMINI_API_KEY or OPENAI_API_KEY in the .env file."
                )

            # Retrieve conversation history for context
            messages = self.message_repo.get_by_conversation(conversation_id)

            # Format messages for OpenAI/Gemini
            openai_messages = []

            # Add system message
            openai_messages.append({
                "role": "system",
                "content": "You are a helpful assistant for managing tasks. You can help users add, list, complete, update, and delete tasks. If a user asks about tasks, try to identify their intent (add, list, complete, update, delete) and respond accordingly. Be friendly and concise."
            })

            # Add conversation history
            for msg in messages:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Add the current user message
            openai_messages.append({
                "role": "user",
                "content": message_content
            })

            # Call OpenAI API (works for Gemini too via compatibility layer)
            response = await self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=openai_messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Sorry, I encountered an error processing your request: {str(e)}"


# Global instance
# NOTE: This is initialized here but repositories will be initialized per request with session
agent_service = AgentService()