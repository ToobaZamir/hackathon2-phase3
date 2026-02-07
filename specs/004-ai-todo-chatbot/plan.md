# AI Todo Chatbot - Production-Ready Development Plan

## 1.0 Executive Summary

This plan details the complete technical architecture and implementation strategy for the AI-Powered Todo Chatbot (Hackathon II Phase 3). The system enables users to manage tasks through natural language conversations powered by Cohere's Command models, with all capabilities exposed via MCP (Model Context Protocol) tools.

**Key Architectural Decisions:**
- **Stateless Design**: No in-memory state; all conversations and tool calls persisted to PostgreSQL
- **Cohere API Integration**: Using OpenAI SDK compatibility layer for minimal code changes
- **MCP Tool Protocol**: Standardized interface between AI agent and database operations
- **Conversation-Driven**: Database-backed conversation history enables seamless resumption

**Timeline**: 1-2 focused days (12-16 hours) for MVP completion

**Critical Success Factors:**
1. Early validation of Cohere tool calling compatibility
2. Stateless architecture enforcement (no global state)
3. Robust conversation persistence and retrieval
4. Clear separation between agent logic and tool implementation

---

## 2.0 High-Level Architecture

### 2.1 System Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[OpenAI ChatKit UI]
    end
    
    subgraph "API Layer"
        API[FastAPI Backend<br/>Stateless]
        AUTH[JWT Auth Middleware]
    end
    
    subgraph "AI Agent Layer"
        AGENT[Cohere Agent<br/>command-a-03-2025]
        PROMPT[System Prompt<br/>Tool Descriptions]
    end
    
    subgraph "Tool Layer"
        MCP[MCP Server<br/>5 Tools]
        CREATE[create_task]
        LIST[list_tasks]
        UPDATE[update_task]
        DELETE[delete_task]
        COMPLETE[complete_task]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL<br/>Neon)]
        TASKS[Tasks Table]
        CONV[Conversations Table]
        MSG[Messages Table]
        USERS[Users Table]
    end
    
    UI -->|POST /api/{user_id}/chat<br/>+ JWT| API
    API -->|Validate JWT| AUTH
    AUTH -->|Extract user_id| API
    API -->|Fetch history| DB
    API -->|Instantiate fresh| AGENT
    AGENT -->|References| PROMPT
    AGENT -->|Calls tools| MCP
    MCP -->|CRUD ops| CREATE
    MCP -->|CRUD ops| LIST
    MCP -->|CRUD ops| UPDATE
    MCP -->|CRUD ops| DELETE
    MCP -->|CRUD ops| COMPLETE
    CREATE -->|Insert| TASKS
    LIST -->|Query| TASKS
    UPDATE -->|Update| TASKS
    DELETE -->|Delete| TASKS
    COMPLETE -->|Update status| TASKS
    API -->|Save messages| CONV
    API -->|Save messages| MSG
    AUTH -->|Validate user| USERS
```

### 2.2 Component Responsibilities

| Component | Responsibility | Stateful? | Dependencies |
|-----------|---------------|-----------|--------------|
| **Frontend (ChatKit)** | User interface, message rendering, JWT passing | No | None |
| **FastAPI Backend** | API endpoints, JWT validation, agent orchestration, DB operations | No | Neon DB, Cohere API |
| **Cohere Agent** | NLP understanding, intent detection, tool orchestration | No (fresh per request) | MCP Tools |
| **MCP Server** | Tool implementations (CRUD operations) | No | SQLModel, Neon DB |
| **PostgreSQL DB** | Persistent storage for tasks, conversations, messages, users | Yes (only component) | None |

### 2.3 Stateless Architecture Flow

```mermaid
sequenceDiagram
    participant User
    participant ChatKit
    participant FastAPI
    participant DB
    participant CohereAgent
    participant MCPTools
    
    User->>ChatKit: Type "Add buy groceries"
    ChatKit->>FastAPI: POST /api/123/chat<br/>{message, conversation_id, JWT}
    FastAPI->>FastAPI: Validate JWT → user_id=123
    FastAPI->>DB: Get/Create conversation(123)
    FastAPI->>DB: Fetch all messages for conversation
    Note over FastAPI: History: [{role: user, content: "..."}]
    FastAPI->>CohereAgent: NEW Client(COHERE_API_KEY)
    Note over CohereAgent: Fresh instance, no prior state
    FastAPI->>CohereAgent: chat.completions.create(<br/>messages=history+new,<br/>tools=mcp_tools)
    CohereAgent->>CohereAgent: Detect intent: CREATE_TASK
    CohereAgent->>MCPTools: create_task(user_id=123,<br/>title="buy groceries")
    MCPTools->>DB: INSERT INTO tasks
    DB-->>MCPTools: task_id=456
    MCPTools-->>CohereAgent: {success: true, task_id: 456}
    CohereAgent-->>FastAPI: "✓ Added task: Buy groceries"
    FastAPI->>DB: INSERT user message
    FastAPI->>DB: INSERT assistant message
    FastAPI->>DB: Log tool call
    FastAPI-->>ChatKit: {response, conversation_id, tool_calls}
    ChatKit-->>User: Display: "✓ Added task: Buy groceries"
    Note over FastAPI,CohereAgent: Agent instance destroyed
    
    Note over User,DB: SERVER RESTART (no state loss)
    
    User->>ChatKit: Type "Show my tasks"
    ChatKit->>FastAPI: POST /api/123/chat<br/>{message, same conversation_id, JWT}
    FastAPI->>DB: Fetch full history (2 prev messages)
    Note over FastAPI: Agent has context of previous task
    FastAPI->>CohereAgent: NEW Client (fresh instance)
    CohereAgent->>MCPTools: list_tasks(user_id=123, status="pending")
    MCPTools->>DB: SELECT * FROM tasks WHERE user_id=123
    DB-->>MCPTools: [task 456: "buy groceries"]
    MCPTools-->>CohereAgent: {tasks: [{id:456, title:"buy groceries"}]}
    CohereAgent-->>FastAPI: "You have 1 task: • Buy groceries"
    FastAPI->>DB: Save new messages
    FastAPI-->>ChatKit: Response
```

**Key Stateless Principles:**
1. **No In-Memory State**: Every request starts fresh
2. **Database as Source of Truth**: All state (conversations, messages, tool calls) persisted
3. **Fresh Agent Instantiation**: New Cohere client on every request
4. **History Fetching**: Full conversation loaded from DB before agent execution
5. **Survives Restarts**: Server can restart anytime without data loss

---

## 3.0 Technology Stack Details

### 3.1 Cohere API Integration

**Primary Model**: `command-a-03-2025`
- Optimized for agentic workflows and tool use
- Strong multi-step reasoning capabilities
- Cost-effective for tool-heavy interactions
- Native tool calling support (JSON schema format)

**Alternative Model**: `command-r-plus-08-2024`
- For complex multi-step reasoning tasks
- Long context window (128k tokens)
- Fallback if primary model unavailable

**Integration Method**: OpenAI SDK with Cohere compatibility endpoint

```python
# Cohere client initialization (OpenAI SDK compatibility)
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("COHERE_API_KEY"),  # Never hardcoded
    base_url="https://api.cohere.ai/compatibility/v1"
)

# Tool calling pattern
response = client.chat.completions.create(
    model="command-a-03-2025",  # Cohere model
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Add buy groceries"}
    ],
    tools=mcp_tools_schema,  # Cohere-compatible JSON schema
    tool_choice="auto"  # Let agent decide when to call tools
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        # Call MCP tool and return result
        result = mcp_server.call_tool(tool_name, tool_args)
```

**Native Cohere SDK Fallback** (if OpenAI compatibility has issues):

```python
import cohere

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

# Native Cohere tool calling
response = co.chat(
    model="command-a-03-2025",
    message="Add buy groceries",
    chat_history=conversation_history,
    tools=mcp_tools_schema,  # Cohere's native tool format
    force_single_step=False  # Allow multi-step reasoning
)
```

### 3.2 Backend Stack

**FastAPI Configuration**:
- Framework: FastAPI 0.104.1+ (async support)
- ASGI Server: Uvicorn 0.24.0+
- ORM: SQLModel 0.0.16+ (Pydantic v2 compatible)
- Database Driver: asyncpg 0.29.0+ for async PostgreSQL
- Migrations: Alembic 1.13.1+

**Authentication**:
- Better Auth integration (JWT-based)
- JWT library: python-jose[cryptography] 3.3.0+
- Password hashing: passlib[bcrypt] 1.7.4+

**Additional Dependencies**:
- `cohere` SDK: 5.0.0+ (fallback for native tool calling)
- `openai` SDK: 1.0.0+ (for Cohere compatibility layer)
- `mcp` package: Official MCP Python SDK for tool server
- `python-dotenv`: 1.0.0+ for environment variable management
- `httpx`: 0.25.2+ for async HTTP requests (if needed)

### 3.3 Frontend Stack

**OpenAI ChatKit** (React-based):
- Framework: Next.js 14.2.5+ (App Router)
- React: 18.2.0+
- UI Components: ChatKit official components
- State Management: React hooks (useState, useEffect)
- HTTP Client: Fetch API or axios

**Note**: Original spec mentioned OpenAI ChatKit, but current frontend uses custom Next.js app. Plan accommodates either:
- **Option A**: Integrate official OpenAI ChatKit library
- **Option B**: Build custom chat UI mimicking ChatKit patterns

### 3.4 Database Stack

**Neon Serverless PostgreSQL**:
- Version: PostgreSQL 15+
- Connection: Connection pooling via SQLModel/SQLAlchemy
- Environment Variable: `DATABASE_URL` (format: `postgresql://user:pass@host/dbname`)

**Schema Management**:
- Alembic for migrations
- SQLModel for ORM models
- Automatic schema creation in development
- Versioned migrations for production

---

## 4.0 Complete Project Structure

