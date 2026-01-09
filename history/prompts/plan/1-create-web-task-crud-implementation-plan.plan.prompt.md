---
id: 1
title: Create Web Task CRUD Implementation Plan
stage: plan
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: web-task-crud
branch: master
user: Claude
command: sp.plan
labels: [architecture, planning, crud, authentication]
links:
  spec: specs/features/web-task-crud.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/plans/web-task-crud-plan.md
tests:
  - specs/plans/web-task-crud-plan.md reviewed for completeness
---

## Prompt

You are an expert software architect specializing in full-stack Spec-Driven Development.

We have completed:
- constitution-phase2.md
- specs/features/web-task-crud.md (feature spec with auth + CRUD)

Now create the detailed implementation plan: specs/plans/web-task-crud-plan.md

This plan MUST:
- Be specific to Phase 2 stack (Next.js 16+ App Router, TypeScript, Tailwind, FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT)
- Reference constitution-phase2.md and web-task-crud.md
- NOT contain any actual code snippets or file contents
- Focus on HOW to achieve the WHAT from the spec

Structure the plan exactly as follows:

# Implementation Plan: Web Task CRUD Operations with Authentication

## 1. Overview & Objectives
(What this plan achieves, alignment with spec)

## 2. High-Level Architecture
- Monorepo structure (folders, CLAUDE.md files)
- Frontend/Backend separation diagram (text-based)
- Authentication flow diagram (text-based)

## 3. Database Design & Migration Strategy
- Tables (users, tasks) with relationships
- Indexes
- Migration tool recommendation (alembic for FastAPI)

## 4. Authentication Implementation
- Better Auth setup on frontend (signup/signin)
- JWT issuance & configuration
- Shared BETTER_AUTH_SECRET handling
- FastAPI middleware for JWT verification & user_id extraction

## 5. API Implementation Approach
- FastAPI structure (main.py, routes, dependencies)
- User_id path parameter validation
- Task filtering by authenticated user
- Pydantic models for requests/responses

## 6. Frontend Implementation Approach
- Next.js App Router pages & layouts
- Authentication pages (signup/signin)
- Task list page, create/edit forms
- API client with JWT attachment (fetch/axios)
- Responsive UI with Tailwind

## 7. Security Implementation
- JWT validation, expiration, user isolation
- CORS configuration
- Input sanitization
- Rate limiting (optional)

## 8. Testing Strategy
- Frontend: Jest + React Testing Library
- Backend: pytest + integration tests
- E2E: Playwright/Cypress
- Coverage goals

## 9. De

## Response snapshot

# Implementation Plan: Web Task CRUD Operations with Authentication

## Technical Context

### System Architecture
- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python 3.10+, async support
- **Database**: Neon PostgreSQL (managed service), SQLModel ORM
- **Authentication**: Better Auth with JWT tokens
- **Environment**: Monorepo structure with frontend/backend separation

### Dependencies & Integration Points
- **Frontend dependencies**: Next.js, React, TypeScript, Tailwind CSS, SWR/react-query
- **Backend dependencies**: FastAPI, SQLModel, Pydantic, uvicorn, alembic
- **Authentication**: Better Auth integration with shared BETTER_AUTH_SECRET
- **Database**: Neon PostgreSQL connection, migration tool (alembic)

### Known Unknowns
- Specific BETTER_AUTH_SECRET generation and management process
- Exact CORS configuration for development vs production
- Performance benchmarks for API response times
- Rate limiting configuration details

### Constraints
- All user data must be isolated using user_id in API paths
- JWT tokens must expire after 24 hours with refresh capability
- API endpoints must follow /api/{user_id}/tasks pattern
- Test coverage minimum 80% for new features
- No cross-user data access possible

## Constitution Check

### Spec-Driven Development Compliance
- [x] Feature spec exists at specs/features/web-task-crud.md
- [x] Implementation plan follows spec requirements
- [x] No code implementation without corresponding spec entry

### Full-Stack Monorepo Architecture
- [x] Frontend in frontend/ folder, Backend in backend/ folder
- [x] Clear separation between frontend and backend code
- [x] No cross-dependency violations planned

### Test-First Approach
- [x] Testing strategy includes unit, integration, and E2E tests
- [x] Minimum 80% coverage goal defined
- [x] Critical paths will have 100% coverage

