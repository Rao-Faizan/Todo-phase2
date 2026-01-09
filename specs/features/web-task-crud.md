# Feature Specification: Web Task CRUD Operations with Authentication

## 1. Overview & Purpose

This feature implements a multi-user task management system with secure authentication and authorization. Users can create accounts, authenticate with Better Auth, and perform CRUD operations on their personal tasks. The system ensures data isolation between users, with each user only able to access their own tasks. The backend uses JWT tokens for stateless authentication and stores data persistently in Neon PostgreSQL.

## 2. User Stories (with priorities)

| Priority | User Story | Acceptance Criteria |
|----------|------------|-------------------|
| P0 | As a user, I want to create an account so that I can use the task management system | User can complete signup form and receive confirmation |
| P0 | As a user, I want to sign in to my account so that I can access my tasks | User can authenticate with credentials and receive JWT token |
| P0 | As a user, I want to create tasks so that I can track my work | User can submit new task with title and description |
| P0 | As a user, I want to view my tasks so that I can see what I need to do | User can see a list of their tasks with status |
| P0 | As a user, I want to update my tasks so that I can modify their details | User can edit task title, description, and completion status |
| P0 | As a user, I want to delete my tasks so that I can remove completed items | User can remove tasks from their list |
| P0 | As a user, I want to mark tasks as complete so that I can track progress | User can update task completion status |
| P1 | As a user, I want a responsive UI so that I can use the app on any device | Interface adapts to mobile, tablet, and desktop screens |

## 3. Acceptance Criteria (detailed, testable)

### Authentication
- User can sign up with email and password
- User can sign in with existing credentials
- JWT token is issued upon successful authentication
- JWT token is required for all task operations
- Invalid JWT tokens are rejected with 401 status

### Task CRUD Operations
- User can create a task with title (required, max 200 chars) and optional description
- User can retrieve all their tasks in a paginated format (default 10 per page)
- User can retrieve a specific task by ID
- User can update task properties (title, description, completion status)
- User can mark a task as complete/incomplete
- User can delete a specific task
- All operations are restricted to user's own tasks only

### Data Isolation
- User A cannot access User B's tasks
- API validates user_id in path matches authenticated user
- Database queries always filter by user_id
- Unauthorized access attempts return 403 status

### Security
- All API endpoints require valid JWT authentication
- Passwords are hashed and never stored in plain text
- Session tokens have reasonable expiration times
- No sensitive data is exposed in error messages

## 4. REST API Specification (endpoints, methods, request/response, auth)

### Authentication Endpoints
```
POST /api/auth/signup
- Request: {email: string, password: string}
- Response: {user: {id: string, email: string}, token: string}
- Auth: None

POST /api/auth/signin
- Request: {email: string, password: string}
- Response: {user: {id: string, email: string}, token: string}
- Auth: None
```

### Task Management Endpoints
```
GET /api/{user_id}/tasks
- Request: None
- Response: {tasks: [{id: string, title: string, description: string, completed: boolean, created_at: timestamp, updated_at: timestamp}]}
- Auth: JWT required
- Query params: page (default 1), limit (default 10)

POST /api/{user_id}/tasks
- Request: {title: string (required, max 200), description: string (optional, max 1000)}
- Response: {task: {id: string, title: string, description: string, completed: boolean, created_at: timestamp, updated_at: timestamp}}
- Auth: JWT required

GET /api/{user_id}/tasks/{task_id}
- Request: None
- Response: {task: {id: string, title: string, description: string, completed: boolean, created_at: timestamp, updated_at: timestamp}}
- Auth: JWT required

PUT /api/{user_id}/tasks/{task_id}
- Request: {title: string (max 200), description: string (max 1000), completed: boolean}
- Response: {task: {id: string, title: string, description: string, completed: boolean, created_at: timestamp, updated_at: timestamp}}
- Auth: JWT required

PATCH /api/{user_id}/tasks/{task_id}/complete
- Request: {completed: boolean}
- Response: {task: {id: string, title: string, description: string, completed: boolean, created_at: timestamp, updated_at: timestamp}}
- Auth: JWT required

DELETE /api/{user_id}/tasks/{task_id}
- Request: None
- Response: {success: boolean}
- Auth: JWT required
```