```
phase-3/
├── backend/
│   ├── alembic/                          # Database migrations
│   │   ├── versions/
│   │   │   ├── 001_initial_task_table.py         [EXISTS]
│   │   │   ├── 002_add_conversations_table.py    [NEW]
│   │   │   ├── 003_add_messages_table.py         [NEW]
│   │   │   └── 004_add_tool_calls_to_messages.py [NEW]
│   │   ├── env.py                                [EXISTS]
│   │   └── alembic.ini                           [EXISTS]
│   │
│   ├── src/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py                   [EXISTS]
│   │   │   │   ├── auth.py                       [EXISTS - JWT endpoints]
│   │   │   │   ├── tasks.py                      [EXISTS - CRUD endpoints]
│   │   │   │   └── chat.py                       [NEW - Stateless chat endpoint]
│   │   │   └── __init__.py                       [EXISTS]
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py                         [EXISTS - Add COHERE_API_KEY]
│   │   │   ├── auth.py                           [EXISTS - JWT validation]
│   │   │   ├── security.py                       [EXISTS]
│   │   │   └── error_handlers.py                 [EXISTS]
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   └── connection.py                     [EXISTS]
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── task.py                           [EXISTS]
│   │   │   ├── user.py                           [EXISTS]
│   │   │   ├── conversation.py                   [NEW]
│   │   │   └── message.py                        [NEW]
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── task.py                           [EXISTS]
│   │   │   ├── chat.py                           [NEW - ChatRequest/Response]
│   │   │   └── message.py                        [NEW]
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── task_service.py                   [EXISTS]
│   │   │   ├── user_service.py                   [EXISTS]
│   │   │   ├── conversation_service.py           [NEW]
│   │   │   ├── agent_service.py                  [NEW - Cohere client wrapper]
│   │   │   └── mcp_client.py                     [NEW - Tool calling logic]
│   │   │
│   │   ├── agent/                                [NEW DIRECTORY]
│   │   │   ├── __init__.py
│   │   │   ├── system_prompt.py                  [NEW - Agent instructions]
│   │   │   ├── cohere_client.py                  [NEW - Cohere SDK wrapper]
│   │   │   └── tool_executor.py                  [NEW - Execute MCP tools]
│   │   │
│   │   └── main.py                               [EXISTS - Add chat route]
│   │
│   ├── mcp_server/                               [NEW DIRECTORY]
│   │   ├── __init__.py
│   │   ├── server.py                             [NEW - MCP server setup]
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── create_task.py                    [NEW]
│   │   │   ├── list_tasks.py                     [NEW]
│   │   │   ├── update_task.py                    [NEW]
│   │   │   ├── delete_task.py                    [NEW]
│   │   │   └── complete_task.py                  [NEW]
│   │   └── schemas/                              [NEW - Cohere tool schemas]
│   │       └── tool_definitions.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_task_service.py              [EXISTS]
│   │   │   ├── test_mcp_tools.py                 [NEW]
│   │   │   ├── test_agent_service.py             [NEW]
│   │   │   └── test_chat_endpoint.py             [NEW]
│   │   └── integration/
│   │       ├── test_chat_flow.py                 [NEW]
│   │       └── test_stateless_architecture.py    [NEW]
│   │
│   ├── requirements.txt                          [EXISTS - Update with AI deps]
│   ├── .env.example                              [NEW]
│   └── README.md                                 [Update with Phase 3 setup]
│
├── frontend-todo-app/                            [EXISTS]
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/                             [NEW - Chat UI page]
│   │   │   │   └── page.tsx
│   │   │   └── ...                               [Existing pages]
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx                 [NEW]
│   │   │   ├── MessageList.tsx                   [NEW]
│   │   │   ├── MessageInput.tsx                  [NEW]
│   │   │   └── ...                               [Existing components]
│   │   ├── lib/
│   │   │   ├── api.ts                            [Update - Add chat endpoint]
│   │   │   └── auth.ts                           [EXISTS]
│   │   └── types/
│   │       └── chat.ts                           [NEW]
│   ├── package.json                              [EXISTS - Add ChatKit if using]
│   └── README.md                                 [Update]
│
├── specs/
│   └── 004-ai-todo-chatbot/
│       ├── spec.md                               [EXISTS]
│       ├── plan.md                               [THIS FILE]
│       ├── tasks.md                              [TO BE GENERATED]
│       ├── checklists/
│       │   └── requirements.md                   [EXISTS]
│       ├── contracts/                            [NEW]
│       │   ├── api-endpoints.md
│       │   ├── mcp-tool-contracts.md
│       │   └── database-schema.md
│       └── research/                             [NEW]
│           ├── cohere-tool-calling.md
│           └── stateless-agent-patterns.md
│
├── history/
│   └── prompts/
│       └── 4-ai-todo-chatbot/                    [NEW PHRs]
│
├── .specify/
│   └── memory/
│       └── constitution.md                       [v2.0.1]
│
├── .env.example                                  [UPDATE]
├── README.md                                     [UPDATE]
└── CLAUDE.md                                     [EXISTS]
```

**File Count Summary**:
- **Existing Files**: ~25 (backend foundation, frontend, specs)
- **New Files to Create**: ~35 (agent layer, MCP tools, chat endpoint, migrations, tests)
- **Files to Update**: ~8 (requirements.txt, config.py, main.py, package.json, README.md, etc.)

**Total Implementation Effort**: ~43 files to touch

---

## 5.0 Database Schema Design

### 5.1 Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Task : owns
    User ||--o{ Conversation : has
    Conversation ||--o{ Message : contains
    Message ||--o{ ToolCall : includes
    
    User {
        int id PK
        string email UK
        string hashed_password
        datetime created_at
        datetime updated_at
    }
    
    Task {
        int id PK
        int user_id FK
        string title
        text description
        bool completed
        datetime created_at
        datetime updated_at
    }
    
    Conversation {
        int id PK
        int user_id FK
        datetime created_at
        datetime updated_at
    }
    
    Message {
        int id PK
        int conversation_id FK
        string role
        text content
        json tool_calls
        datetime timestamp
    }
    
    ToolCall {
        int id PK
        int message_id FK
        string tool_name
        json arguments
        json result
        datetime executed_at
    }
```

### 5.2 SQLModel Definitions

**New Models to Create**:

```python
# backend/src/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, DateTime, func

class Conversation(SQLModel, table=True):
    """Conversation model - represents a chat session"""
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    )
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationCreate(SQLModel):
    """Schema for creating a new conversation"""
    user_id: int

class ConversationPublic(SQLModel):
    """Public schema for returning conversation data"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    message_count: int = 0  # Computed field
    
    class Config:
        from_attributes = True
```

```python
# backend/src/models/message.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, DateTime, JSON, func
from enum import Enum

class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(SQLModel, table=True):
    """Message model - represents a single chat message"""
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(String(20), nullable=False))
    content: str = Field(max_length=10000)
    
    # Optional: Store tool calls for debugging
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    
    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class MessageCreate(SQLModel):
    """Schema for creating a new message"""
    conversation_id: int
    role: MessageRole
    content: str
    tool_calls: Optional[Dict[str, Any]] = None

class MessagePublic(SQLModel):
    """Public schema for returning message data"""
    id: int
    conversation_id: int
    role: MessageRole
    content: str
    tool_calls: Optional[Dict[str, Any]]
    timestamp: datetime
    
    class Config:
        from_attributes = True
```

**Existing Model Updates**:

```python
# backend/src/models/task.py - Already exists, no changes needed
# Verify fields match spec:
# - id (primary key)
# - user_id (indexed, foreign key)
# - title (1-255 chars)
# - description (optional, max 1000 chars)
# - completed (boolean, default False)
# - created_at (datetime)
# - updated_at (datetime)
```

### 5.3 Database Indexes

**Critical Indexes for Performance**:

```sql
-- Already exists (from Phase 1)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- New indexes for Phase 3
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);  -- For pagination

-- Composite index for common query pattern
CREATE INDEX idx_tasks_user_status ON tasks(user_id, completed);
```

**Rationale**:
- `user_id` indexes: Enable fast filtering by user (critical for multi-tenancy)
- `conversation_id` index: Fast message retrieval for conversation history
- `timestamp` index: Efficient pagination and chronological ordering
- Composite index: Optimizes filtered task lists (e.g., "show pending tasks")

### 5.4 Migration Strategy

**Alembic Migration Sequence**:

1. **002_add_conversations_table.py** - Create conversations table
2. **003_add_messages_table.py** - Create messages table with foreign keys
3. **004_add_tool_calls_to_messages.py** - Add tool_calls JSON column (optional)

**Migration Template**:

```python
# alembic/versions/002_add_conversations_table.py
"""Add conversations table

Revision ID: 002
Revises: 001
Create Date: 2026-02-07

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('created_at', TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('conversations')
```

---

## 6.0 MCP Tools Specification

### 6.1 Tool Architecture

**Design Principles**:
1. **Stateless Execution**: Each tool call is independent
2. **Cohere-Compatible Schemas**: JSON format matching OpenAI function calling
3. **Consistent Error Handling**: Structured error responses
4. **Parameter Validation**: Strict input validation before DB operations
5. **User Isolation**: All tools enforce user_id filtering

### 6.2 Tool Definitions (Cohere-Compatible JSON Schema)

```python
# backend/mcp_server/schemas/tool_definitions.py

MCP_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Creates a new task for the user. Use this when the user wants to add, create, or be reminded of something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user creating the task (from JWT token)"
                    },
                    "title": {
                        "type": "string",
                        "description": "The task title (1-255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional detailed description of the task",
                        "maxLength": 1000
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority level (default: medium)"
                    }
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieves tasks for the user. Supports filtering by completion status. Use this when the user wants to see, show, or list their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status (default: all)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return (default: 50)",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of tasks to skip for pagination (default: 0)",
                        "minimum": 0
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Updates an existing task's title, description, or status. Use this when the user wants to change, update, modify, or edit a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (1-255 characters)",
                        "minLength": 1,
                        "maxLength": 255
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description",
                        "maxLength": 1000
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "New completion status (true = completed, false = pending)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Permanently deletes a task. Use this when the user wants to delete or remove a task. Always confirm before calling this tool.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Marks a task as completed. This is a shortcut for update_task with completed=true. Use when the user says they finished, completed, or are done with a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user (from JWT token)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]
```

### 6.3 Tool Implementation Patterns

**Example: create_task Tool**

```python
# backend/mcp_server/tools/create_task.py
from sqlmodel import Session, select
from typing import Optional, Dict, Any
from backend.src.models.task import Task, TaskCreate
from backend.src.database.connection import engine

async def create_task(
    user_id: int,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = "medium"
) -> Dict[str, Any]:
    """
    Creates a new task for the user.
    
    Args:
        user_id: ID of the user creating the task
        title: Task title (1-255 chars)
        description: Optional task description
        priority: Task priority (low/medium/high)
    
    Returns:
        Success: {"success": True, "task_id": int, "title": str}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        # Validate inputs
        if not title or len(title.strip()) == 0:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task title cannot be empty"
            }
        
        if len(title) > 255:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Task title must be 255 characters or less"
            }
        
        # Create task
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "created_at": task.created_at.isoformat()
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not create task: {str(e)}"
        }
```

**Example: list_tasks Tool**

```python
# backend/mcp_server/tools/list_tasks.py
from sqlmodel import Session, select
from typing import Optional, Dict, Any, List
from backend.src.models.task import Task
from backend.src.database.connection import engine

async def list_tasks(
    user_id: int,
    status: Optional[str] = "all",
    limit: Optional[int] = 50,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Retrieves tasks for the user with optional filtering.
    
    Args:
        user_id: ID of the user
        status: Filter by status (all/pending/completed)
        limit: Max tasks to return
        offset: Number of tasks to skip
    
    Returns:
        Success: {"success": True, "tasks": [...], "count": int}
        Error: {"success": False, "error": str, "message": str}
    """
    try:
        with Session(engine) as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)
            
            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            # "all" = no filter
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            # Execute query
            results = session.exec(query).all()
            
            # Format results
            tasks = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in results
            ]
            
            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": "internal_error",
            "message": f"Could not retrieve tasks: {str(e)}"
        }
