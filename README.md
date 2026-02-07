# AI-Powered Todo Chatbot - Hackathon II Phase 3

A conversational AI interface for managing todo tasks through natural language, built with Cohere API, FastAPI, and React.

## 🎯 Project Overview

This project demonstrates a stateless, AI-powered task management system where users interact with their todos through natural conversation instead of traditional CRUD interfaces.

**Key Features:**
- 🤖 Natural language task management ("Add buy groceries", "Show my pending tasks")
- 💬 Conversational AI powered by Cohere's Command-A model
- 🔧 MCP (Model Context Protocol) tools for standardized AI-database interaction
- 🔄 Stateless architecture - survives server restarts without data loss
- 🔐 JWT-based authentication with multi-user isolation
- 📱 Modern React/Next.js chat interface

## 🏗️ Architecture

### High-Level Overview

```
Frontend (Next.js) → FastAPI Backend → Cohere Agent → MCP Tools → PostgreSQL
```

**Stateless Design:**
- Fresh agent instantiation per request
- Conversation history stored in PostgreSQL
- No in-memory state - fully scalable

### Components

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **AI Agent**: Cohere API (command-a-03-2025) via OpenAI SDK compatibility
- **Tools**: 5 MCP tools (create, list, update, delete, complete tasks)
- **Database**: Neon PostgreSQL (serverless)
- **Auth**: JWT-based authentication (Better Auth compatible)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon account)
- Cohere API key (get from [cohere.com](https://cohere.com))

### Backend Setup

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # - DATABASE_URL (Neon PostgreSQL connection string)
   # - COHERE_API_KEY (from cohere.com)
   # - SECRET_KEY (for JWT)
   ```

5. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start backend server:**
   ```bash
   uvicorn src.main:app --reload --port 8001
   ```

   Backend will be available at `http://localhost:8001`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend-todo-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   # Create .env.local
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
   ```

4. **Start frontend:**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

### Usage

1. **Register/Login** at `http://localhost:3000/auth`
2. **Navigate to Chat** at `http://localhost:3000/chat`
3. **Start conversing:**
   - "Add buy groceries"
   - "Show my tasks"
   - "Complete task 1"
   - "Delete task 2"
   - "Update task 3 to 'Buy organic milk'"

## 📁 Project Structure

```
phase-3/
├── backend/
│   ├── src/
│   │   ├── api/v1/
│   │   │   ├── auth.py           # JWT authentication endpoints
│   │   │   ├── tasks.py          # Traditional CRUD endpoints
│   │   │   └── chat.py           # 🆕 Conversational chat endpoint
│   │   ├── agent/
│   │   │   ├── system_prompt.py  # 🆕 AI assistant instructions
│   │   │   └── cohere_client.py  # 🆕 Cohere API wrapper
│   │   ├── models/
│   │   │   ├── task.py           # Task entity
│   │   │   ├── user.py           # User entity
│   │   │   ├── conversation.py   # 🆕 Conversation entity
│   │   │   └── message.py        # 🆕 Message entity
│   │   ├── services/
│   │   │   ├── agent_service.py       # 🆕 Agent orchestration
│   │   │   └── conversation_service.py # 🆕 Conversation management
│   │   └── schemas/
│   │       └── chat.py           # 🆕 Chat request/response schemas
│   ├── mcp_server/               # 🆕 MCP Tools
│   │   ├── tools/
│   │   │   ├── create_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── delete_task.py
│   │   │   └── update_task.py
│   │   ├── schemas/
│   │   │   └── tool_definitions.py  # Cohere-compatible schemas
│   │   └── server.py             # MCP server initialization
│   ├── alembic/
│   │   └── versions/
│   │       ├── 001_initial_task_table.py
│   │       ├── 002_add_conversations_table.py  # 🆕
│   │       └── 003_add_messages_table.py       # 🆕
│   └── requirements.txt
├── frontend-todo-app/
│   ├── src/
│   │   ├── app/
│   │   │   └── chat/
│   │   │       └── page.tsx      # 🆕 Chat interface page
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx    # 🆕 Main chat container
│   │   │   ├── MessageList.tsx      # 🆕 Message display
│   │   │   └── MessageInput.tsx     # 🆕 Input component
│   │   ├── lib/
│   │   │   └── api.ts            # Updated with chat API
│   │   └── types/
│   │       └── chat.ts           # 🆕 Chat TypeScript types
│   └── package.json
├── specs/
│   └── 004-ai-todo-chatbot/
│       ├── spec.md               # Feature specification
│       ├── plan.md               # Technical architecture
│       └── tasks.md              # Implementation tasks (104 total)
└── README.md                     # This file
```

## 🛠️ API Endpoints

### Chat Endpoint (Phase 3)

**POST** `/api/{user_id}/chat`
- Stateless conversational interface
- Request: `{"message": "Add buy groceries", "conversation_id": 123}`
- Response: `{"message": "✓ Added task #5: Buy groceries", "conversation_id": 123, "tool_calls": [...]}`

### Traditional CRUD (Phase 1-2)

- **POST** `/api/todos` - Create task
- **GET** `/api/todos` - List tasks
- **PUT** `/api/todos/{task_id}` - Update task
- **DELETE** `/api/todos/{task_id}` - Delete task
- **PATCH** `/api/todos/{task_id}` - Toggle completion

### Authentication

- **POST** `/api/auth/signup` - Register
- **POST** `/api/auth/login` - Login (returns JWT)

## 🧪 Testing

### Manual Testing Scenarios

1. **Task Creation (US1)**
   ```
   User: "Add buy groceries"
   Agent: "✓ Added task #1: Buy groceries"
   ```

2. **Task Viewing (US2)**
   ```
   User: "Show my pending tasks"
   Agent: "You have 1 pending task: • Task #1: Buy groceries"
   ```

3. **Task Completion (US3)**
   ```
   User: "Complete buy groceries"
   Agent: "✓ Marked task #1 'Buy groceries' as complete! Great job!"
   ```

4. **Stateless Architecture (US6)**
   - Create tasks in conversation
   - Stop server (`Ctrl+C`)
   - Restart server
   - Send new message with same conversation_id
   - Verify context maintained ✓

### Acceptance Criteria

All 12 MVP acceptance criteria from spec.md:
- ✅ Task creation via natural language
- ✅ Task listing with status filters
- ✅ Task completion by ID or name
- ✅ Task deletion with confirmation
- ✅ Task updates
- ✅ Conversation persistence across restarts
- ✅ JWT authentication with 401/403 errors
- ✅ Error handling and friendly messages
- ✅ Stateless architecture (no in-memory state)
- ✅ MCP tools implementation
- ✅ Process documentation (PHRs, specs, plans)
- ✅ README with setup instructions

## 🔑 Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Authentication
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cohere API (Phase 3)
COHERE_API_KEY=your-cohere-api-key
COHERE_MODEL=command-a-03-2025
COHERE_BASE_URL=https://api.cohere.ai/compatibility/v1

# Application
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

## 📚 Documentation

- **Specification**: `specs/004-ai-todo-chatbot/spec.md`
- **Architecture Plan**: `specs/004-ai-todo-chatbot/plan.md`
- **Implementation Tasks**: `specs/004-ai-todo-chatbot/tasks.md`
- **Constitution**: `.specify/memory/constitution.md` (v2.0.1)
- **Prompt History Records**: `history/prompts/4-ai-todo-chatbot/`

## 🎯 Hackathon Deliverables

### Process Transparency

- ✅ **Specification**: Complete feature spec with 6 user stories
- ✅ **Planning**: Detailed 3,068-line technical plan
- ✅ **Tasks**: 104 dependency-ordered implementation tasks
- ✅ **PHRs**: 4+ prompt history records documenting development
- ✅ **Constitution**: v2.0.1 with Cohere API amendment

### Technical Implementation

- ✅ **Backend**: FastAPI + SQLModel + Cohere integration
- ✅ **MCP Tools**: 5 standardized tools with Cohere-compatible schemas
- ✅ **Agent**: Stateless design with conversation persistence
- ✅ **Frontend**: React/Next.js chat interface
- ✅ **Database**: PostgreSQL with proper migrations

### Demo Scenarios (for Judges)

1. **Multi-User Task Management**: Two accounts cannot see each other's tasks
2. **Natural Language CRUD**: Add, list, complete, delete, update via chat
3. **Stateless Architecture**: Server restart doesn't lose conversation context
4. **Error Handling**: Friendly messages for invalid operations
5. **Process Traceability**: Full development workflow visible in docs

## 🧠 Key Technical Decisions

### Why Cohere over OpenAI?

- **Cost/Performance**: Better pricing for tool-heavy workflows
- **Multilingual**: Strong support for future expansion
- **Tool Calling**: Excellent JSON schema tool calling support
- **Compatibility**: Can use OpenAI SDK interface

### Why Stateless Architecture?

- **Scalability**: Horizontal scaling without sticky sessions
- **Reliability**: Server restarts don't lose data
- **Simplicity**: No complex state management
- **Cloud-Native**: Serverless deployment ready

### Why MCP Tools?

- **Standardization**: Consistent tool interface
- **Separation**: Agent doesn't directly access database
- **Testability**: Tools independently testable
- **Reusability**: Tools can be used by multiple agents

## 🤝 Contributing

This is a hackathon project. For production use, consider:
- Adding comprehensive unit/integration tests
- Implementing rate limiting
- Adding caching layer (Redis)
- Setting up CI/CD pipeline
- Adding monitoring and observability
- Implementing data export features

## 📄 License

MIT License - See LICENSE file for details

## 🏆 Hackathon Team

- **Development**: AI-assisted via Claude Code
- **Architecture**: Spec-Driven Development (SDD)
- **AI Provider**: Cohere (command-a-03-2025)
- **Framework**: Agentic Dev Stack

---

**Built with** ❤️ **for Hackathon II Phase 3**

For questions or issues, check the `specs/` directory for detailed documentation.
