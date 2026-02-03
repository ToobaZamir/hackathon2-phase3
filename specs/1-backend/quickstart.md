# Quickstart Guide: Todo Backend System

## Prerequisites

- Python 3.11 or higher
- PostgreSQL (Neon Serverless compatible)
- pip package manager
- Virtual environment tool (venv recommended)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@neon-host.region.neon.tech/dbname
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 5. Set Up Database
```bash
# Run database migrations
alembic upgrade head
```

### 6. Start the Application
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## API Usage Examples

### 1. Create a Task
```bash
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the tutorial and build a sample app",
    "completed": false
  }'
```

### 2. Get All Tasks for User
```bash
curl -X GET http://localhost:8000/api/1/tasks
```

### 3. Get Specific Task
```bash
curl -X GET http://localhost:8000/api/1/tasks/1
```

### 4. Update a Task
```bash
curl -X PUT http://localhost:8000/api/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Master FastAPI",
    "completed": true
  }'
```

### 5. Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/api/1/tasks/1/complete \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

### 6. Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/1/tasks/1
```

## Configuration Details

### Environment Variables
- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `SECRET_KEY`: Secret key for cryptographic operations
- `DEBUG`: Enable/disable debug mode (true/false)

### Database Setup
The application uses SQLModel with Alembic for database migrations. After setting up the database connection, run migrations to create the required tables.

### Running Tests
```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run contract tests
pytest tests/contract/
```

## Project Structure
```
src/
├── models/           # SQLModel definitions
│   └── task.py
├── schemas/          # Pydantic schemas for API validation
│   └── task.py
├── database/         # Database connection and session management
│   └── connection.py
├── api/              # API route definitions
│   └── v1/
│       └── tasks.py
├── core/             # Configuration and utilities
│   └── config.py
└── main.py           # FastAPI application entry point

tests/
├── unit/             # Unit tests
├── integration/      # Integration tests
└── contract/         # Contract tests

alembic/              # Database migration files
├── env.py
├── script.py.mako
└── versions/
```

## Development Commands

### Setting up Development Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks (if configured)
pre-commit install
```

### Running in Development Mode
```bash
# With auto-reload
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# With logging
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level info
```

### Building for Production
```bash
# The application is ready for deployment as-is with uvicorn
# Or use gunicorn for production:
gunicorn src.main:app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify DATABASE_URL is correctly set in environment
   - Check that the Neon PostgreSQL database is accessible
   - Ensure required SSL certificates are available

2. **Migration Issues**
   - Run `alembic revision --autogenerate -m "Initial migration"` to create new migration
   - Run `alembic upgrade head` to apply all migrations

3. **Dependency Issues**
   - Recreate virtual environment if experiencing import errors
   - Update requirements.txt if new dependencies were added

### Useful Commands
```bash
# Check installed packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade

# Format code (if black is installed)
black src/

# Check code style (if flake8 is installed)
flake8 src/
```