```

### 6.4 Tool Error Taxonomy

| Error Code | HTTP Status | When to Use | Example Message |
|------------|-------------|-------------|-----------------|
| `validation_error` | 400 | Invalid input parameters | "Task title must be 1-255 characters" |
| `not_found` | 404 | Resource doesn't exist | "Task with ID 123 not found" |
| `unauthorized` | 401 | Missing/invalid JWT | "Authentication required" |
| `forbidden` | 403 | User can't access resource | "You don't have permission to access this task" |
| `internal_error` | 500 | Unexpected server error | "Could not complete operation. Please try again." |

**Tool Response Format**:

```python
# Success response
{
    "success": True,
    "task_id": 123,
    "title": "Buy groceries",
    # ... other relevant data
}

# Error response
{
    "success": False,
    "error": "not_found",  # Error code
    "message": "Task with ID 123 not found"  # User-friendly message
}
```

---

## 7.0 API Endpoint Design

### 7.1 Chat Endpoint Specification

**Endpoint**: `POST /api/{user_id}/chat`

**Purpose**: Stateless conversational interface for task management

**Authentication**: JWT required (user_id validated against token)

**Request Schema**:

```python
# backend/src/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message to the agent"
    )
    conversation_id: Optional[int] = Field(
        None,
        description="Existing conversation ID (if resuming). If null, creates new conversation."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add buy groceries",
                "conversation_id": 123
            }
        }

class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    message: str = Field(
        ...,
        description="Agent's response message"
    )
    conversation_id: int = Field(
        ...,
        description="Conversation ID (for subsequent requests)"
    )
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of tools called by the agent (for debugging)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "✓ Added task: Buy groceries",
                "conversation_id": 123,
                "tool_calls": [
                    {
                        "tool": "create_task",
                        "arguments": {"user_id": 1, "title": "Buy groceries"},
                        "result": {"success": True, "task_id": 456}
                    }
                ]
            }
        }
```

**Endpoint Implementation**:

```python
# backend/src/api/v1/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any

from backend.src.schemas.chat import ChatRequest, ChatResponse
from backend.src.core.auth import get_current_user
from backend.src.database.connection import get_session
from backend.src.services.conversation_service import ConversationService
from backend.src.services.agent_service import AgentService
from backend.src.models.user import User

router = APIRouter()

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Stateless chat endpoint for conversational task management.
    
    Flow:
    1. Validate JWT and user_id match
    2. Get/create conversation from DB
    3. Fetch full conversation history from DB
    4. Instantiate fresh Cohere agent with MCP tools
    5. Execute agent with history + new message
    6. Save user message and agent response to DB
    7. Return response with conversation_id
    
    Args:
        user_id: User ID from URL path
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user (from JWT)
        session: Database session
    
    Returns:
        ChatResponse with agent's message and conversation_id
    
    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation_id not found
        HTTPException 500: If agent execution fails
    """
    # 1. Validate authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )
    
    # 2. Get or create conversation
    conversation_service = ConversationService(session)
    
    if request.conversation_id:
        conversation = conversation_service.get_conversation(
            conversation_id=request.conversation_id,
            user_id=user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found"
            )
    else:
        conversation = conversation_service.create_conversation(user_id=user_id)
    
    # 3. Fetch conversation history from DB
    history = conversation_service.get_conversation_history(conversation.id)
    
    # 4. Save user message to DB
    user_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    
    # 5. Instantiate fresh agent and execute
    agent_service = AgentService()
    
    try:
        agent_response = await agent_service.execute(
            user_id=user_id,
            message=request.message,
            history=history
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )
    
    # 6. Save agent response to DB
    assistant_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content=agent_response["message"],
        tool_calls=agent_response.get("tool_calls")
    )
    
    # 7. Return response
    return ChatResponse(
        message=agent_response["message"],
        conversation_id=conversation.id,
        tool_calls=agent_response.get("tool_calls")
    )
```

### 7.2 Existing Endpoints (No Changes Required)

**Task CRUD Endpoints** (already implemented in Phase 1):
- `POST /api/todos` - Create task
- `GET /api/todos` - List tasks
- `PUT /api/todos/{task_id}` - Update task
- `DELETE /api/todos/{task_id}` - Delete task
- `PATCH /api/todos/{task_id}` - Partial update (e.g., toggle completed)

**Authentication Endpoints** (already implemented in Phase 2):
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

**Note**: These endpoints remain available for direct API access but are NOT used by the chat agent. The agent uses MCP tools exclusively.

### 7.3 Error Response Format

**Consistent Error Structure**:

```python
# backend/src/core/error_handlers.py (add to existing)
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def chat_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle errors from chat endpoint"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "chat_error",
            "message": "Unable to process your message. Please try again.",
            "details": str(exc) if settings.debug else None
        }
    )

# Register in main.py
app.add_exception_handler(ChatError, chat_error_handler)
```

---

## 8.0 Agent Architecture

### 8.1 Cohere Client Initialization

```python
# backend/src/services/agent_service.py
from openai import OpenAI
import os
from typing import List, Dict, Any, Optional
import json

from backend.src.agent.system_prompt import SYSTEM_PROMPT
from backend.mcp_server.schemas.tool_definitions import MCP_TOOLS
from backend.mcp_server.tools import (
    create_task, list_tasks, update_task, delete_task, complete_task
)

class AgentService:
    """
    Service for executing Cohere-powered AI agent with MCP tools.
    
    Stateless design:
    - Fresh client instantiated on each execute() call
    - No instance variables storing conversation state
    - All state passed as parameters or retrieved from DB
    """
    
    def __init__(self):
        """Initialize agent service (no state stored)"""
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        
        self.model = os.getenv("COHERE_MODEL", "command-a-03-2025")
    
    async def execute(
        self,
        user_id: int,
        message: str,
        history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Execute agent with user message and conversation history.
        
        Args:
            user_id: ID of the user (for MCP tool calls)
            message: User's new message
            history: Previous conversation messages [{role: str, content: str}]
        
        Returns:
            {
                "message": str,  # Agent's response
                "tool_calls": List[Dict]  # Tools called during execution
            }
        """
        # 1. Create fresh Cohere client (stateless)
        client = OpenAI(
            api_key=self.cohere_api_key,
            base_url="https://api.cohere.ai/compatibility/v1"
        )
        
        # 2. Build message list
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + history + [
            {"role": "user", "content": message}
        ]
        
        # 3. Call Cohere API
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=MCP_TOOLS,
            tool_choice="auto",  # Let agent decide when to use tools
            temperature=0.7,
            max_tokens=1000
        )
        
        # 4. Handle tool calls (if any)
        tool_calls_log = []
        assistant_message = response.choices[0].message
        
        if assistant_message.tool_calls:
            # Agent wants to call tools
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # Inject user_id into tool args
                tool_args["user_id"] = user_id
                
                # Execute tool
                tool_result = await self._execute_tool(tool_name, tool_args)
                
                # Log tool call
                tool_calls_log.append({
                    "tool": tool_name,
                    "arguments": tool_args,
                    "result": tool_result
                })
            
            # Send tool results back to agent for final response
            messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # Add tool results
            for i, tool_call in enumerate(assistant_message.tool_calls):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_calls_log[i]["result"])
                })
            
            # Get final response from agent
            final_response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            final_message = final_response.choices[0].message.content
        else:
            # No tool calls, use direct response
            final_message = assistant_message.content
        
        # 5. Return response
        return {
            "message": final_message,
            "tool_calls": tool_calls_log if tool_calls_log else None
        }
    
    async def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute MCP tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            args: Tool arguments (including user_id)
        
        Returns:
            Tool execution result
        """
        tool_map = {
            "create_task": create_task,
            "list_tasks": list_tasks,
            "update_task": update_task,
            "delete_task": delete_task,
            "complete_task": complete_task
        }
        
        tool_func = tool_map.get(tool_name)
        if not tool_func:
            return {
                "success": False,
                "error": "invalid_tool",
                "message": f"Tool '{tool_name}' not found"
            }
        
        try:
            result = await tool_func(**args)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": "tool_execution_error",
                "message": f"Tool execution failed: {str(e)}"
            }
```

### 8.2 System Prompt Design

```python
# backend/src/agent/system_prompt.py

SYSTEM_PROMPT = """You are a helpful todo assistant. Your role is to help users manage their tasks through natural conversation.

# Your Capabilities

You can help users:
- **Add tasks**: "add [task]", "remind me to [task]", "create task [task]"
- **List tasks**: "show my tasks", "what do I need to do?", "list pending tasks"
- **Complete tasks**: "mark task [id] as done", "complete [task name]", "I finished [task]"
- **Update tasks**: "change task [id] to [new title]", "update [task name]"
- **Delete tasks**: "delete task [id]", "remove [task name]"

# Available Tools

You have access to these MCP tools to interact with the user's task database:

1. **create_task(user_id, title, description?, priority?)** - Add a new task
2. **list_tasks(user_id, status?, limit?, offset?)** - Retrieve tasks (filter by pending/completed/all)
3. **update_task(user_id, task_id, title?, description?, completed?)** - Modify an existing task
4. **delete_task(user_id, task_id)** - Permanently remove a task
5. **complete_task(user_id, task_id)** - Mark a task as completed (shortcut for update_task)

# Important Guidelines

