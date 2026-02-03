# Todo Backend System

A RESTful API for managing todo tasks with persistent storage, built with Python FastAPI and SQLModel.

## Features

- Full CRUD operations for todo tasks
- Multi-user support with user isolation
- Persistent storage with Neon PostgreSQL
- RESTful API design with proper HTTP status codes
- Data validation and error handling
- Task completion status management
- Health check endpoints
- Database connection pooling

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (Neon Serverless compatible)
- **Python Version**: 3.11+

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env .env.local
   # Edit .env.local with your database configuration
   ```

## Database Setup

1. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Task Management

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check for the main application
- `GET /api/{user_id}/health` - Health check for the task service

## Environment Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `SECRET_KEY` - Secret key for security (default: dev-secret-key-change-in-production)
- `ENVIRONMENT` - Environment (development/production, default: development)
- `DEBUG` - Enable/disable debug mode (default: True)

## Development

1. Run tests:
   ```bash
   pytest
   ```

2. Format code:
   ```bash
   black src/
   isort src/
   ```

## Project Structure

```
├── src/
│   ├── models/           # SQLModel definitions
│   ├── schemas/          # Pydantic schemas for API validation
│   ├── database/         # Database connection and session management
│   ├── api/              # API route definitions
│   ├── services/         # Business logic
│   └── core/             # Configuration and utilities
├── tests/                # Test files
├── alembic/              # Database migration files
├── requirements.txt      # Python dependencies
├── alembic.ini           # Alembic configuration
└── .env                  # Environment variables template
```

## API Response Format

Successful responses follow this format:
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional descriptive message"
}
```

Error responses follow this format:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Descriptive error message"
  }
}
```