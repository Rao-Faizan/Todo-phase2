# Todo Application - Phase 2

A full-stack todo application with authentication, built using Next.js 16+ (App Router), FastAPI, SQLModel, Neon PostgreSQL, and Better Auth.

## Project Structure

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
│   ├── services/    # Business logic
│   ├── schemas/     # Pydantic schemas
│   └── tests/       # Backend tests
├── .specify/        # Spec-Kit Plus configuration
├── specs/          # Feature specifications
└── history/        # PHRs and ADRs
```

## Getting Started

### Prerequisites

- Node.js 18+ for frontend
- Python 3.10+ for backend
- PostgreSQL (or Neon PostgreSQL for cloud)

### Installation

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Or use the monorepo script:
```bash
npm run install
```

### Environment Variables

Copy the example environment files and configure them:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Update the values in the .env files as needed.

### Running the Application

### Option 1: With Docker (Recommended)

1. Make sure Docker is running on your system
2. Run the application using Docker Compose:
```bash
docker-compose up -d
```
The application will be available at `http://localhost:8000`

To stop the application:
```bash
docker-compose down
```

### Option 2: Local Development

To run both frontend and backend simultaneously:
```bash
npm run dev
```

To run individually:
- Frontend: `npm run dev:frontend` or `cd frontend && npm run dev`
- Backend: `npm run dev:backend` or `cd backend && uvicorn main:app --reload`

## Features

- User authentication with Better Auth
- Secure task management with user isolation
- RESTful API with JWT authentication
- Responsive UI with Tailwind CSS
- Type-safe models with SQLModel and TypeScript

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/signin` - Authenticate user

### Tasks (require authentication)
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task