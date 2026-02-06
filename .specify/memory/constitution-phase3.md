<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Modified principles: Full-Stack Monorepo Architecture → AI-Powered Chat Interface Architecture, Phase 2 Specific Constraints → Phase 3 Specific Constraints
Added sections: MCP Server Integration, AI Logic Architecture, Conversation Management
Removed sections: None
Templates requiring updates: ⚠ pending (plan-template.md, spec-template.md, tasks-template.md)
Follow-up TODOs: None
-->

# Project Constitution - Phase 3: AI-Powered Todo Chatbot

## 1. Core Philosophy & Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All features must be specified before implementation using Spec-Kit Plus templates (spec.md, plan.md, tasks.md). No code written without corresponding spec entry. Requirements clearly defined, acceptance criteria measurable, implementation plan approved before coding begins.

### II. AI-Powered Chat Interface Architecture
Frontend (OpenAI ChatKit hosted solution) and Backend (FastAPI) coexist in single repository with clear separation. Frontend in `frontend/` folder, Backend in `backend/` folder. MCP server in `mcp/` folder. AI logic integrated via OpenAI Agents SDK. No cross-dependency violations between frontend, backend, and MCP server code.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. Unit tests for all business logic, integration tests for API endpoints, E2E tests for critical user flows. Coverage minimum 80% for new features.

### IV. User Isolation & Security-First
Every user's data completely isolated via user_id in API paths (/api/{user_id}/chat). No cross-user data access possible. Authentication required for all endpoints. JWT tokens validated, session management secure. Data protection by design, not afterthought.

### V. Stateless Architecture
Backend services stateless, no session storage on server. JWT tokens handle authentication state. Frontend manages UI state independently. API endpoints idempotent where possible. Caching strategies respect user boundaries and security requirements.

### VI. API-First Design
REST API design with consistent patterns: /api/{user_id}/chat for all operations. Clear request/response contracts. Versioning strategy for future changes. Proper HTTP status codes (200/201/400/401/404/500). Error responses consistent format with user-friendly messages.

## 2. Technology & Tooling Constraints

### Frontend Stack
- OpenAI ChatKit (hosted solution) for chat interface
- TypeScript (strict mode) for all components and logic
- Tailwind CSS for styling (no custom CSS frameworks)
- Client components for interactivity, Server components for data fetching
- SWR/react-query for data fetching and caching

### Backend Stack
- FastAPI for API framework (Pydantic v2, async support)
- SQLModel for database models and queries
- Neon PostgreSQL for managed database service
- Pydantic for request/response validation
- uvicorn for ASGI server

### AI Logic & MCP Server
- OpenAI Agents SDK for AI-powered chatbot logic
- Official MCP SDK for standardized tool integration
- MCP server in `mcp/` folder with 5 core tools: add_task, list_tasks, complete_task, delete_task, update_task
- State management for conversations and messages in database
- Tool calling patterns for task operations

### Authentication & Security
- Better Auth for authentication system
- Shared BETTER_AUTH_SECRET across frontend/backend
- JWT tokens for stateless authentication
- Secure session management
- CORS properly configured for frontend domain

### Monorepo Structure
```
project/
├── frontend/           # OpenAI ChatKit frontend
│   ├── app/           # App Router pages
│   ├── components/    # React components
│   ├── lib/          # Shared utilities
│   └── public/       # Static assets
├── backend/          # FastAPI application
│   ├── api/         # API routes
│   ├── models/      # SQLModel definitions
│   ├── auth/        # Authentication logic
│   ├── ai/          # AI logic and agents
│   └── tests/       # Backend tests
├── mcp/             # MCP server implementation
│   ├── tools/       # MCP tools (add_task, list_tasks, etc.)
│   ├── server/      # MCP server implementation
│   └── tests/       # MCP tests
├── .specify/        # Spec-Kit Plus configuration
├── specs/          # Feature specifications
└── history/        # PHRs and ADRs
```

## 3. Code Quality & Style Rules (frontend + backend + mcp)

### Frontend Quality Rules
- TypeScript strict mode enabled (noImplicitAny, strictNullChecks, etc.)
- ESLint + Prettier configuration enforced
- Component props typed with interfaces
- API calls typed with return types
- No inline styles (Tailwind only)
- Accessibility compliance (ARIA labels, keyboard navigation)

### Backend Quality Rules
- Type hints mandatory for all functions
- FastAPI path operations properly typed
- SQLModel models with validation
- Pydantic schemas for request/response
- Error handling with proper exceptions
- Logging with structured format

### MCP Server Quality Rules
- MCP SDK integration following official patterns
- Type safety for all tool definitions and responses
- Proper error handling for tool operations
- Consistent response formats for all tools
- Validation of tool parameters and results

### Cross-Stack Rules
- API contracts defined with OpenAPI
- Shared type definitions where appropriate
- Consistent naming conventions
- Proper documentation for public APIs
- Security validation on all inputs

## 4. Architecture & Design Decisions (monorepo, auth flow, AI integration)

### API Architecture
- Stateless chat endpoint at `/api/{user_id}/chat`
- User isolation via user_id in path parameter
- JWT validation middleware for authentication
- SQLModel models for database operations
- Repository pattern for data access abstraction

### AI Logic Architecture
- OpenAI Agents SDK for conversation management
- Tool integration via MCP server
- Conversation state stored in database
- Message history persistence for context
- AI response formatting for chat interface

