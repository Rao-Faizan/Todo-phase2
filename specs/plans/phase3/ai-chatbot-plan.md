# Implementation Plan: AI Chatbot for Todo Management

## 1. Overview & Objectives

This implementation plan details the technical approach for building the AI Chatbot for Todo Management feature. The plan outlines how to integrate OpenAI ChatKit frontend with a FastAPI backend that leverages OpenAI Agents SDK and an MCP server to provide natural language todo management capabilities. The solution will maintain user data isolation through JWT authentication and persist conversation history in the database.

**Objectives:**
- Implement stateless chat endpoint at `/api/{user_id}/chat`
- Build MCP server with 5 standardized tools for todo operations
- Integrate OpenAI Agents SDK for natural language processing
- Maintain data isolation and security per constitution-phase3.md
- Ensure seamless user experience with OpenAI ChatKit frontend

## 2. High-Level Architecture

### Monorepo Structure Update
- Add `mcp/` folder containing the MCP server implementation
- Maintain separation between `frontend/`, `backend/`, and `mcp/` folders
- Update package management to handle dependencies across all components

### System Components Diagram
```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   OpenAI        │    │                  │    │                  │
│   ChatKit       │◄──►│  FastAPI         │◄──►│  MCP Server      │
│   (Hosted)      │    │  Backend         │    │  (Official SDK)  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                              │                          │
                              ▼                          ▼
                       ┌──────────────────┐    ┌──────────────────┐
                       │   Neon           │    │   Existing       │
                       │   PostgreSQL     │    │   Services       │
                       │   (Shared DB)    │    │   (Auth, etc.)   │
                       └──────────────────┘    └──────────────────┘
```

### Chat Flow Process
1. User sends natural language message via ChatKit
2. Frontend makes authenticated request to `/api/{user_id}/chat`
3. Backend verifies JWT and extracts user_id
4. OpenAI Agent processes message and determines intent
5. Agent calls appropriate MCP tool via internal communication
6. MCP tool performs database operation on user's data
7. Result returned to agent
8. Agent formats response and sends back to user
9. Conversation history saved to database with user_id isolation

### AI Agent + MCP Tools Flow
- Natural language input → Intent recognition → Tool selection
- Tool execution → Database operations → Result formatting
- Context maintenance across conversation turns

## 3. Database Design & Models

### Conversation Model
- `id`: UUID primary key
- `user_id`: UUID foreign key to users table (enforces isolation)
- `title`: String (generated from first message or user input)
- `created_at`: DateTime
- `updated_at`: DateTime
- Indexes: user_id for efficient user-specific queries

### Message Model
- `id`: UUID primary key
- `conversation_id`: UUID foreign key to conversations
- `role`: String (user/assistant/system)
- `content`: Text (message content)
- `timestamp`: DateTime
- `tool_calls`: JSONB (for tool call history)
- `tool_responses`: JSONB (for tool call results)
- Indexes: conversation_id for conversation retrieval

### Integration with Existing Tables
- Link messages and conversations to existing users table via user_id
- Maintain relationship with existing tasks table through MCP tools
- Ensure all queries include user_id filters for security

### Migration Strategy
- Use Alembic for database migrations
- Create conversation and message tables in new migration
- Update existing models with necessary indexes
- Plan rollback strategy for safe deployment

## 4. Authentication Integration

### JWT Token Handling
- Verify JWT token from Authorization header in `/api/{user_id}/chat`
- Extract user_id from token claims
- Validate token signature using BETTER_AUTH_SECRET
- Return 401 for invalid/missing tokens

### User_ID Validation
- Compare user_id in URL path with user_id from JWT token
- Prevent users from accessing other users' conversations
- Apply user_id filter to all database queries in chat endpoint
- Log authentication violations for security monitoring

### Token Refresh Strategy
- Handle token expiration gracefully
- Provide clear error messages for expired tokens
- Integrate with Better Auth refresh mechanisms

## 5. MCP Server Implementation

### 5 Tools Registration
- **add_task**: Create new task from natural language
- **list_tasks**: Retrieve user's tasks with filtering
- **complete_task**: Mark task as completed
- **delete_task**: Remove task from user's list
- **update_task**: Modify existing task properties

