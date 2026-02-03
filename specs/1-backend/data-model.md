# Data Model: Todo Backend System

## Task Entity

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique identifier for each task |
| title | String(255) | Not Null | The title or name of the task |
| description | String(1000) | Nullable | Detailed description of the task |
| completed | Boolean | Not Null, Default: false | Status of task completion |
| user_id | Integer | Not Null, Foreign Key | Reference to the user who owns this task |
| created_at | DateTime | Not Null, Auto-populated | Timestamp when the task was created |
| updated_at | DateTime | Not Null, Auto-populated/Updated | Timestamp when the task was last modified |

### Relationships
- Task belongs to one User (via user_id foreign key)
- User has many Tasks

### Constraints
- `title` must not be empty (length > 0)
- `user_id` must reference an existing user (when user system is implemented)
- `completed` is a boolean value (true/false)

### Indexes
- Index on `user_id` for efficient querying of tasks by user
- Index on `completed` for efficient filtering by completion status
- Composite index on (`user_id`, `completed`) for efficient queries filtering by both user and status

## Validation Rules

### Create Task
- Title is required and must be between 1-255 characters
- Description, if provided, must be between 1-1000 characters
- Completed status defaults to false if not provided
- User ID must be provided and valid

### Update Task
- Title, if provided, must be between 1-255 characters
- Description, if provided, must be between 1-1000 characters
- Completed status, if provided, must be boolean
- User ID cannot be changed (maintains ownership)

### Toggle Completion
- Task must exist and belong to the user
- Completed status is toggled between true/false

## State Transitions

### Task Lifecycle
```
[Created] -(update status)-> [Completed] -(update status)-> [Incomplete]
     |                            |                            |
     |-(update details)            |-(update details)           |-(update details)
     |                            |                            |
     |-(delete)-------------------> [Deleted] <-(delete)--------|
```

### Valid State Changes
- New task: `completed = false` by default
- Task completion: `completed = false` → `completed = true`
- Task reversion: `completed = true` → `completed = false`
- Task deletion: Any state → Deleted (removed from system)

## SQL Schema

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);

-- Foreign key constraint (when user table exists)
-- ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user FOREIGN KEY (user_id) REFERENCES users(id);
```