### User Isolation & Security-First
- [x] User_id in API paths for data isolation (/api/{user_id}/tasks)
- [x] Authentication required for all endpoints
- [x] JWT token validation and user_id extraction planned
- [x] Database queries will filter by user_id

### Stateless Architecture
- [x] Backend services designed as stateless
- [x] JWT tokens handle authentication state
- [x] Frontend manages UI state independently

### API-First Design
- [x] REST API design with consistent patterns
- [x] Proper HTTP status codes planned (200/201/400/401/404/500)
- [x] Clear request/response contracts defined

## 1. Overview & Objectives
This plan implements a multi-user task management system with secure authentication and authorization as specified in the feature spec. The implementation will follow the Phase 2 stack using Next.js 16+ App Router, FastAPI, SQLModel, Neon PostgreSQL, and Better Auth with JWT tokens. The system will ensure data isolation between users, with each user only able to access their own tasks. The implementation aligns with the project constitution by following spec-driven development, test-first approach, and security-first principles.

## 2. High-Level Architecture
- **Monorepo structure**:
  ```
  project/
  ├── frontend/           # Next.js application
    ├── app/           # App Router pages
    ├── components/    # React components
    ├── lib/          # Shared utilities
    └── public/       # Static assets
  ├── backend/          # FastAPI application
    ├── api/         # API routes
    ├── models/      # SQLModel definitions
    ├── auth/        # Authentication logic
    └── tests/       # Backend tests
  ├── .specify/        # Spec-Kit Plus configuration
  ├── specs/          # Feature specifications
  └── history/        # PHRs and ADRs
  ```

- **Frontend/Backend separation**:
  - Frontend: Next.js 16+ App Router with TypeScript and Tailwind CSS
  - Backend: FastAPI with SQLModel and Neon PostgreSQL
  - API communication via REST endpoints with JWT authentication

- **Authentication flow**:
  - User authenticates via Better Auth
  - JWT token issued with user_id claim
  - Token sent with each API request in Authorization header
  - Backend validates JWT and extracts user_id for data isolation

## 3. Database Design & Migration Strategy
- **Tables**:
  - `users` table: id (UUID), email (VARCHAR), password_hash (VARCHAR), timestamps
  - `tasks` table: id (UUID), user_id (UUID FK), title (VARCHAR), description (TEXT), completed (BOOLEAN), timestamps
  - Foreign key constraint: tasks.user_id → users.id with CASCADE delete
  - Indexes: idx_tasks_user_id on user_id, idx_tasks_completed on completed status

- **Migration tool**: Alembic for FastAPI database migrations
  - Auto-generate migration scripts from SQLModel model changes
  - Apply migrations in deployment pipeline
  - Support for rollback and version tracking

## 4. Authentication Implementation
- **Better Auth setup**:
  - Configure Better Auth on frontend with signup/signin pages
  - Set up JWT issuance with user_id claim and 24-hour expiration
  - Share BETTER_AUTH_SECRET between frontend and backend via environment variables
  - Implement secure token storage and retrieval

- **FastAPI middleware**:
  - Create JWT verification middleware to validate tokens
  - Extract user_id from JWT claims
  - Verify token expiration and signature
  - Return 401 for invalid tokens

## 5. API Implementation Approach
- **FastAPI structure**:
  - main.py: Application entry point with CORS configuration
  - api/routes: Separate modules for auth and task endpoints
  - api/dependencies: JWT validation and user_id extraction functions
  - models/: SQLModel definitions for users and tasks

- **User_id path parameter validation**:
  - Validate user_id in URL path matches authenticated user from JWT
  - Return 403 for mismatched user access attempts
  - Use UUID validation for path parameters

- **Task filtering by authenticated user**:
  - All database queries filter tasks by authenticated user_id
  - Prevent cross-user data access through query-level filtering
  - Implement repository pattern for data access abstraction

- **Pydantic models**:
  - Request models for input validation
  - Response models for consistent API output
  - DTOs for data transfer between layers

## 6. Frontend Implementation Approach
- **Next.js App Router**:
  - Layouts for authenticated vs unauthenticated users
  - Protected routes for task management pages
  - Server components for data fetching where appropriate
  - Client components for interactive UI elements

