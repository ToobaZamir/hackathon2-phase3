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
DEBUG=True
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

### 7. Health Check
```bash
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/1/health
```

## Validation

To validate that all functionality works as documented:

1. **Start the application** as shown in step 6 above.

2. **Test all CRUD operations** using the curl commands above:
   - Create a task and verify it returns a 200 status with the created task
   - Get all tasks and verify the created task appears in the list
   - Get a specific task and verify its details
   - Update a task and verify the changes are reflected
   - Toggle task completion status and verify the status changes
   - Delete a task and verify it's removed

3. **Test persistence**:
   - Create a task
   - Restart the server
   - Verify the task still exists

4. **Test error handling**:
   - Try to get a non-existent task (should return 404)
   - Try to update a non-existent task (should return 404)
   - Try to delete a non-existent task (should return 404)

5. **Test health endpoints**:
   - Both health endpoints should return healthy status

6. **Run the unit tests**:
   ```bash
   pytest tests/unit/
   ```

All tests should pass, confirming that the functionality works as documented in the specification.