1. **Task References by Name**: If a user references a task by name (e.g., "complete buy groceries"), first call `list_tasks()` to find the task_id, then call the appropriate tool with that ID.

2. **Confirm Destructive Actions**: Always ask for confirmation before calling `delete_task()`. Example: "Are you sure you want to delete task #5 'Buy milk'? Type 'yes' to confirm."

3. **Provide Context**: Always mention the task title and ID in your responses. Examples:
   - "✓ Added task #7: Buy groceries"
   - "Marked task #3 'Call mom' as complete!"
   - "Updated task #2 to 'Buy organic milk'"

4. **Handle Ambiguity**: If multiple tasks match a name, list them and ask which one. Example:
   "I found 2 tasks with 'meeting':
   1. Task #5: Team meeting
   2. Task #8: Client meeting
   Which one would you like to complete?"

5. **Error Handling**: If a tool returns an error, explain it in user-friendly language:
   - not_found: "I couldn't find task #5. Try saying 'show my tasks' to see your list."
   - validation_error: "Task titles must be between 1-255 characters. Can you shorten that?"
   - internal_error: "I'm having trouble with that operation. Please try again in a moment."

6. **Friendly Tone**: Use encouraging, conversational language. Celebrate completions!

7. **Status Filters**: When listing tasks, respect user intent:
   - "show my tasks" → status="all"
   - "what do I need to do?" → status="pending"
   - "what have I finished?" → status="completed"

# Example Interactions

**User**: "Add buy groceries"
**You**: [Call create_task(user_id, title="buy groceries")]
**Response**: "✓ Added task #7: Buy groceries"

**User**: "Show my pending tasks"
**You**: [Call list_tasks(user_id, status="pending")]
**Response**: "You have 2 pending tasks:
• Task #7: Buy groceries
• Task #9: Call mom"

**User**: "Complete buy groceries"
**You**: [Call list_tasks(user_id) to find task, then complete_task(user_id, task_id=7)]
**Response**: "✓ Marked task #7 'Buy groceries' as complete! Great job!"

**User**: "Delete task 7"
**You**: [Call list_tasks to get task details]
**Response**: "Are you sure you want to delete task #7 'Buy groceries'? Type 'yes' to confirm."
**User**: "yes"
**You**: [Call delete_task(user_id, task_id=7)]
**Response**: "✓ Deleted task #7 'Buy groceries'"

# Remember

- You are stateless: Each conversation starts fresh, but you have access to full conversation history
- Always use the provided tools to interact with tasks (don't make up data)
- Be helpful, friendly, and concise
- Prioritize user experience over technical details
"""
```

### 8.3 Conversation History Management

```python
# backend/src/services/conversation_service.py
from sqlmodel import Session, select
from typing import List, Dict, Optional
from datetime import datetime

from backend.src.models.conversation import Conversation, ConversationCreate
from backend.src.models.message import Message, MessageCreate, MessageRole

class ConversationService:
    """Service for managing conversations and messages"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_conversation(self, user_id: int) -> Conversation:
        """Create a new conversation for a user"""
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation
    
    def get_conversation(
        self,
        conversation_id: int,
        user_id: int
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID (with user authorization check)
        
        Returns None if not found or user doesn't own it
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return self.session.exec(statement).first()
    
    def get_conversation_history(
        self,
        conversation_id: int,
        limit: Optional[int] = 50
    ) -> List[Dict[str, str]]:
        """
        Fetch all messages for a conversation in chronological order.
        
        Returns list of message dicts formatted for Cohere API:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        """
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
        )
        messages = self.session.exec(statement).all()
        
        return [
            {
                "role": message.role.value,
                "content": message.content
            }
            for message in messages
        ]
    
    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        tool_calls: Optional[Dict] = None
    ) -> Message:
        """Add a new message to a conversation"""
        message = Message(
            conversation_id=conversation_id,
            role=MessageRole(role),
            content=content,
            tool_calls=tool_calls
        )
        self.session.add(message)
        
        # Update conversation's updated_at timestamp
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(message)
        return message
```

### 8.4 Multi-Step Reasoning with Tool Chaining

**Example**: User says "Delete buy groceries"

1. **Agent receives**: "Delete buy groceries"
2. **Agent thinks**: "I need task_id to delete, but only have name"
3. **Tool Call 1**: `list_tasks(user_id, status="all")`
   - Result: `[{id: 7, title: "buy groceries", ...}, {id: 9, title: "call mom", ...}]`
4. **Agent analyzes**: Found task #7 matches "buy groceries"
5. **Agent confirms**: "Are you sure you want to delete task #7 'Buy groceries'? Type 'yes' to confirm."
6. **User responds**: "yes"
7. **Tool Call 2**: `delete_task(user_id, task_id=7)`
   - Result: `{success: True}`
8. **Agent responds**: "✓ Deleted task #7 'Buy groceries'"

**Cohere's Multi-Step Support**: Command models handle this naturally through multiple tool call rounds within a single API request or across requests with conversation history.

---

## 9.0 Implementation Sequence (8 Phases)

### Phase 1: Database Setup (2-3 hours)

**Goal**: Extend database schema to support conversations and messages

**Tasks**:
1. **Create Conversation Model** (`backend/src/models/conversation.py`)
   - SQLModel class with id, user_id, created_at, updated_at
   - Relationship to User and Message
2. **Create Message Model** (`backend/src/models/message.py`)
   - SQLModel class with id, conversation_id, role, content, tool_calls, timestamp
   - Enum for MessageRole (user/assistant/system)
3. **Generate Alembic Migrations**
   - `002_add_conversations_table.py`
   - `003_add_messages_table.py`
4. **Run Migrations**
   - Test locally: `alembic upgrade head`
   - Verify tables created in Neon DB
5. **Create ConversationService** (`backend/src/services/conversation_service.py`)
   - CRUD operations: create_conversation, get_conversation, get_conversation_history, add_message

**Acceptance Criteria**:
- [ ] Tables exist in database (verify with `\dt` in psql)
- [ ] Can create conversation via service
- [ ] Can add messages to conversation
- [ ] Can retrieve full conversation history

**Dependencies**: None (extends existing Phase 1 database)

**Files Created**: 5 (2 models, 2 migrations, 1 service)

---

### Phase 2: MCP Server Implementation (4-5 hours)

**Goal**: Implement 5 MCP tools with Cohere-compatible schemas

**Tasks**:
1. **Create MCP Server Directory** (`backend/mcp_server/`)
2. **Define Tool Schemas** (`backend/mcp_server/schemas/tool_definitions.py`)
   - 5 tools in OpenAI function calling format (Cohere-compatible)
   - JSON schema with descriptions, parameter types, required fields
3. **Implement Tools** (one file per tool):
   - `create_task.py`: Add new task to DB
   - `list_tasks.py`: Query tasks with filters
   - `update_task.py`: Update task fields
   - `delete_task.py`: Delete task by ID
   - `complete_task.py`: Mark task as completed (wrapper for update_task)
4. **Tool Testing**
   - Unit tests for each tool (`backend/tests/unit/test_mcp_tools.py`)
   - Test success cases and error handling
   - Verify user isolation (can't access other users' tasks)

**Acceptance Criteria**:
- [ ] All 5 tools implemented and importable
- [ ] Tool schemas match Cohere format
- [ ] Tools correctly interact with database via SQLModel
- [ ] Error responses follow taxonomy (validation_error, not_found, internal_error)
- [ ] User isolation enforced (user_id filtering)

**Dependencies**: Phase 1 (database models)

**Files Created**: 8 (1 schema, 5 tools, 1 init, 1 test)

---

### Phase 3: Authentication Middleware (1 hour)

**Goal**: Ensure JWT validation works for chat endpoint

**Tasks**:
1. **Update Config** (`backend/src/core/config.py`)
   - Add `COHERE_API_KEY` environment variable
   - Add `COHERE_MODEL` (default: "command-a-03-2025")
2. **Verify JWT Middleware** (`backend/src/core/auth.py`)
   - Ensure `get_current_user()` dependency works
   - Test JWT extraction and validation
3. **Create .env.example**
   - Document all required environment variables

**Acceptance Criteria**:
- [ ] `COHERE_API_KEY` configurable via environment
- [ ] JWT middleware validates tokens correctly
- [ ] `.env.example` includes all Phase 3 variables

**Dependencies**: Phase 2 existing auth system

**Files Updated**: 2 (config.py, .env.example)

---

### Phase 4: Chat Endpoint (3-4 hours)

**Goal**: Implement stateless FastAPI chat endpoint

**Tasks**:
1. **Create Chat Schemas** (`backend/src/schemas/chat.py`)
   - ChatRequest (message, conversation_id)
   - ChatResponse (message, conversation_id, tool_calls)
2. **Implement Chat Endpoint** (`backend/src/api/v1/chat.py`)
   - Route: `POST /api/{user_id}/chat`
   - JWT validation
   - Conversation get/create logic
   - History fetching
   - Agent execution (placeholder)
   - Message persistence
3. **Register Route** (`backend/src/main.py`)
   - Add chat router to FastAPI app
4. **Manual Testing**
   - Test with curl/Postman
   - Verify stateless behavior (restart server, resume conversation)

**Acceptance Criteria**:
- [ ] Endpoint accepts ChatRequest
- [ ] Returns ChatResponse with conversation_id
- [ ] Validates JWT and user_id
- [ ] Persists user messages to database
- [ ] Fetches full conversation history
- [ ] Returns 403 for unauthorized access

**Dependencies**: Phase 1 (conversation models), Phase 3 (auth)

**Files Created**: 3 (1 schema, 1 endpoint, update main.py)

---

### Phase 5: Agent Logic (Cohere Integration) (4-5 hours)

**Goal**: Integrate Cohere API with tool calling

**Tasks**:
1. **Create System Prompt** (`backend/src/agent/system_prompt.py`)
   - Define agent personality and capabilities
   - Tool usage guidelines
   - Example interactions
2. **Implement Cohere Client** (`backend/src/agent/cohere_client.py`)
   - Wrapper around OpenAI SDK with Cohere compatibility
   - Fallback to native Cohere SDK if needed
3. **Create AgentService** (`backend/src/services/agent_service.py`)
   - Fresh client instantiation per request
   - Tool calling orchestration
   - Multi-step reasoning support
   - Tool result handling
4. **Integrate into Chat Endpoint**
   - Replace placeholder in chat.py with agent execution
5. **Early Testing**
   - Test simple tool call: "Add buy groceries"
   - Test tool chaining: "Complete buy groceries" (list → complete)
   - Test no-tool response: "Hello"

**Acceptance Criteria**:
- [ ] Cohere client initializes with API key
- [ ] Agent receives conversation history
- [ ] Agent calls MCP tools correctly
- [ ] Tool results incorporated into response
- [ ] Agent provides natural language responses
- [ ] Multi-step reasoning works (tool chaining)

**Dependencies**: Phase 2 (MCP tools), Phase 4 (chat endpoint)

**Files Created**: 4 (system_prompt, cohere_client, agent_service, update chat.py)

---

### Phase 6: Frontend Integration (3-4 hours)

**Goal**: Build chat UI that proxies to backend

**Tasks**:
1. **Create Chat Page** (`frontend-todo-app/src/app/chat/page.tsx`)
   - Next.js page component
   - Route: `/chat`
2. **Build Chat Components**
   - `ChatInterface.tsx`: Main container
   - `MessageList.tsx`: Display conversation history
   - `MessageInput.tsx`: Text input with send button
3. **Add API Client** (`frontend-todo-app/src/lib/api.ts`)
   - Function: `sendChatMessage(userId, message, conversationId, jwt)`
   - Fetch POST to `/api/{userId}/chat`
4. **State Management**
   - useState for messages, conversationId, loading
   - useEffect to load conversation on mount (if resuming)
5. **JWT Integration**
   - Pass JWT in Authorization header
   - Handle 401/403 errors (redirect to login)

**Acceptance Criteria**:
- [ ] Chat UI renders with message history
- [ ] User can type and send messages
- [ ] Messages display in chronological order
- [ ] Loading state during agent processing
- [ ] Conversation ID persisted across page reloads
- [ ] Errors displayed gracefully

**Dependencies**: Phase 4 (chat endpoint), Phase 5 (agent logic)

**Files Created**: 6 (1 page, 3 components, 1 type definition, update api.ts)

---

### Phase 7: Testing & Validation (2-3 hours)

**Goal**: Comprehensive manual and automated testing

**Tasks**:
1. **Manual Natural Language Tests**
   - Test all user stories from spec.md
   - Edge cases: ambiguous references, invalid IDs, empty inputs
2. **Integration Tests** (`backend/tests/integration/`)
   - `test_chat_flow.py`: End-to-end conversation flow
   - `test_stateless_architecture.py`: Restart server mid-conversation
3. **Error Case Testing**
   - Invalid JWT: Expect 401
   - Wrong user_id: Expect 403
   - Task not found: Expect friendly error message
   - Cohere API failure: Expect graceful degradation
4. **Performance Testing**
   - Measure response time for typical requests
   - Verify <3 second target for 90% of requests
5. **Conversation Resume Testing**
   - Create tasks in conversation
   - Stop server
   - Restart server
   - Resume conversation → verify context maintained

**Acceptance Criteria**:
- [ ] All 12 MVP acceptance criteria pass
- [ ] All 6 user stories verified manually
- [ ] Stateless architecture confirmed (survives restarts)
- [ ] Error handling validated for all failure modes
- [ ] Response times within SLA (<3s for 90%)

**Dependencies**: Phases 1-6 (all features)

**Files Created**: 3 (2 integration tests, 1 test plan document)

---

### Phase 8: Documentation & Polish (2-3 hours)

**Goal**: Complete documentation for hackathon submission

**Tasks**:
1. **Update README.md**
   - Phase 3 architecture overview
   - Cohere API setup instructions
   - Environment variables (COHERE_API_KEY)
   - Chat endpoint documentation
   - Demo scenario instructions
2. **Create .env.example**
   - All required variables with descriptions
3. **Update requirements.txt**
   - Add cohere SDK
   - Add openai SDK (for compatibility)
   - Add mcp package
4. **Create ADR** (if not already done)
   - Document OpenAI → Cohere migration decision
   - Rationale: cost/performance, tool calling, multilingual support
5. **Create PHR for Implementation**
   - Document full implementation session
   - Link to spec, plan, tasks
6. **Final Verification**
   - Run through all 5 demo scenarios for judges
   - Verify process transparency (specs, PHRs, ADRs accessible)

**Acceptance Criteria**:
- [ ] README has Phase 3 setup instructions
- [ ] .env.example includes COHERE_API_KEY
- [ ] requirements.txt complete
- [ ] ADR documents LLM provider choice
- [ ] PHR created for implementation phase
- [ ] Demo scenarios executable in <5 minutes

**Dependencies**: Phases 1-7 (all features)

**Files Updated**: 5 (README, .env.example, requirements.txt, ADR, PHR)

---

## 10.0 Dependencies & Requirements

### 10.1 Backend Requirements (requirements.txt)

```txt
# Existing dependencies (Phase 1-2)
fastapi==0.104.1
sqlmodel==0.0.16
pydantic==2.5.0
pydantic-settings==2.1.0
uvicorn==0.24.0
psycopg2-binary==2.9.9
alembic==1.13.1
asyncpg==0.29.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
SQLAlchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# NEW: Phase 3 AI dependencies
cohere==5.0.0                    # Native Cohere SDK (fallback)
openai==1.0.0                    # OpenAI SDK for Cohere compatibility layer
mcp==0.9.0                       # Official MCP Python SDK (if available)
# Note: MCP SDK may not have PyPI package yet - check official docs
# Alternative: Implement MCP tools without SDK (just function definitions)
```

### 10.2 Frontend Requirements (package.json updates)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "14.2.5",
    "better-auth": "^1.4.10",
    
    // NEW: Phase 3 chat dependencies
    "@openai/chatkit": "^1.0.0",  // Optional: if using official ChatKit
    "react-markdown": "^8.0.0",   // For rendering formatted agent responses
    "date-fns": "^2.30.0"         // For timestamp formatting
  }
}
```