### HTTP Status Codes
- 200: Success for GET, PUT, PATCH operations
- 201: Success for POST operations (resource created)
- 204: Success for DELETE operations (no content)
- 400: Bad request (validation error)
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user trying to access another user's data)
- 404: Resource not found (task or user doesn't exist)
- 500: Internal server error

## 5. Authentication Flow

1. User accesses the application and chooses to sign up or sign in
2. For sign up:
   - User provides email and password
   - System validates credentials
   - System creates user account with hashed password
   - System generates JWT token with user_id claim
   - Token is returned to frontend
3. For sign in:
   - User provides email and password
   - System validates credentials against stored hash
   - System generates JWT token with user_id claim
   - Token is returned to frontend
4. For subsequent requests:
   - Frontend includes JWT token in Authorization header
   - Backend verifies JWT signature and expiration
   - Backend extracts user_id from token claim
   - Backend validates that user_id matches path parameter
   - Request is processed if all validations pass

## 6. Database Schema (users + tasks tables)

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## 7. Input/Output Examples

### Create Task Request
```json
{
  "title": "Complete project proposal",
  "description": "Finish writing and review the Q1 project proposal document"
}
```

### Create Task Response
```json
{
  "task": {
    "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "title": "Complete project proposal",
    "description": "Finish writing and review the Q1 project proposal document",
    "completed": false,
    "created_at": "2026-01-04T10:30:00Z",
    "updated_at": "2026-01-04T10:30:00Z"
  }
}
```

### Get All Tasks Response
```json
{
  "tasks": [
    {
      "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "title": "Complete project proposal",
      "description": "Finish writing and review the Q1 project proposal document",
      "completed": false,
      "created_at": "2026-01-04T10:30:00Z",
      "updated_at": "2026-01-04T10:30:00Z"
    },
    {
      "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
      "title": "Schedule team meeting",
      "description": "Set up meeting with team for project review",
      "completed": true,
      "created_at": "2026-01-04T09:15:00Z",
      "updated_at": "2026-01-04T11:45:00Z"
    }
  ]
}
```

## 8. Edge Cases & Validation Rules

### Input Validation
- Task title: Required, 1-200 characters, no HTML/script tags
- Task description: Optional, 0-1000 characters, no HTML/script tags
- Email format: Valid email format required
- Password: Minimum 8 characters with at least one uppercase, lowercase, number, and special character

### Business Logic Validation
- Users can only access tasks belonging to their user_id
- Users cannot create more than 100 tasks per day (rate limiting)
- Task ID in URL must match actual task record
- User ID in JWT must match user ID in URL path

### Error Handling
- Invalid JWT returns 401 with "Invalid or expired token" message
- Attempting to access another user's tasks returns 403 with "Access denied" message
- Non-existent task returns 404 with "Task not found" message
- Validation errors return 400 with specific field validation messages

## 9. Non-Functional Requirements (performance, security, usability)

### Performance
- API endpoints respond within 500ms for 95% of requests
- Database queries complete within 200ms for 95% of requests
- Frontend loads within 3 seconds on average mobile connection
- System supports 1000 concurrent users

### Security
- JWT tokens expire after 24 hours (refreshable)
- Passwords use bcrypt hashing with 12 rounds
- All API communication uses HTTPS
- SQL injection prevention through parameterized queries
- XSS prevention through input sanitization
- Rate limiting to prevent abuse (100 requests per minute per IP)

### Usability
- Responsive design works on screen sizes from 320px to 1920px
- Intuitive form validation with clear error messages
- Loading states for all API operations
- Accessible to users with disabilities (WCAG 2.1 AA compliance)
- Clear visual feedback for all user actions

## 10. Out of Scope for Phase 2

### Explicitly Not Included
- Advanced task features (due dates, priorities, categories)
- Sharing tasks with other users
- Team/collaborative features
- Email notifications
- Advanced reporting or analytics
- File attachments to tasks
- Task comments or discussions
- Mobile app (native)
- Offline functionality
- Advanced search or filtering beyond basic pagination
- Admin panel or user management beyond individual user accounts
- Export/import functionality
- Third-party integrations
- Multi-language support
- Advanced authentication methods (2FA, social login beyond Better Auth standard options)