### Stateless Tool Design
- Each tool call is independent with full context
- No server-side session state maintained
- Tools receive user_id context from authentication layer
- Tools operate only on user's data with user_id validation

### MCP Endpoint Setup
- Run MCP server on separate port/endpoint
- Configure tool discovery and registration
- Implement proper error handling and logging
- Set up health checks for MCP server

## 6. Chat Endpoint Implementation

### Stateless Design
- `/api/{user_id}/chat` accepts conversation context in request
- No server-side session storage
- All necessary context passed in request body
- Response includes updated conversation context

### Conversation History Management
- Fetch recent conversation history before processing
- Append user message to conversation
- Save AI response to conversation after processing
- Limit history length to prevent performance issues

### OpenAI Agents SDK Integration
- Initialize agent with system instructions
- Register MCP tools with agent
- Process user input through agent
- Handle tool calls and responses appropriately

### Tool Calling & Response Formatting
- Map natural language to appropriate tool calls
- Format tool responses for natural language output
- Handle tool errors and provide user-friendly messages
- Maintain conversation context across tool interactions

## 7. OpenAI ChatKit Frontend Setup

### Hosted ChatKit Integration
- Configure ChatKit with backend API endpoint
- Set up custom authentication headers
- Customize chat interface to match application branding
- Implement proper error handling for API failures

### Domain Allowlist Configuration
- Configure CORS settings to allow ChatKit domains
- Add ChatKit URLs to authentication allowlist
- Ensure secure token transmission to hosted service
- Test cross-origin request handling

### JWT Token Attachment
- Implement token injection mechanism for ChatKit requests
- Securely transmit JWT tokens to backend
- Handle token refresh scenarios
- Implement fallback authentication if needed

## 8. Agent Behavior & Natural Language Mapping

### Intent Recognition
- Train agent to recognize add/list/complete/delete/update intents
- Implement confidence threshold for intent classification
- Handle ambiguous requests with clarification
- Support natural language variations for each intent

### Tool Selection Logic
- Map recognized intents to appropriate MCP tools
- Validate required parameters before tool calls
- Handle missing information with follow-up questions
- Implement fallback strategies for unrecognized commands

### Clarification Questions
- Detect when user input lacks required information
- Generate appropriate follow-up questions
- Support natural follow-up responses from users
- Maintain context during clarification dialogs

### Confirmation Messages
- Generate natural language confirmations for successful operations
- Format tool responses for user-friendly presentation
- Provide feedback for all user actions
- Maintain conversational tone throughout interactions

## 9. Testing Strategy

### Unit Testing
- Test individual functions in MCP tools
- Test authentication and user_id validation
- Test database model operations
- Test agent configuration and tool registration

### Integration Testing
- Test end-to-end chat flow
- Test MCP tool integration with database
- Test authentication middleware
- Test error handling scenarios

### E2E Testing
- Test complete user journey from ChatKit to database
- Test conversation history persistence
- Test user data isolation
- Test authentication flow

### Tool Testing
- Test each MCP tool individually
- Test tool error handling
- Test tool parameter validation
- Test tool response formatting

### Conversation Flow Testing
- Test multi-turn conversations
- Test context maintenance
- Test conversation history limits
- Test concurrent conversations

### Coverage Goals
- Achieve 80%+ test coverage for new code
- Focus on critical paths for data isolation
- Test error scenarios thoroughly
- Maintain coverage during refactoring

## 10. Deployment & Environment Setup

### Backend + MCP Deployment
- Deploy FastAPI backend with proper scaling
- Deploy MCP server separately or alongside backend
- Configure load balancing if needed
- Set up monitoring and logging

### ChatKit Hosted URL
- Configure production ChatKit instance
- Set up custom domain if needed
- Configure SSL certificates
- Set up DNS and routing

### Environment Variables
- `BETTER_AUTH_SECRET`: Authentication secret for JWT
- `OPENAI_API_KEY`: API key for OpenAI services
- `DATABASE_URL`: Connection string for Neon PostgreSQL
- `MCP_SERVER_URL`: URL for MCP server communication
- `JWT_ALGORITHM`: Algorithm used for token signing
- `ACCESS_TOKEN_EXPIRES_MINUTES`: Token expiration time

### Security Configuration
- Restrict environment variable access
- Use secrets management for sensitive data
- Configure firewall rules for service communication
- Set up audit logging for security monitoring