### 10.3 Environment Variables (.env.example)

```bash
# Phase 1-2: Database & Auth
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
DEBUG=True

# Phase 3: AI Integration
COHERE_API_KEY=your-cohere-api-key-here           # REQUIRED
COHERE_MODEL=command-a-03-2025                     # Optional (default)
COHERE_BASE_URL=https://api.cohere.ai/compatibility/v1  # Optional (default)

# Optional: Fallback to native Cohere SDK
USE_NATIVE_COHERE=false                            # Set to 'true' if OpenAI compatibility fails
```

### 10.4 External Dependencies

| Dependency | Type | Purpose | SLA | Fallback |
|------------|------|---------|-----|----------|
| **Cohere API** | External Service | AI agent NLP and tool calling | 99.9% uptime | Return error message to user |
| **Neon PostgreSQL** | External Service | Persistent storage | 99.95% uptime | None (critical path) |
| **Better Auth** | External Service | JWT token validation | 99.9% uptime | None (critical path) |

---

## 11.0 Cohere Integration Details

### 11.1 Tool Schema Compatibility

**Cohere's Tool Format** (native):
```python
{
    "name": "create_task",
    "description": "Creates a new task",
    "parameter_definitions": {
        "user_id": {
            "type": "int",
            "description": "User ID",
            "required": True
        },
        "title": {
            "type": "str",
            "description": "Task title",
            "required": True
        }
    }
}
```

**OpenAI-Compatible Format** (for OpenAI SDK with Cohere):
```python
{
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Creates a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "User ID"},
                "title": {"type": "string", "description": "Task title"}
            },
            "required": ["user_id", "title"]
        }
    }
}
```

**Strategy**: Use OpenAI-compatible format by default. If compatibility issues arise, convert to native Cohere format and use native SDK.

### 11.2 Model Selection Strategy

**Primary Model: command-a-03-2025**
- **Use Case**: Default for all chat requests
- **Strengths**: Optimized for agentic workflows, fast tool calling, cost-effective
- **Token Limit**: 128k context window
- **Cost**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

**Alternative Model: command-r-plus-08-2024**
- **Use Case**: Fallback for complex multi-step reasoning or very long conversations
- **Strengths**: Enhanced reasoning, longer context retention
- **Token Limit**: 128k context window
- **Cost**: ~$3.00 per 1M input tokens, ~$15.00 per 1M output tokens

**Model Selection Logic**:
```python
def select_model(conversation_length: int, complexity: str) -> str:
    """
    Select appropriate Cohere model based on conversation context.
    
    Args:
        conversation_length: Number of messages in conversation
        complexity: "simple" | "complex" (detected heuristically)
    
    Returns:
        Model name string
    """
    if conversation_length > 50 or complexity == "complex":
        return "command-r-plus-08-2024"  # Use more powerful model
    else:
        return "command-a-03-2025"  # Default to faster, cheaper model
```

### 11.3 Error Handling for API Failures

**Cohere API Error Codes**:
| Error Code | Status | Cause | Mitigation |
|------------|--------|-------|------------|
| `invalid_api_key` | 401 | API key missing/invalid | Check COHERE_API_KEY environment variable |
| `rate_limit_exceeded` | 429 | Too many requests | Implement exponential backoff, retry after delay |
| `model_not_found` | 404 | Invalid model name | Fall back to default model |
| `context_length_exceeded` | 400 | Conversation too long | Truncate history or summarize |
| `internal_server_error` | 500 | Cohere API issue | Return user-friendly error, log for monitoring |

**Error Handler Pattern**:
```python
async def execute_with_retry(func, max_retries=3):
    """Execute Cohere API call with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except CohereAPIError as e:
            if e.status_code == 429:  # Rate limit
                delay = 2 ** attempt  # Exponential backoff
                await asyncio.sleep(delay)
            elif e.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise
            else:
                raise  # Don't retry client errors (400, 401, 404)
    
    raise Exception("Max retries exceeded")
```

### 11.4 Rate Limiting Considerations

**Cohere Free Tier Limits** (example - verify actual limits):
- 100 requests/minute
- 10,000 requests/day

**Mitigation Strategies**:
1. **Client-Side Throttling**: Debounce user input (prevent spam)
2. **Backend Queue**: Queue requests during high traffic
3. **Caching**: Cache common responses (e.g., "help", "show tasks")
4. **Graceful Degradation**: If rate limited, queue request and notify user of delay

---

## 12.0 Risks & Mitigations

### Risk Matrix