### MCP Server Architecture
- 5 core tools: add_task, list_tasks, complete_task, delete_task, update_task
- Standardized tool calling interface
- Error handling and validation for all tools
- Integration with backend data models
- Authentication and authorization for tool access

### Authentication Flow
1. User authenticates via Better Auth
2. JWT token issued with user_id claim
3. Token stored securely in frontend
4. Token sent with each API request
5. Backend validates JWT and extracts user_id
6. User_id used for data isolation in queries
7. MCP tools inherit authentication context

### Database Design
- Neon PostgreSQL for managed service
- SQLModel for type-safe queries
- Conversation + Message models for chat history
- Proper indexing for performance
- Foreign key constraints for data integrity
- Migration strategy for schema changes

## 5. Security & Safety Rules (JWT, CORS, user isolation, AI)

### JWT Security
- BETTER_AUTH_SECRET stored in environment variables
- JWT tokens validated with proper algorithms
- Token expiration enforced (reasonable TTL)
- Secure token storage (HTTP-only cookies or secure localStorage)
- Token refresh mechanisms when needed

### CORS Policy
- Frontend domain explicitly whitelisted
- Credentials allowed only for trusted origins
- Proper header validation
- No wildcard origins in production

### Data Isolation
- User_id validation on every request
- Database queries always filtered by user_id
- No cross-user data access possible
- Proper authorization checks for all operations
- Conversation isolation by user

### Input Validation
- All API inputs validated with Pydantic
- SQL injection prevention via ORM
- XSS prevention with proper escaping
- Rate limiting for API endpoints
- AI prompt sanitization and validation

### AI Safety
- Prompt injection prevention
- Response validation and sanitization
- Tool usage monitoring and limits
- Safe guardrails for sensitive operations
- Content filtering for inappropriate requests

## 6. Testing & Validation Expectations

### Frontend Testing
- Unit tests for React components (Jest + React Testing Library)
- Integration tests for API interactions
- E2E tests for critical user flows (Playwright/Cypress)
- Accessibility testing for components

### Backend Testing
- Unit tests for business logic functions
- Integration tests for API endpoints
- Database transaction tests
- Authentication flow tests
- Error handling tests

### AI/MCP Testing
- Unit tests for AI agent logic
- Integration tests for MCP tool operations
- End-to-end conversation flow tests
- Tool response validation tests
- Error handling for AI operations

### Test Coverage
- Minimum 80% coverage for new features
- Critical paths 100% covered
- Mutation testing for complex logic
- Performance tests for API endpoints
- AI response time and accuracy tests

## 7. Documentation Requirements

### Code Documentation
- JSDoc/Docstrings for all public functions
- API endpoint documentation via FastAPI
- Component usage documentation
- Architecture decision records (ADRs)
- MCP tool documentation

### Project Documentation
- Setup and deployment guides
- API reference documentation
- Environment variable documentation
- Security configuration guides
- MCP server setup and integration guide

### Spec Documentation
- Feature specifications in specs/ folder
- Implementation plans with architecture decisions
- Testable tasks with acceptance criteria
- Prompt History Records for all changes

## 8. Spec-Driven Workflow Rules (Spec-Kit referencing)

### Spec Template Usage
- Use `.specify/templates/spec-template.md` for feature specs
- Use `.specify/templates/plan-template.md` for architecture plans
- Use `.specify/templates/tasks-template.md` for implementation tasks
- Maintain consistency with template structure

### Feature Development Flow
1. Create spec.md with requirements and acceptance criteria
2. Create plan.md with architecture and implementation approach
3. Create tasks.md with testable implementation steps
4. Implement following tasks in order
5. Update documentation and create PHR

### Quality Gates
- Spec approved before implementation begins
- Plan reviewed for architectural soundness
- Tasks include test cases and validation steps
- Implementation matches spec exactly

## 9. Phase 3 Specific Constraints

### No Manual Coding Rule
- All code generation via Claude Code only
- No hand-written code without proper spec
- Automated generation from specs/tasks
- Manual changes only for debugging purposes

### AI Integration Requirements
- All AI logic must use OpenAI Agents SDK
- MCP tools must follow standardized interface
- Conversation state must be persisted in database
- AI responses must be formatted for ChatKit
- Tool operations must maintain user isolation

### API Contract Consistency
- All API endpoints follow /api/{user_id}/chat pattern
- Consistent request/response formats
- Proper error handling and status codes
- Versioning strategy for future changes

### Deployment Constraints
- Frontend, backend, and MCP server deployed separately
- Environment variables properly configured
- Database migrations automated
- Health checks implemented
- MCP server connectivity verified

## 10. Compliance & Enforcement

### Code Review Requirements
- All PRs must reference corresponding spec/plan/tasks
- Architecture decisions documented in ADRs
- Security requirements verified
- Test coverage requirements met

### Quality Metrics
- Test coverage minimum 80%
- Code quality scores maintained
- Performance benchmarks met
- Security scanning passed
- AI response accuracy validated

### Violation Handling
- Non-compliant code rejected in review
- Process violations require explanation
- Constitution amendments follow governance procedure
- Regular compliance audits performed

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Use CLAUDE.md files for runtime development guidance in root, frontend, backend, and mcp folders.

**Version**: 3.0.0 | **Ratified**: 2026-01-17 | **Last Amended**: 2026-01-17
