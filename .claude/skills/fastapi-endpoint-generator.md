---
name: fastapi-endpoint-generator
description: Use this skill to create new FastAPI routes/endpoints with full code - models, dependencies, DB integration, auth, responses, and examples.
when_to_use: Use whenever the user asks to generate, implement, code, or create a FastAPI endpoint, route, API path, chat endpoint, CRUD operation, or mentions "/api/", POST/GET/PUT/DELETE.
invoke_directly: true
---

# FastAPI Endpoint Generator

## Overview

This skill generates complete, production-ready FastAPI endpoint code including:
- Path operations (GET, POST, PUT, PATCH, DELETE)
- Request/Response Pydantic models (v2+)
- Database integration (SQLModel sessions)
- Authentication dependencies (JWT/user_id)
- Error handling (HTTPException with proper status codes)
- Async/await patterns
- Stateless design patterns
- OpenAPI documentation (tags, summaries, descriptions)

Optimized for hackathon projects like **Todo AI Chatbot Phase 3** with MCP tools, OpenAI Agents SDK, and Neon PostgreSQL + SQLModel.

## When to Use This Skill

Invoke `/fastapi-endpoint-generator` when:
- User asks to "create an endpoint", "generate API route", "build FastAPI path"
- User mentions HTTP methods: POST, GET, PUT, DELETE, PATCH
- User references API paths: `/api/tasks`, `/api/chat`, `/api/{user_id}/...`
- User needs CRUD operations for a resource
- User wants to implement the chat endpoint for Phase 3
- User requests "stateless endpoint", "async endpoint", or "authenticated route"

## Required Information (Ask if Missing)

Before generating code, gather these details:

### 1. Endpoint Basics
- **HTTP Method:** GET, POST, PUT, PATCH, DELETE
- **Path:** e.g. `/api/tasks`, `/api/{user_id}/chat`, `/api/tasks/{task_id}`
- **Purpose:** Brief description (e.g., "Create a new task", "Chat with AI agent")

### 2. Request Schema
- **Path Parameters:** e.g. `user_id: int`, `task_id: int`
- **Query Parameters:** e.g. `status: str | None`, `limit: int = 10`
- **Request Body:** Fields and types (e.g., `title: str`, `description: str | None`)

### 3. Response Schema
- **Success Response:** Model fields or dict structure
- **Status Code:** 200 (OK), 201 (Created), 204 (No Content)

### 4. Dependencies
- **Auth Required?** JWT token → `user_id: int = Depends(get_current_user_id)`
- **Database Session?** SQLModel → `session: Session = Depends(get_session)`
- **Other Dependencies:** Rate limiting, role checks, etc.

### 5. Database Interaction
- **Models Involved:** e.g. `Task`, `Conversation`, `Message`
- **Query Type:** SELECT, INSERT, UPDATE, DELETE
- **Relationships:** Join queries, nested objects

### 6. Special Requirements (Phase 3)
- **Agent Integration?** OpenAI Agents SDK with MCP tools
- **Stateless Pattern?** Fetch state from DB, no in-memory storage
- **MCP Tool Calls?** Which tools: `create_task`, `list_tasks`, etc.
- **Conversation Persistence?** Save messages to DB

## Generation Process

### Step 1: Analyze Request
- Parse user's endpoint description
- Identify HTTP method and path
- Determine if stateless/async/authenticated

### Step 2: Ask Clarifying Questions (if needed)
Present missing information as a checklist:
```markdown
To generate this endpoint, I need:
- [ ] HTTP Method (GET/POST/PUT/DELETE)
- [ ] Path (e.g., /api/tasks)
- [ ] Request body schema
- [ ] Response model
- [ ] Auth requirement (JWT user_id?)
- [ ] Database models involved
```

### Step 3: Generate Code Structure

