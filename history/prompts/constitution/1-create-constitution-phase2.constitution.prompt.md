---
id: 1
title: Create constitution-phase2.md
stage: constitution
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: LENOVO
command: /sp.constitution
labels: [constitution,spec-driven,full-stack]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution-phase2.md
tests:
---

## Prompt

You are an expert in Spec-Driven Development for full-stack applications.

Create constitution-phase2.md for Phase 2: Full-Stack Todo Web App (monorepo with Next.js frontend + FastAPI backend).

Base it on Phase 1 constitution (in-memory CLI), but update for:
- Frontend: Next.js 16+ App Router, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, Neon PostgreSQL
- Auth: Better Auth + JWT (shared BETTER_AUTH_SECRET)
- Monorepo: frontend/ and backend/ folders
- Spec-Kit Plus: .spec-kit/config.yaml, organized specs folder
- Multiple CLAUDE.md (root, frontend, backend)
- API: REST endpoints under /api/{user_id}/tasks with JWT
- User isolation, stateless auth
- No manual coding – all via Claude Code

Structure:
# Project Constitution - Phase 2: Full-Stack Todo Web App

## 1. Core Philosophy & Principles
## 2. Technology & Tooling Constraints
## 3. Code Quality & Style Rules (frontend + backend)
## 4. Architecture & Design Decisions (monorepo, auth flow)
## 5. Security & Safety Rules (JWT, CORS, user isolation)
## 6. Testing & Validation Expectations
## 7. Documentation Requirements
## 8. Spec-Driven Workflow Rules (Spec-Kit referencing)
## 9. Phase 2 Specific Constraints
## 10. Compliance & Enforcement

Keep unchanged Phase 1 rules, add/update for Phase 2.
Use bullets, tables, code blocks.
Output ONLY the complete constitution-phase2.md content – start directly with heading.

## Response snapshot

# Project Constitution - Phase 2: Full-Stack Todo Web App

## 1. Core Philosophy & Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All features must be specified before implementation using Spec-Kit Plus templates (spec.md, plan.md, tasks.md). No code written without corresponding spec entry. Requirements clearly defined, acceptance criteria measurable, implementation plan approved before coding begins.

### II. Full-Stack Monorepo Architecture
Frontend (Next.js 16+ App Router) and Backend (FastAPI) coexist in single repository with clear separation. Frontend in `frontend/` folder, Backend in `backend/` folder. Shared types and API contracts defined in common interfaces. No cross-dependency violations between frontend and backend code.

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. Unit tests for all business logic, integration tests for API endpoints, E2E tests for critical user flows. Coverage minimum 80% for new features.

### IV. User Isolation & Security-First
Every user's data completely isolated via user_id in API paths (/api/{user_id}/tasks). No cross-user data access possible. Authentication required for all endpoints. JWT tokens validated, session management secure. Data protection by design, not afterthought.

### V. Stateless Architecture
Backend services stateless, no session storage on server. JWT tokens handle authentication state. Frontend manages UI state independently. API endpoints idempotent where possible. Caching strategies respect user boundaries and security requirements.

### VI. API-First Design
REST API design with consistent patterns: /api/{user_id}/tasks for all operations. Clear request/response contracts. Versioning strategy for future changes. Proper HTTP status codes (200/201/400/401/404/500). Error responses consistent format with user-friendly messages.

## 2. Technology & Tooling Constraints

### Frontend Stack
- Next.js 16+ with App Router (not Pages Router)
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

### Authentication & Security
- Better Auth for authentication system
- Shared BETTER_AUTH_SECRET across frontend/backend
- JWT tokens for stateless authentication
- Secure session management
- CORS properly configured for frontend domain

### Monorepo Structure
```
project/
├── frontend/           # Next.js application
│   ├── app/           # App Router pages
│   ├── components/    # React components
│   ├── lib/          # Shared utilities
│   └── public/       # Static assets
├── backend/          # FastAPI application
│   ├── api/         # API routes
│   ├── models/      # SQLModel definitions
│   ├── auth/        # Authentication logic
│   └── tests/       # Backend tests
├── .specify/        # Spec-Kit Plus configuration
├── specs/          # Feature specifications
└── history/        # PHRs and ADRs
```

## 3. Code Quality & Style Rules (frontend + backend)

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

### Cross-Stack Rules
- API contracts defined with OpenAPI
- Shared type definitions where appropriate
- Consistent naming conventions
- Proper documentation for public APIs
- Security validation on all inputs

## 4. Architecture & Design Decisions (monorepo, auth flow)

### API Architecture
- REST endpoints under `/api/{user_id}/tasks`
- User isolation via user_id in path parameter
- JWT validation middleware for authentication
- SQLModel models for database operations
- Repository pattern for data access abstraction

### Authentication Flow
1. User authenticates via Better Auth
2. JWT token issued with user_id claim
3. Token stored securely in frontend
4. Token sent with each API request
5. Backend validates JWT and extracts user_id
6. User_id used for data isolation in queries

### Database Design
- Neon PostgreSQL for managed service
- SQLModel for type-safe queries
- Proper indexing for performance
- Foreign key constraints for data integrity
- Migration strategy for schema changes

## 5. Security & Safety Rules (JWT, CORS, user isolation)

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

### Input Validation
- All API inputs validated with Pydantic
- SQL injection prevention via ORM
- XSS prevention with proper escaping
- Rate limiting for API endpoints

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

### Test Coverage
- Minimum 80% coverage for new features
- Critical paths 100% covered
- Mutation testing for complex logic
- Performance tests for API endpoints

## 7. Documentation Requirements

### Code Documentation
- JSDoc/Docstrings for all public functions
- API endpoint documentation via FastAPI
- Component usage documentation
- Architecture decision records (ADRs)

### Project Documentation
- Setup and deployment guides
- API reference documentation
- Environment variable documentation
- Security configuration guides

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

## 9. Phase 2 Specific Constraints

### No Manual Coding Rule
- All code generation via Claude Code only
- No hand-written code without proper spec
- Automated generation from specs/tasks
- Manual changes only for debugging purposes

### API Contract Consistency
- All API endpoints follow /api/{user_id}/tasks pattern
- Consistent request/response formats
- Proper error handling and status codes
- Versioning strategy for future changes

### Deployment Constraints
- Frontend and backend deployed separately
- Environment variables properly configured
- Database migrations automated
- Health checks implemented

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

### Violation Handling
- Non-compliant code rejected in review
- Process violations require explanation
- Constitution amendments follow governance procedure
- Regular compliance audits performed

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance. Complexity must be justified. Use CLAUDE.md files for runtime development guidance in root, frontend, and backend folders.

**Version**: 2.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04

## Outcome

- ✅ Impact: Created new constitution-phase2.md file with comprehensive rules for full-stack todo app development
- 🧪 Tests: No tests required for this documentation task
- 📁 Files: Created .specify/memory/constitution-phase2.md with 380+ lines of governance rules
- 🔁 Next prompts: Ready to proceed with Phase 2 implementation following new constitution
- 🧠 Reflection: Constitution properly covers all required aspects for Phase 2 full-stack development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Standard constitution creation prompt
- Next experiment (smallest change to try): Begin implementing Phase 2 features following new constitution