| Risk | Likelihood | Impact | Severity | Mitigation |
|------|------------|--------|----------|------------|
| **Tool Calling Compatibility Issues** | Medium | High | CRITICAL | Test early with simple tool, have native Cohere SDK fallback |
| **OpenAI SDK Compatibility Limitations** | Medium | Medium | HIGH | Document differences, implement native SDK alternative |
| **Database Transaction Safety** | Low | High | MEDIUM | Use SQLModel's session management, test concurrent requests |
| **JWT Validation Security Flaws** | Low | Critical | HIGH | Use established python-jose library, validate in middleware |
| **CORS and Domain Allowlisting** | Low | Medium | LOW | Configure CORS middleware properly, test from frontend |
| **Cohere API Rate Limiting** | Medium | Medium | MEDIUM | Implement exponential backoff, monitor usage |
| **Conversation History Pagination** | Low | Low | LOW | Implement limit/offset in message retrieval |
| **Agent Hallucination (Making Up Tasks)** | Low | Medium | MEDIUM | Clear system prompt, always call tools for data |
| **Multi-Step Reasoning Failure** | Medium | Medium | MEDIUM | Test complex scenarios, log tool call chains |
| **Frontend State Management Bugs** | Medium | Low | LOW | Use simple useState, test conversation resume |

### 12.1 Critical Risk: Tool Calling Compatibility

**Scenario**: Cohere's tool calling via OpenAI SDK compatibility endpoint doesn't work as expected.

**Early Detection**:
- **Phase 2**: Implement simple test script that calls Cohere API with a single tool
- **Test Code**:
  ```python
  # test_cohere_tool_calling.py
  from openai import OpenAI
  
  client = OpenAI(
      api_key=os.getenv("COHERE_API_KEY"),
      base_url="https://api.cohere.ai/compatibility/v1"
  )
  
  tools = [
      {
          "type": "function",
          "function": {
              "name": "get_weather",
              "description": "Get weather for a city",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "city": {"type": "string"}
                  },
                  "required": ["city"]
              }
          }
      }
  ]
  
  response = client.chat.completions.create(
      model="command-a-03-2025",
      messages=[{"role": "user", "content": "What's the weather in NYC?"}],
      tools=tools
  )
  
  print(response.choices[0].message.tool_calls)
  ```

**If Compatibility Fails**:
- **Fallback 1**: Use native Cohere SDK
- **Fallback 2**: Manually parse tool intent from agent response (less reliable)

### 12.2 Medium Risk: Database Transaction Safety

**Scenario**: Concurrent requests create race conditions (e.g., duplicate tasks, lost updates).

**Mitigation**:
- Use SQLModel's session management (automatic transaction handling)
- Add database constraints (unique indexes where needed)
- Test concurrent requests:
  ```python
  # Test concurrent task creation
  async def test_concurrent_creates():
      tasks = [
          create_task(user_id=1, title=f"Task {i}")
          for i in range(10)
      ]
      results = await asyncio.gather(*tasks)
      assert len(results) == 10  # All succeeded
      assert len(set(r["task_id"] for r in results)) == 10  # All unique
  ```

### 12.3 Medium Risk: Agent Hallucination

**Scenario**: Agent invents tasks or tool results instead of calling actual tools.

**Mitigation**:
1. **Clear System Prompt**: Emphasize "Always use tools, never make up data"
2. **Tool Enforcement**: In system prompt, state "You MUST call tools to retrieve task data"
3. **Validation**: Log all tool calls, verify agent doesn't return task data without calling list_tasks
4. **Example System Prompt Addition**:
   ```
   CRITICAL: Never make up task data. Always call list_tasks() to retrieve current tasks.
   If you don't have data from a tool call, say "Let me check your tasks" and call the tool.
   ```

---

## 13.0 Timeline Estimate

### 13.1 Detailed Task Breakdown

| Phase | Task | Est. Hours | Parallel? | Dependencies |
|-------|------|-----------|-----------|--------------|
| **Phase 1** | Database models | 1.0 | No | None |
| | Alembic migrations | 0.5 | No | Models |
| | ConversationService | 1.0 | No | Models |
| | Testing | 0.5 | No | Service |
| **Phase 2** | Tool schemas | 1.0 | Yes | None |
| | Implement 5 tools | 2.0 | Yes | Schemas |
| | Tool tests | 1.5 | No | Tools |
| **Phase 3** | Update config | 0.5 | Yes | None |
| | Verify JWT middleware | 0.5 | Yes | None |
| **Phase 4** | Chat schemas | 0.5 | Yes | None |
| | Chat endpoint | 2.0 | No | Schemas |
| | Manual testing | 0.5 | No | Endpoint |
| **Phase 5** | System prompt | 1.0 | Yes | None |
| | Cohere client | 1.5 | No | System prompt |
| | AgentService | 2.0 | No | Client |
| | Early testing | 1.0 | No | AgentService |
| **Phase 6** | Chat UI components | 2.0 | Yes | None |
| | API integration | 1.0 | No | Components |
| | Frontend testing | 0.5 | No | Integration |
| **Phase 7** | Manual NL tests | 1.0 | Yes | All |
| | Integration tests | 1.0 | Yes | All |
| | Error case testing | 0.5 | No | Tests |
| **Phase 8** | Documentation | 1.5 | Yes | All |
| | PHR/ADR creation | 0.5 | Yes | All |
| | Final verification | 0.5 | No | All |

### 13.2 Timeline Summary

**Total Effort**: ~25 hours (raw task time)

**Calendar Time** (with parallelization and breaks):
- **Day 1**: Phases 1-3 (Database, MCP Tools, Auth) → 6-7 hours
- **Day 2**: Phases 4-6 (Chat Endpoint, Agent, Frontend) → 7-8 hours
- **Day 3**: Phases 7-8 (Testing, Documentation) → 3-4 hours

**Aggressive Timeline**: 1.5-2 focused days (12-16 hours)

**Comfortable Timeline**: 3 days (allowing for breaks, troubleshooting)

### 13.3 Critical Path

```mermaid
graph LR
    P1[Phase 1: DB] --> P2[Phase 2: MCP Tools]
    P2 --> P4[Phase 4: Chat Endpoint]
    P4 --> P5[Phase 5: Agent Logic]
    P5 --> P6[Phase 6: Frontend]
    P6 --> P7[Phase 7: Testing]
    P7 --> P8[Phase 8: Documentation]
    
    P3[Phase 3: Auth] -.->|Parallel| P4
    
    style P1 fill:#ffcccc
    style P2 fill:#ffcccc
    style P5 fill:#ffcccc
    style P7 fill:#ffcccc
```

**Critical Path**: Phase 1 → 2 → 4 → 5 → 6 → 7 → 8 (cannot parallelize)

**Parallelizable Work**:
- Phase 3 (Auth updates) can run parallel to Phase 2 (MCP tools)
- Within Phase 2: All 5 tools can be implemented in parallel
- Within Phase 6: UI components can be built in parallel
- Within Phase 7: Manual tests and integration tests can run in parallel

### 13.4 Parallel Work Opportunities

**Day 1 Parallelization**:
- While implementing MCP tools (Phase 2), update config and verify auth (Phase 3)
- Team of 2: One person on tools, one on database/config

**Day 2 Parallelization**:
- While implementing agent logic (Phase 5), start building frontend components (Phase 6)
- Team of 2: One person on backend agent, one on frontend UI

**Day 3 Parallelization**:
- Manual testing and integration tests can run simultaneously
- Documentation and testing can overlap

---

## 14.0 Testing Strategy

### 14.1 Manual Natural Language Command Tests

**Test Suite** (aligned with spec.md user stories):

```markdown
# Phase 3 Manual Test Plan

## Test Environment Setup
1. Start backend: `uvicorn src.main:app --reload`
2. Start frontend: `npm run dev` (in frontend-todo-app/)
3. Create test user account
4. Get JWT token from login

## Test Cases

### TC-001: Create Task (US1)
**User Input**: "Add buy groceries"
**Expected**: Task created with title "buy groceries"
**Verification**: Agent responds "✓ Added task #N: Buy groceries"
**Pass/Fail**: ___

### TC-002: Create Task with Details (US1)
**User Input**: "Remind me to call mom tomorrow at 5pm"
**Expected**: Task created with title "call mom"
**Verification**: Agent confirms with task details
**Pass/Fail**: ___

### TC-003: Incomplete Create Request (US1 - Edge Case)
**User Input**: "Add"
**Expected**: Agent asks for clarification
**Verification**: Agent responds "What would you like to add to your task list?"
**Pass/Fail**: ___

### TC-004: List All Tasks (US2)
**User Input**: "Show my tasks"
**Expected**: All tasks listed with IDs and titles
**Verification**: Agent lists tasks in bullet format
**Pass/Fail**: ___

### TC-005: List Pending Tasks (US2)
**User Input**: "Show my pending tasks"
**Expected**: Only pending tasks listed
**Verification**: Agent filters correctly
**Pass/Fail**: ___

### TC-006: List Tasks - Empty (US2 - Edge Case)
**User Input**: "Show my tasks" (when no tasks exist)
**Expected**: Agent responds helpfully
**Verification**: Agent says "You don't have any tasks yet. Would you like to add one?"
**Pass/Fail**: ___

### TC-007: Complete Task by ID (US3)
**User Input**: "Complete task 3"
**Expected**: Task #3 marked as completed
**Verification**: Agent confirms "✓ Marked task #3 '[title]' as complete!"
**Pass/Fail**: ___

### TC-008: Complete Task by Name (US3 - Multi-Step)
**User Input**: "I finished calling mom"
**Expected**: Agent finds task, marks complete
**Verification**: Agent confirms with task ID and title
**Pass/Fail**: ___

### TC-009: Complete Non-Existent Task (US3 - Error)
**User Input**: "Complete task 999"
**Expected**: Friendly error message
**Verification**: Agent responds "I couldn't find task #999. Try typing 'show my tasks' to see your list."
**Pass/Fail**: ___

### TC-010: Delete Task with Confirmation (US4)
**User Input**: "Delete task 5" → "yes"
**Expected**: Task deleted after confirmation
**Verification**: Agent asks for confirmation, then confirms deletion
**Pass/Fail**: ___

### TC-011: Update Task Title (US5)
**User Input**: "Update task 2 to 'Buy organic milk'"
**Expected**: Task #2 title changed
**Verification**: Agent confirms "✓ Updated task #2 to 'Buy organic milk'"
**Pass/Fail**: ___

### TC-012: Conversation Continuity (US6)
**Steps**:
1. Create 3 tasks in conversation
2. Close browser/restart server
3. Reopen chat with same conversation_id
4. Send new message
**Expected**: Full conversation history loaded, agent has context
**Verification**: Agent references previous tasks
**Pass/Fail**: ___
```

