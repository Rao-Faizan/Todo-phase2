# Feature Specification: AI Chatbot for Todo Management

## 1. Overview & Purpose

The AI Chatbot for Todo Management feature provides a natural language interface that allows users to manage their todo lists through conversational interactions. Using OpenAI's ChatKit frontend and OpenAI Agents SDK backend, users can speak to an intelligent assistant that understands natural language commands and performs todo operations using standardized MCP tools. The system maintains conversation history in the database and integrates with existing authentication to ensure user data isolation.

## 2. User Stories (with priorities)

### High Priority
- **As a user**, I want to add tasks using natural language commands like "Remind me to buy groceries tomorrow" so that I don't need to use structured input forms.
- **As a user**, I want to see my current tasks by asking "What do I need to do today?" so that I can quickly get an overview of my commitments.
- **As a user**, I want to mark tasks as completed by saying "I finished the report" so that I can easily update my progress.
- **As a user**, I want to update task details by saying "Move my meeting to 3 PM" so that I can modify my schedule naturally.

### Medium Priority
- **As a user**, I want to delete tasks by saying "Remove the old appointment" so that I can clean up my todo list.
- **As a user**, I want the bot to remember our conversation context so that I can have natural follow-up interactions.
- **As a user**, I want friendly error messages when I provide invalid commands so that I understand how to interact properly.

### Low Priority
- **As a user**, I want the bot to suggest optimal times for new tasks based on my schedule so that I can plan more efficiently.
- **As a user**, I want to set priorities for tasks through conversation so that important items are highlighted.

## 3. Acceptance Criteria (detailed, testable)

### Core Functionality
- Given a user sends a natural language message to the chat endpoint, when the AI processes the request, then the appropriate MCP tool is called and the result is returned to the user.
- Given a user is authenticated, when they access the chat endpoint, then their conversation history is isolated from other users and they can only interact with their own tasks.
- Given a user sends a command that maps to a task operation, when the system processes it, then the corresponding database operation occurs and the user receives confirmation.
- Given a user sends an invalid command, when the system processes it, then the user receives a helpful error message suggesting the correct way to phrase their request.

### Conversation Management
- Given a user starts a new conversation, when they send multiple messages, then the conversation context is maintained and the AI remembers previous exchanges.
- Given a user has an ongoing conversation, when they ask about "the task I just mentioned", then the AI correctly references the appropriate task from the conversation context.
- Given a conversation has occurred, when the system stores the interaction, then both user messages and AI responses are persisted in the database with timestamps.

### Security & Access Control
- Given an unauthenticated user attempts to access the chat endpoint, when they make a request, then the system returns an authentication error.
- Given an authenticated user attempts to access another user's tasks through the chat interface, when they make a request, then the system restricts access to only their own tasks.

## 4. Chat API Endpoint (/api/{user_id}/chat)

### Endpoint Details
- **Path**: `/api/{user_id}/chat`
- **Method**: POST
- **Authentication**: JWT token required in Authorization header
- **Stateless**: Each request contains necessary context; no server-side session storage

### Request Format
```json
{
  "message": "string (user's natural language input)",
  "conversation_id": "optional string (to continue existing conversation)",
  "timestamp": "ISO 8601 datetime (client-provided timestamp)"
}
```

### Response Format
```json
{
  "response": "string (AI-generated response)",
  "conversation_id": "string (identifier for the conversation)",
  "tool_used": "string (name of MCP tool used, if any)",
  "success": "boolean (whether the operation succeeded)",
  "error": "optional string (error message if operation failed)",
  "timestamp": "ISO 8601 datetime"
}
```

### Error Responses
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User attempting to access another user's data
- **400 Bad Request**: Malformed request body
- **500 Internal Server Error**: Unexpected server error during processing

## 5. MCP Tools Specification (exact 5 tools + schemas)

### add_task
**Purpose**: Creates a new task based on natural language input
**Input Schema**:
```json
{
  "title": "string (task title extracted from user input)",
  "description": "optional string (task details)",
  "due_date": "optional string (ISO 8601 date/time)",
  "priority": "optional string ('low', 'medium', 'high')",
  "tags": "optional array of strings (task categories)"
}
```
**Output Schema**:
```json
{
  "task_id": "string (unique identifier for the created task)",
  "created": "boolean (true if successful)",
  "message": "string (confirmation message)"
}
```

### list_tasks
**Purpose**: Retrieves user's tasks with optional filtering
**Input Schema**:
```json
{
  "status": "optional string ('all', 'pending', 'completed')",
  "limit": "optional integer (max number of tasks to return)",
  "sort_by": "optional string ('created_at', 'due_date', 'priority')"
}
```
**Output Schema**:
```json
{
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "status": "string ('pending', 'completed')",
      "due_date": "string (ISO 8601) or null",
      "priority": "string ('low', 'medium', 'high')",
      "created_at": "string (ISO 8601)"
    }
  ],
  "total_count": "integer",
  "message": "string (summary message)"
}
```

### complete_task
**Purpose**: Marks a task as completed
**Input Schema**:
```json
{
  "task_id": "string (unique identifier of task to complete)",
  "task_identifier": "optional string (alternative way to identify task, e.g., title)"
}
```
**Output Schema**:
```json
{
  "task_id": "string (identifier of completed task)",
  "completed": "boolean (true if successful)",
  "message": "string (confirmation message)"
}
```

### delete_task
**Purpose**: Removes a task from the user's list
**Input Schema**:
```json
{
  "task_id": "string (unique identifier of task to delete)",
  "task_identifier": "optional string (alternative way to identify task, e.g., title)"
}
```
**Output Schema**:
```json
{
  "task_id": "string (identifier of deleted task)",
  "deleted": "boolean (true if successful)",
  "message": "string (confirmation message)"
}
```

### update_task
**Purpose**: Modifies an existing task's properties
**Input Schema**:
```json
{
  "task_id": "string (unique identifier of task to update)",
  "task_identifier": "optional string (alternative way to identify task, e.g., title)",
  "updates": {
    "title": "optional string",
    "description": "optional string",
    "due_date": "optional string (ISO 8601)",
    "priority": "optional string ('low', 'medium', 'high')",
    "status": "optional string ('pending', 'completed')"
  }
}
```
**Output Schema**:
```json
{
  "task_id": "string (identifier of updated task)",
  "updated": "boolean (true if successful)",
  "message": "string (confirmation message)"
}
```

## 6. Agent Configuration

### OpenAI Agent Setup
- **Model**: Latest OpenAI GPT model suitable for tool calling
- **Instructions**: System prompt that defines the agent's role as a todo management assistant
- **Tool Mapping**: Natural language understanding maps to the 5 specified MCP tools
- **Context Window**: Sufficient to maintain conversation history for context awareness

### Natural Language Processing
- **Intent Recognition**: Identifies user intentions (add, list, complete, delete, update)
- **Entity Extraction**: Extracts task details like titles, dates, priorities from natural language
- **Ambiguity Resolution**: Handles unclear references by asking clarifying questions
- **Fallback Handling**: Gracefully handles unrecognized commands with helpful suggestions

### Error Handling & Recovery
- **Tool Failures**: When MCP tools fail, the agent provides appropriate user-facing error messages
- **Invalid Inputs**: When user provides insufficient information, the agent asks for clarification
- **Recovery Prompts**: Guides users back to valid interaction patterns after errors

### Response Generation
- **Personalization**: Responses tailored to individual user's task patterns and preferences
- **Consistency**: Maintains consistent tone and terminology throughout conversations
- **Helpfulness**: Provides contextual suggestions and reminders when appropriate