- **Authentication pages**:
  - Signup form with email and password validation
  - Signin form with credential validation
  - Error handling and user feedback
  - Redirect after successful authentication

- **Task management pages**:
  - Task list page with pagination and filtering
  - Create task form with validation
  - Edit task form with pre-populated values
  - Delete confirmation dialogs

- **API client**:
  - Centralized API client with JWT attachment
  - Consistent error handling across all requests
  - Loading states and user feedback
  - Retry logic for failed requests

- **Responsive UI**:
  - Tailwind CSS for responsive design
  - Mobile-first approach with breakpoints
  - Accessible components with proper ARIA attributes
  - Loading and error states

## 7. Security Implementation
- **JWT validation**:
  - Verify token signature and expiration
  - Secure token storage and transmission
  - Reasonable expiration times with refresh mechanism

- **User isolation**:
  - Validate user_id in path matches authenticated user
  - Database queries always filter by user_id
  - Return 403 for unauthorized access attempts

- **CORS configuration**:
  - Whitelist frontend domain explicitly
  - Allow credentials only for trusted origins
  - No wildcard origins in production

- **Input sanitization**:
  - Pydantic validation for all API inputs
  - SQL injection prevention via ORM
  - XSS prevention with proper escaping

- **Rate limiting**:
  - Limit API requests per IP address
  - Prevent abuse and brute force attacks

## 8. Testing Strategy
- **Frontend testing**:
  - Jest + React Testing Library for unit tests
  - Component testing for UI elements
  - Integration tests for API interactions
  - Accessibility testing for components

- **Backend testing**:
  - pytest for unit and integration tests
  - Database transaction tests
  - Authentication flow tests
  - Error handling tests

- **E2E testing**:
  - Playwright or Cypress for critical user flows
  - Authentication and task CRUD operations
  - Cross-user access prevention tests

- **Coverage goals**:
  - Minimum 80% test coverage for new features
  - Critical paths 100% covered
  - Mutation testing for complex business logic

## 9. Deployment & DevOps Strategy
- **Environment management**:
  - Separate environment variables for dev/staging/prod
  - Secure handling of secrets (BETTER_AUTH_SECRET, database URLs)
  - Configuration management across environments

- **Database migrations**:
  - Automated migration application in deployment pipeline
  - Backup strategies before schema changes
  - Rollback procedures for failed migrations

- **Health checks**:
  - API endpoint for system health monitoring
  - Database connectivity checks
  - Authentication service availability

- **Monitoring & observability**:
  - Structured logging for debugging
  - Performance monitoring for API endpoints
  - Error tracking and alerting

## 10. Implementation Phases & Milestones
- **Phase 1**: Authentication setup (Better Auth integration, JWT configuration)
- **Phase 2**: Database models and migrations (SQLModel, Alembic setup)
- **Phase 3**: Backend API endpoints (FastAPI routes for tasks)
- **Phase 4**: Frontend authentication pages (signup/signin)
- **Phase 5**: Frontend task management UI (CRUD operations)
- **Phase 6**: Security hardening and testing (validation, security checks)
- **Phase 7**: Performance optimization and deployment preparation

## 11. Risk Analysis & Mitigation
- **Top Risks**:
  1. Authentication vulnerabilities - Mitigation: Follow JWT best practices, input validation
  2. Data isolation failures - Mitigation: Multiple validation layers, thorough testing
  3. Performance degradation - Mitigation: Proper indexing, query optimization

- **Blast radius**: Limited to individual user data due to user_id isolation
- **Kill switches**: API rate limiting, authentication service disable capability

## Outcome

- ✅ Impact: Created comprehensive implementation plan for web task CRUD with authentication that aligns with project constitution and feature spec
- 🧪 Tests: Plan reviewed for completeness and constitution compliance
- 📁 Files: specs/plans/web-task-crud-plan.md created successfully
- 🔁 Next prompts: Implementation can now proceed based on this plan
- 🧠 Reflection: Plan addresses all required aspects and includes technical context and constitution check as required

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Plan meets all requirements
- Prompt variant (if applicable): Standard plan creation prompt
- Next experiment (smallest change to try): Begin implementation following the plan