### 14.2 Error Case Testing

**Error Test Cases**:

```python
# backend/tests/integration/test_error_cases.py

import pytest
from fastapi.testclient import TestClient
from backend.src.main import app

client = TestClient(app)

def test_missing_jwt():
    """Test chat endpoint without JWT token"""
    response = client.post("/api/1/chat", json={"message": "Hello"})
    assert response.status_code == 401
    assert "unauthorized" in response.json()["error"]

def test_wrong_user_id():
    """Test accessing another user's conversation"""
    jwt_user_1 = get_jwt_for_user(1)
    response = client.post(
        "/api/2/chat",  # Wrong user_id
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {jwt_user_1}"}
    )
    assert response.status_code == 403
    assert "forbidden" in response.json()["error"]

def test_invalid_conversation_id():
    """Test resuming non-existent conversation"""
    jwt = get_jwt_for_user(1)
    response = client.post(
        "/api/1/chat",
        json={"message": "Hello", "conversation_id": 99999},
        headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["error"]

@pytest.mark.asyncio
async def test_cohere_api_failure(mock_cohere):
    """Test graceful handling of Cohere API failure"""
    mock_cohere.side_effect = Exception("API timeout")
    jwt = get_jwt_for_user(1)
    response = client.post(
        "/api/1/chat",
        json={"message": "Add buy groceries"},
        headers={"Authorization": f"Bearer {jwt}"}
    )
    assert response.status_code == 500
    assert "try again" in response.json()["message"].lower()
```

### 14.3 Conversation Resume Testing

**Test Procedure**:

1. **Setup**:
   ```bash
   # Terminal 1: Start backend
   uvicorn src.main:app --reload
   
   # Terminal 2: Start frontend
   cd frontend-todo-app && npm run dev
   ```

2. **Create Conversation**:
   - User 1 logs in
   - Sends message: "Add buy groceries"
   - Sends message: "Add call mom"
   - Sends message: "Show my tasks"
   - Note conversation_id from response

3. **Simulate Server Restart**:
   ```bash
   # Terminal 1: Stop server (Ctrl+C)
   # Wait 5 seconds
   # Restart server
   uvicorn src.main:app --reload
   ```

4. **Resume Conversation**:
   - Frontend reloads chat with same conversation_id
   - User sends: "Complete buy groceries"
   - **Expected**: Agent has full context, knows about both tasks

5. **Verification**:
   - Agent response references previous tasks
   - Database check: All messages persisted
   - No errors in logs

**Acceptance**: Test passes if agent correctly completes "buy groceries" task despite server restart.

### 14.4 Performance Testing

**Response Time Test**:

```python
# backend/tests/integration/test_performance.py

import pytest
import time
from statistics import mean, quantile

@pytest.mark.asyncio
async def test_chat_response_time():
    """Verify 90% of requests complete in <3 seconds"""
    jwt = get_jwt_for_user(1)
    
    response_times = []
    
    for i in range(100):  # 100 requests
        start = time.time()
        response = client.post(
            "/api/1/chat",
            json={"message": f"Add task {i}"},
            headers={"Authorization": f"Bearer {jwt}"}
        )
        end = time.time()
        
        assert response.status_code == 200
        response_times.append(end - start)
    
    # Calculate statistics
    p90 = quantile(response_times, 0.9)
    p95 = quantile(response_times, 0.95)
    avg = mean(response_times)
    
    print(f"Average: {avg:.2f}s")
    print(f"P90: {p90:.2f}s")
    print(f"P95: {p95:.2f}s")
    
    # Assert SLA
    assert p90 < 3.0, f"P90 response time {p90:.2f}s exceeds 3s target"
```

---

## 15.0 Deliverables Checklist

### 15.1 MVP Acceptance Criteria (from spec.md)

- [ ] **AC-1**: User can type "Add buy groceries" and task is created with confirmation
- [ ] **AC-2**: User can type "Show my tasks" or "List pending tasks" and see filtered results
- [ ] **AC-3**: User can type "Complete task 3" or "Mark buy groceries done" and status updates with confirmation
- [ ] **AC-4**: User can type "Delete task 5" with confirmation prompt, then task is removed
- [ ] **AC-5**: User can type "Update task 2 to 'Buy organic milk'" and title changes
- [ ] **AC-6**: User can close/reopen browser or server restarts, and conversation history loads correctly
- [ ] **AC-7**: All endpoints validate JWT and enforce user_id authorization (401/403 errors)
- [ ] **AC-8**: Agent provides helpful guidance when tasks not found, input unclear, or operations fail
- [ ] **AC-9**: No in-memory state in backend; all state persisted to database; agent instantiated fresh per request
- [ ] **AC-10**: All 5 tools (add, list, complete, delete, update) implemented via MCP and callable by agent
- [ ] **AC-11**: PHRs created for specification, planning, task generation, and implementation phases
- [ ] **AC-12**: README updated with setup instructions, architecture overview, API documentation

### 15.2 GitHub Repository Structure

```
phase-3/
├── README.md                 ✅ Updated with Phase 3 instructions
├── .env.example              ✅ Includes COHERE_API_KEY
├── backend/
│   ├── src/
│   │   ├── api/v1/chat.py    ✅ Stateless chat endpoint
│   │   ├── agent/            ✅ Agent logic (system prompt, Cohere client)
│   │   ├── models/           ✅ Conversation & Message models
│   │   └── services/         ✅ AgentService, ConversationService
│   ├── mcp_server/           ✅ 5 MCP tools with Cohere schemas
│   ├── requirements.txt      ✅ Includes cohere, openai, mcp
│   └── tests/                ✅ Unit & integration tests
├── frontend-todo-app/
│   └── src/app/chat/         ✅ Chat UI page
├── specs/004-ai-todo-chatbot/
│   ├── spec.md               ✅ Feature specification
│   ├── plan.md               ✅ THIS FILE
│   ├── tasks.md              📝 To be generated with /sp.tasks
│   └── contracts/            ✅ API & tool contracts
├── history/
│   ├── prompts/4-ai-todo-chatbot/  ✅ PHRs for all phases
│   └── adr/                  ✅ ADR for Cohere migration
└── .specify/
    └── memory/constitution.md  ✅ v2.0.1 (Cohere API)
```

### 15.3 Documentation Checklist

- [ ] **README**: Phase 3 setup instructions (Cohere API key, environment variables)
- [ ] **README**: Architecture diagram (system overview with Cohere integration)
- [ ] **README**: Chat endpoint documentation with example requests/responses
- [ ] **README**: Demo scenario instructions for judges
- [ ] **.env.example**: All Phase 3 variables documented (COHERE_API_KEY, COHERE_MODEL)
- [ ] **ADR**: OpenAI → Cohere migration decision documented
- [ ] **PHR**: Implementation session recorded with all phases
- [ ] **contracts/api-endpoints.md**: Chat endpoint contract
- [ ] **contracts/mcp-tool-contracts.md**: All 5 tools documented
- [ ] **contracts/database-schema.md**: Conversation & Message tables

---

## 16.0 Next Steps

### 16.1 Immediate Actions

**Step 1: Generate Tasks Document**
```bash
/sp.tasks
```
- Convert this plan into ordered, testable tasks
- Add acceptance criteria to each task
- Identify dependencies and parallel work
- Output: `specs/004-ai-todo-chatbot/tasks.md`

**Step 2: Early Cohere Testing**
```bash
# Test Cohere API connection before Phase 5
python -c "
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv('COHERE_API_KEY'),
    base_url='https://api.cohere.ai/compatibility/v1'
)
response = client.chat.completions.create(
    model='command-a-03-2025',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(response.choices[0].message.content)
"
```
- Verify API key works
- Test tool calling with simple example
- Confirm OpenAI SDK compatibility

**Step 3: Review Constitutional Compliance**
- [ ] Verify stateless architecture (no global state)
- [ ] Verify MCP tools only (no direct DB access in agent)
- [ ] Verify Cohere API integration (no OpenAI native)
- [ ] Verify COHERE_API_KEY environment variable usage
- [ ] Verify all code via Claude Code (no manual coding)

### 16.2 Implementation Commands

**After tasks.md generated**:
```bash
# Implement all tasks
/sp.implement

# During implementation, use custom skills
/todo_mcp_helper    # For MCP tool guidance
```

**After implementation complete**:
```bash
# Create ADR for Cohere migration
/sp.adr cohere-api-migration

# Analyze cross-artifact consistency
/sp.analyze

# Create PHR for implementation
/sp.phr --stage implement --feature ai-todo-chatbot

# Create pull request
/sp.git.commit_pr
```

### 16.3 Custom Skills to Use

1. **todo_mcp_helper**
   - Use during Phase 2 (MCP tool implementation)
   - Use during Phase 5 (agent behavior design)
   - Command: `/todo_mcp_helper [question]`

2. **fastapi-endpoint-generator** (if available)
   - Use during Phase 4 (chat endpoint)
   - Command: `/fastapi-endpoint-generator chat endpoint`

### 16.4 Validation Checkpoints

**After Phase 2 (MCP Tools)**:
- [ ] Run unit tests: `pytest backend/tests/unit/test_mcp_tools.py`
- [ ] Verify all 5 tools work independently
- [ ] Check user isolation (cross-user access blocked)

**After Phase 5 (Agent Logic)**:
- [ ] Test simple tool call: "Add buy groceries"
- [ ] Test tool chaining: "Complete buy groceries"
- [ ] Test no-tool response: "Hello"
- [ ] Verify conversation history passed correctly

**After Phase 7 (Testing)**:
- [ ] All 12 manual test cases pass
- [ ] All 6 user stories verified
- [ ] Stateless architecture confirmed (server restart test)
- [ ] Performance SLA met (<3s for 90% of requests)

**Before Submission**:
- [ ] Run all tests: `pytest backend/tests/`
- [ ] Run demo scenarios (5 scenarios from spec.md)
- [ ] Verify process transparency (PHRs, ADRs, specs accessible)
- [ ] Check README completeness (setup instructions, architecture)

---

## 17.0 Constitutional Compliance Verification

### 17.1 Stateless Architecture Compliance

**Requirement**: All server components must be stateless (Constitution Principle 3)

**Verification Checklist**:
- [ ] No global variables storing conversation state
- [ ] No in-memory caches or session stores
- [ ] Agent instantiated fresh on every `/chat` request
- [ ] Conversation history fetched from DB on every request
- [ ] MCP tools operate independently (no shared state)
- [ ] SQLModel sessions closed after each request
- [ ] Server can restart mid-conversation without data loss

