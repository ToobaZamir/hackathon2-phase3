# API Contracts: Todo Backend System

## Base URL
```
https://api.example.com/api/{user_id}
```

## Authentication
All endpoints require authentication through the user_id in the URL path. (Authentication mechanism to be implemented in future phase)

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional descriptive message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Descriptive error message",
    "details": { /* optional error details */ }
  }
}
```

## Endpoints

### 1. Get All Tasks
```
GET /api/{user_id}/tasks
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user whose tasks to retrieve

#### Query Parameters
- `completed` (boolean, optional): Filter tasks by completion status
- `limit` (integer, optional): Maximum number of tasks to return (default: 50, max: 100)
- `offset` (integer, optional): Number of tasks to skip (for pagination)

#### Responses
- `200 OK`: Successfully retrieved tasks
- `400 Bad Request`: Invalid query parameters
- `404 Not Found`: User ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Complete project",
        "description": "Finish the todo backend implementation",
        "completed": false,
        "user_id": 123,
        "created_at": "2026-01-09T10:00:00Z",
        "updated_at": "2026-01-09T10:00:00Z"
      },
      {
        "id": 2,
        "title": "Review code",
        "description": "Review the implementation with team",
        "completed": true,
        "user_id": 123,
        "created_at": "2026-01-09T09:30:00Z",
        "updated_at": "2026-01-09T11:15:00Z"
      }
    ],
    "total": 2
  }
}
```

### 2. Create Task
```
POST /api/{user_id}/tasks
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user creating the task

#### Request Body
```json
{
  "title": "Task title (required, string, max 255 chars)",
  "description": "Task description (optional, string, max 1000 chars)",
  "completed": false
}
```

#### Responses
- `201 Created`: Task created successfully
- `400 Bad Request`: Invalid request body or validation errors
- `404 Not Found`: User ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "id": 3,
    "title": "New task",
    "description": "Task description",
    "completed": false,
    "user_id": 123,
    "created_at": "2026-01-09T12:00:00Z",
    "updated_at": "2026-01-09T12:00:00Z"
  },
  "message": "Task created successfully"
}
```

### 3. Get Single Task
```
GET /api/{user_id}/tasks/{id}
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user
- `id` (integer, required): The ID of the task to retrieve

#### Responses
- `200 OK`: Task retrieved successfully
- `404 Not Found`: Task or user ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the todo backend implementation",
    "completed": false,
    "user_id": 123,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T10:00:00Z"
  }
}
```

### 4. Update Task
```
PUT /api/{user_id}/tasks/{id}
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user
- `id` (integer, required): The ID of the task to update

#### Request Body
```json
{
  "title": "Updated task title (optional, string, max 255 chars)",
  "description": "Updated task description (optional, string, max 1000 chars)",
  "completed": true
}
```

#### Responses
- `200 OK`: Task updated successfully
- `400 Bad Request`: Invalid request body or validation errors
- `404 Not Found`: Task or user ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "user_id": 123,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T13:00:00Z"
  },
  "message": "Task updated successfully"
}
```

### 5. Delete Task
```
DELETE /api/{user_id}/tasks/{id}
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user
- `id` (integer, required): The ID of the task to delete

#### Responses
- `200 OK`: Task deleted successfully
- `404 Not Found`: Task or user ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### 6. Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
```

#### Path Parameters
- `user_id` (integer, required): The ID of the user
- `id` (integer, required): The ID of the task to toggle

#### Request Body
```json
{
  "completed": true
}
```

#### Responses
- `200 OK`: Task completion status updated successfully
- `400 Bad Request`: Invalid request body
- `404 Not Found`: Task or user ID does not exist
- `500 Internal Server Error`: Server error

#### Success Response Example
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the todo backend implementation",
    "completed": true,
    "user_id": 123,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T14:00:00Z"
  },
  "message": "Task completion status updated"
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_INPUT` | 400 | Request body contains invalid data |
| `TASK_NOT_FOUND` | 404 | Requested task does not exist |
| `USER_NOT_FOUND` | 404 | Requested user does not exist |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INTERNAL_ERROR` | 500 | Internal server error occurred |
| `UNAUTHORIZED` | 403 | User not authorized to access resource |
| `NOT_FOUND` | 404 | Resource not found |

## Validation Rules

### Task Creation/Update
- Title: Required, 1-255 characters
- Description: Optional, 0-1000 characters
- Completed: Boolean value (true/false)
- User ID: Integer, must match authenticated user

### Task ID Validation
- Must be a positive integer
- Must exist in the database
- Must belong to the requesting user