#### A. Import Statements
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.database import get_session
from app.auth import get_current_user_id
from app.models import Task, Conversation, Message  # Adjust as needed
```

#### B. Router Setup
```python
router = APIRouter(prefix="/api", tags=["tasks"])
```

#### C. Request/Response Models
```python
class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high)$")

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
```

#### D. Endpoint Function
```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Creates a new task for the authenticated user"
)
async def create_task(
    request: TaskCreateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task.

    - **title**: Task title (required, 1-200 chars)
    - **description**: Optional task description
    - **priority**: low, medium, or high (default: medium)
    """
    # Business logic
    new_task = Task(
        user_id=user_id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        status="pending"
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return TaskResponse.model_validate(new_task)
```

#### E. Error Handling
```python
# Example: Task not found
task = session.get(Task, task_id)
if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found"
    )

# Example: Unauthorized access
if task.user_id != user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to access this task"
    )
```

### Step 4: Add Stateless Design Notes (if applicable)
For endpoints involving conversation/agent:
```python
# STATELESS DESIGN:
# 1. Fetch full conversation history from DB
# 2. Instantiate fresh agent with MCP tools
# 3. Execute agent with history + new message
# 4. Save agent response to DB
# 5. Return response (no in-memory state)
```

### Step 5: Provide Usage Examples
```bash
# cURL example
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "priority": "high"}'
```

## Real-World Examples

### Example 1: POST /api/tasks - Create Task

**User Request:** "Generate endpoint to create a task"

**Generated Code:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.database import get_session
from app.auth import get_current_user_id
from app.models import Task

router = APIRouter(prefix="/api", tags=["tasks"])

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: str = Field("medium", pattern="^(low|medium|high|urgent)$")

class TaskResponse(BaseModel):
    task_id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task"
)
async def create_task(
    request: TaskCreateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """Create a new task for the authenticated user."""

    new_task = Task(
        user_id=user_id,
        title=request.title,
        description=request.description,
        due_date=request.due_date,
        priority=request.priority,
        status="pending"
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return TaskResponse.model_validate(new_task)
```

### Example 2: GET /api/{user_id}/tasks - List Tasks with Filters

**User Request:** "Create endpoint to list tasks with status filter"

**Generated Code:**
```python
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskResponse],
    summary="List user tasks"
)
async def list_tasks(
    user_id: int,
    status: Optional[str] = Query(None, pattern="^(pending|completed|all)$"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """
    List tasks for a user with optional filters.

    - **status**: Filter by pending/completed/all (default: all)
    - **limit**: Max results (1-500, default: 100)
    - **offset**: Pagination offset (default: 0)
    """

    # Authorization: users can only list their own tasks
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' tasks"
        )

    # Build query
    query = select(Task).where(Task.user_id == user_id)

    if status and status != "all":
        query = query.where(Task.status == status)

    query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())

    # Execute query
    tasks = session.exec(query).all()

    return [TaskResponse.model_validate(task) for task in tasks]
```

### Example 3: POST /api/{user_id}/chat - Stateless Chat with Agent

**User Request:** "Generate the Phase 3 chat endpoint with OpenAI Agent and MCP tools"

**Generated Code:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_session
from app.auth import get_current_user_id
from app.models import Conversation, Message
from app.agent import create_agent_with_mcp_tools, run_agent

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: int | None = None

class MessageResponse(BaseModel):
    message_id: int
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

class ChatResponse(BaseModel):
    conversation_id: int
    message: MessageResponse
    tool_calls: List[Dict[str, Any]] = []

@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with AI agent (stateless)"
)
async def chat_with_agent(
    user_id: int,
    request: ChatRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Send message to AI agent and get response.

    **STATELESS DESIGN:**
    1. Fetch conversation history from DB
    2. Instantiate fresh OpenAI Agent with MCP tools
    3. Execute agent with history + new user message
    4. Save messages (user + assistant) to DB
    5. Return assistant response with tool calls

    - **message**: User's message (1-2000 chars)
    - **conversation_id**: Optional, creates new conversation if null
    """

    # Authorization check
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' conversations"
        )

    # Step 1: Get or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        conversation = Conversation(user_id=user_id, title="New Chat")
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Step 2: Fetch conversation history from DB
    query = select(Message).where(
        Message.conversation_id == conversation.conversation_id
    ).order_by(Message.created_at.asc())
    history = session.exec(query).all()

    # Step 3: Save user message to DB
    user_message = Message(
        conversation_id=conversation.conversation_id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()
    session.refresh(user_message)

    # Step 4: Create fresh agent with MCP tools (stateless)
    agent = create_agent_with_mcp_tools(user_id=user_id)

    # Step 5: Run agent with full history + new message
    agent_response = await run_agent(
        agent=agent,
        history=[{"role": msg.role, "content": msg.content} for msg in history],
        new_message=request.message
    )

    # Step 6: Save assistant response to DB
    assistant_message = Message(
        conversation_id=conversation.conversation_id,
        role="assistant",
        content=agent_response["content"],
        tool_calls=agent_response.get("tool_calls", [])
    )
    session.add(assistant_message)
    session.commit()
    session.refresh(assistant_message)

    # Step 7: Return response
    return ChatResponse(
        conversation_id=conversation.conversation_id,
        message=MessageResponse.model_validate(assistant_message),
        tool_calls=agent_response.get("tool_calls", [])
    )
```

### Example 4: PUT /api/tasks/{task_id} - Update Task

**User Request:** "Generate endpoint to update a task"

**Generated Code:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api", tags=["tasks"])

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(pending|completed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    due_date: Optional[datetime] = None

@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update task"
)
async def update_task(
    task_id: int,
    request: TaskUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update task fields (partial update allowed).

    Only provided fields will be updated.
    """

    # Fetch task
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    # Authorization check
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update other users' tasks"
        )

    # Update fields (only if provided)
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.model_validate(task)
```

## Best Practices Checklist

When generating endpoints, ensure:

### Code Quality
- ✅ Use **Pydantic v2** syntax (`model_config`, `Field`, `model_validate`)
- ✅ Use **async def** for endpoints (even if not awaiting, for future-proofing)
- ✅ Proper **type hints** (use `int | None` not `Optional[int]` in Python 3.10+)
- ✅ **Field validation** (min_length, max_length, pattern, ge, le)
- ✅ **Dependency injection** (no global variables)

### API Design
- ✅ **Proper HTTP status codes** (201 for creation, 204 for deletion, etc.)
- ✅ **OpenAPI documentation** (summary, description, docstrings)
- ✅ **RESTful naming** (/tasks not /get_tasks)
- ✅ **Router tags** for grouping in docs
- ✅ **Consistent response models** across endpoints

### Security
- ✅ **Authentication required** (Depends(get_current_user_id))
- ✅ **Authorization checks** (user can only access own resources)
- ✅ **Input validation** (Pydantic models with constraints)
- ✅ **SQL injection prevention** (SQLModel ORM, no raw SQL)

### Database
- ✅ **Session management** (Depends(get_session), auto-cleanup)
- ✅ **Transactions** (commit on success, rollback on error)
- ✅ **Refresh after insert** (get updated fields like created_at)
- ✅ **Efficient queries** (select only needed fields, use indexes)

### Error Handling
- ✅ **HTTPException with detail** (clear error messages)
- ✅ **404 for not found** resources
- ✅ **403 for unauthorized** access
- ✅ **422 for validation** errors (automatic via Pydantic)

### Stateless Design (Phase 3)
- ✅ **No in-memory state** (fetch from DB on each request)
- ✅ **Fresh agent instantiation** (no global agent)
- ✅ **Full history retrieval** (for conversation context)
- ✅ **Persist all state to DB** (messages, tool calls, etc.)

## Integration with Other Skills

After generating an endpoint with this skill, suggest:

### 1. Database Operations
```
💡 Next: Use /sqlmodel-crud-helper to generate optimized database queries for this endpoint
```

### 2. MCP Tool Integration
```
💡 Next: Use /mcp-tool-crafter to create MCP tools called by this endpoint
```

### 3. Testing
```
💡 Next: Use /pytest-generator to create test cases for this endpoint
```

### 4. Documentation
```
💡 Next: Add this endpoint to specs/4-ai-agent-behavior/api.spec.md
```

### 5. Spec-Kit Plus Workflow
```
💡 Next: Run /sp.plan to update technical plan with this endpoint
```

## Troubleshooting

### Issue: Pydantic validation errors
**Solution:** Check model_config, use `from_attributes=True` for SQLModel models

### Issue: Session not closing
**Solution:** Use `Depends(get_session)` which handles cleanup automatically

### Issue: 422 Unprocessable Entity
**Solution:** Check request body matches Pydantic model, verify Field constraints

### Issue: Circular imports
**Solution:** Use `from __future__ import annotations` and string type hints

### Issue: Agent state lost between requests
**Solution:** Verify conversation history is fetched from DB, not cached

## Output Template

When this skill is invoked, provide:

1. **Import statements** (all required modules)
2. **Router setup** (with prefix and tags)
3. **Request/Response models** (Pydantic v2)
4. **Endpoint function** (fully implemented)
5. **Error handling** (HTTPException examples)
6. **Usage example** (cURL or Python requests)
7. **Next steps** (link to related skills/commands)

---

**Version:** 1.0
**Last Updated:** 2026-02-07
**Compatible With:** FastAPI 0.109+, Pydantic v2+, SQLModel 0.0.14+, Python 3.10+