**Evidence**: Stateless chat endpoint implementation (Phase 4), ConversationService DB retrieval (Phase 1)

### 17.2 MCP Tool Integration Compliance

**Requirement**: All AI capabilities via MCP tools (Constitution Principle 4)

**Verification Checklist**:
- [ ] 5 required tools implemented: create_task, list_tasks, update_task, delete_task, complete_task
- [ ] Tools use Official MCP Python SDK patterns (or compatible implementation)
- [ ] Cohere-compatible JSON schemas for all tools
- [ ] All tools enforce user_id filtering (data isolation)
- [ ] Tools use SQLModel for database operations
- [ ] Structured error responses for all failure cases
- [ ] No direct database access in agent logic (only via tools)

**Evidence**: MCP tool implementations (Phase 2), tool schema definitions (Phase 2)

### 17.3 AI Agent Integration Compliance

**Requirement**: Cohere API only, via OpenAI SDK compatibility (Constitution Principle 5)

**Verification Checklist**:
- [ ] Cohere API used (not OpenAI native)
- [ ] Primary model: command-a-03-2025
- [ ] Alternative model: command-r-plus-08-2024
- [ ] API configuration: base_url = "https://api.cohere.ai/compatibility/v1"
- [ ] Environment variable: COHERE_API_KEY (never hardcoded)
- [ ] OpenAI SDK with Cohere compatibility endpoint
- [ ] Native Cohere SDK available as fallback
- [ ] Fresh agent instance on every request (stateless)
- [ ] All tool calls persisted to database

**Evidence**: AgentService implementation (Phase 5), config.py updates (Phase 3)

### 17.4 Spec-Driven Development Compliance

**Requirement**: No implementation before specification (Constitution Principle 1)

**Verification Checklist**:
- [ ] spec.md created before plan.md ✅
- [ ] plan.md created before tasks.md (next step)
- [ ] tasks.md created before implementation (pending)
- [ ] All code generated via Claude Code (no manual editing)
- [ ] PHRs created for all phases ✅ (constitution, spec completed)
- [ ] ADR created for significant decisions (Cohere migration) ✅

**Evidence**: Directory structure (specs/004-ai-todo-chatbot/), PHR history

### 17.5 Security Compliance

**Requirement**: JWT validation, zero-trust authorization (Constitution Principle 7)

**Verification Checklist**:
- [ ] JWT validation on all endpoints except /auth
- [ ] User ID extracted from JWT payload (not URL/body)
- [ ] URL path user_id matches JWT user_id
- [ ] 401 for missing/invalid JWT
- [ ] 403 for cross-user access attempts
- [ ] No hardcoded secrets (all via environment variables)
- [ ] SQLModel parameterized queries (SQL injection prevention)

**Evidence**: JWT middleware (Phase 3), chat endpoint authorization (Phase 4)

---

## 18.0 Appendix: Code Snippets

### A.1 Complete Cohere Client Example

```python
# backend/src/agent/cohere_client.py
from openai import OpenAI
import os
from typing import List, Dict, Any, Optional
import json

class CohereClient:
    """
    Wrapper around OpenAI SDK configured for Cohere API compatibility.
    
    Supports fallback to native Cohere SDK if compatibility issues arise.
    """
    
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        
        self.model = os.getenv("COHERE_MODEL", "command-a-03-2025")
        self.base_url = os.getenv(
            "COHERE_BASE_URL",
            "https://api.cohere.ai/compatibility/v1"
        )
        
        # Initialize OpenAI client with Cohere endpoint
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Execute chat completion with Cohere via OpenAI SDK compatibility.
        
        Args:
            messages: Conversation history [{"role": str, "content": str}]
            tools: Optional tool definitions (OpenAI format)
            temperature: Sampling temperature
            max_tokens: Max tokens in response
        
        Returns:
            Dict with "message" and optional "tool_calls"
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "message": response.choices[0].message,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            # Log error and raise
            print(f"Cohere API error: {str(e)}")
            raise
    
    def native_fallback(
        self,
        message: str,
        chat_history: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Fallback to native Cohere SDK if OpenAI compatibility fails.
        
        Args:
            message: User's message
            chat_history: Previous messages
            tools: Tool definitions (convert to Cohere format)
        
        Returns:
            Dict with "message" and optional "tool_calls"
        """
        import cohere
        
        co = cohere.Client(api_key=self.api_key)
        
        # Convert tools to Cohere format
        cohere_tools = self._convert_tools_to_cohere(tools) if tools else None
        
        response = co.chat(
            model=self.model,
            message=message,
            chat_history=chat_history,
            tools=cohere_tools,
            force_single_step=False
        )
        
        return {
            "message": response.text,
            "tool_calls": response.tool_calls if hasattr(response, "tool_calls") else None
        }
    
    def _convert_tools_to_cohere(
        self,
        openai_tools: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Convert OpenAI tool format to Cohere native format.
        
        OpenAI format:
        {
            "type": "function",
            "function": {
                "name": "create_task",
                "description": "...",
                "parameters": {"type": "object", "properties": {...}}
            }
        }
        
        Cohere format:
        {
            "name": "create_task",
            "description": "...",
            "parameter_definitions": {
                "user_id": {"type": "int", "description": "...", "required": True}
            }
        }
        """
        cohere_tools = []
        
        for tool in openai_tools:
            func = tool["function"]
            parameters = func["parameters"]["properties"]
            required = func["parameters"].get("required", [])
            
            param_defs = {}
            for param_name, param_schema in parameters.items():
                param_defs[param_name] = {
                    "type": param_schema["type"],
                    "description": param_schema.get("description", ""),
                    "required": param_name in required
                }
            
            cohere_tools.append({
                "name": func["name"],
                "description": func["description"],
                "parameter_definitions": param_defs
            })
        
        return cohere_tools
```

### A.2 Stateless Chat Endpoint (Complete)

```python
# backend/src/api/v1/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any

from backend.src.schemas.chat import ChatRequest, ChatResponse
from backend.src.core.auth import get_current_user
from backend.src.database.connection import get_session
from backend.src.services.conversation_service import ConversationService
from backend.src.services.agent_service import AgentService
from backend.src.models.user import User

router = APIRouter()

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Stateless chat endpoint for conversational task management.
    
    This endpoint:
    1. Validates JWT and matches user_id
    2. Gets/creates conversation from database
    3. Fetches full conversation history from database
    4. Instantiates fresh Cohere agent (no cached state)
    5. Executes agent with history + new message
    6. Saves user message and agent response to database
    7. Returns response with conversation_id
    
    Stateless guarantees:
    - No in-memory conversation state
    - Server can restart mid-conversation without data loss
    - Full history retrieved from DB on every request
    - Fresh agent instance per request
    
    Args:
        user_id: User ID from URL path
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user (from JWT middleware)
        session: Database session (from FastAPI dependency)
    
    Returns:
        ChatResponse with agent's message, conversation_id, and tool calls
    
    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 404: If conversation_id not found or not owned by user
        HTTPException 500: If agent execution fails
    """
    # 1. Validate authorization
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )
    
    # 2. Get or create conversation
    conversation_service = ConversationService(session)
    
    if request.conversation_id:
        # Resume existing conversation
        conversation = conversation_service.get_conversation(
            conversation_id=request.conversation_id,
            user_id=user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {request.conversation_id} not found or not accessible"
            )
    else:
        # Create new conversation
        conversation = conversation_service.create_conversation(user_id=user_id)
    
    # 3. Fetch conversation history from DB (stateless - no cache)
    history = conversation_service.get_conversation_history(conversation.id)
    
    # 4. Save user message to DB
    user_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    
    # 5. Instantiate fresh agent and execute (stateless)
    agent_service = AgentService()
    
    try:
        agent_response = await agent_service.execute(
            user_id=user_id,
            message=request.message,
            history=history
        )
    except Exception as e:
        # Log error (in production, use structured logging)
        print(f"Agent execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process your message. Please try again."
        )
    
    # 6. Save agent response to DB
    assistant_message = conversation_service.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content=agent_response["message"],
        tool_calls=agent_response.get("tool_calls")
    )
    
    # 7. Return response
    return ChatResponse(
        message=agent_response["message"],
        conversation_id=conversation.id,
        tool_calls=agent_response.get("tool_calls")
    )


# Optional: Health check endpoint for chat service
@router.get("/health")
async def chat_health():
    """Health check for chat service"""
    return {
        "status": "healthy",
        "service": "chat",
        "stateless": True
    }
```

---

## Critical Files for Implementation

Based on this plan, here are the 5 most critical files for implementing the AI Todo Chatbot:

1. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/api/v1/chat.py`** - [NEW] Core stateless chat endpoint that orchestrates the entire conversation flow, validates JWT, manages conversation persistence, and calls the agent

2. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/services/agent_service.py`** - [NEW] Agent service that integrates Cohere API, executes tool calls via MCP, and handles multi-step reasoning - this is the brain of the system

3. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/mcp_server/schemas/tool_definitions.py`** - [NEW] Cohere-compatible tool schemas that define all 5 MCP tools - critical for agent tool calling functionality

4. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/models/conversation.py`** - [NEW] Conversation and Message SQLModel definitions that enable stateless architecture by persisting all conversation state to database

5. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/agent/system_prompt.py`** - [NEW] System prompt that defines agent behavior, tool usage patterns, and response style - determines the quality of the conversational experience

**Additional Critical Files** (if expanding to top 10):

6. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/services/conversation_service.py`** - [NEW] Database service for managing conversations and messages
7. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/mcp_server/tools/create_task.py`** - [NEW] Pattern for MCP tool implementation (all 5 tools follow similar structure)
8. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/src/core/config.py`** - [UPDATE] Add COHERE_API_KEY environment variable
9. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/backend/requirements.txt`** - [UPDATE] Add cohere, openai, and mcp dependencies
10. **`/mnt/c/Users/Daniyal Shaikh/Desktop/hackathon 2/phase-3/frontend-todo-app/src/app/chat/page.tsx`** - [NEW] Chat UI interface for user interaction

---

**Plan Version**: 1.0  
**Created**: 2026-02-07  
**Author**: Claude Code (Sonnet 4.5)  
**Constitution Version**: 2.0.1 (Cohere API)  
**Spec Version**: 1.1 (Updated with Cohere)  
**Status**: Ready for Task Generation  
**Next Step**: Run `/sp.tasks` to generate implementation tasks