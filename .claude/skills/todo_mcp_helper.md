---
name: todo_mcp_helper
description: Automatically helps with Todo AI Chatbot Phase 3 features (add_task, list_tasks, complete_task, etc.)
when_to_use: Use this skill whenever the user mentions Phase 3, MCP tools, OpenAI Agents SDK, FastAPI chat endpoint, or natural language todo commands.
invoke_directly: true
---

# Todo MCP Helper - Phase 3 AI Chatbot Assistant

## Overview

This skill provides intelligent assistance for Hackathon II Phase 3 Todo AI Chatbot development. It helps with:

- MCP Server tools specification and implementation
- OpenAI Agents SDK integration patterns
- FastAPI stateless chat endpoint design
- Natural language command mapping to MCP tool calls
- Agent behavior and system prompt design

## Architecture Context

**Phase 3 Stack:**
- **Frontend:** OpenAI ChatKit (React-based)
- **Backend:** FastAPI (stateless)
- **AI Logic:** OpenAI Agents SDK
- **Tool Layer:** MCP (Model Context Protocol) Server
- **Database:** PostgreSQL
- **Key Principle:** Stateless - all state persisted in DB, no server-side memory

## When to Use This Skill

Invoke `/todo_mcp_helper` when you need help with:

1. **MCP Tool Development**
   - Defining tool schemas (add_task, list_tasks, complete_task, delete_task, update_task)
   - Tool parameter validation
   - Error handling patterns

2. **Agent Behavior Design**
   - System prompts for OpenAI Agents SDK
   - Intent detection and routing
   - Multi-turn conversation handling (stateless)

3. **API Endpoint Design**
   - FastAPI chat endpoint (`POST /chat`)
   - Request/response schemas
   - Agent execution lifecycle

4. **Natural Language Processing**
   - Mapping user commands to tool calls
   - Handling ambiguous references (task by name vs ID)
   - Confirmation and error messaging

## Step-by-Step Usage

### 1. Quick Reference
```bash
/todo_mcp_helper
```
Displays available MCP tools, agent patterns, and common Phase 3 workflows.

### 2. Tool-Specific Help
```bash
/todo_mcp_helper What are the parameters for add_task?
```

### 3. Agent Behavior Guidance
```bash
/todo_mcp_helper How should the agent handle "mark task 3 complete"?
```

### 4. Implementation Assistance
```bash
/todo_mcp_helper Generate the stateless chat endpoint
```

## Common Phase 3 Tasks

### Task 1: Implement MCP Tool Specification

**User Request:**
> "Help me implement add_task tool"

**Assistant Actions:**
1. Reference MCP tool schema from specs/4-ai-agent-behavior/mcp-tools.spec.md
2. Provide Python implementation template:
   ```python
   @server.call_tool()
   async def add_task(
       user_id: int,
       title: str,
       description: str | None = None,
       due_date: str | None = None,
       priority: Literal["low", "medium", "high"] | None = "medium"
   ) -> dict:
       # Database insert logic
       # Return: {"task_id": int, "title": str, "status": "success"}
   ```
3. Suggest validation rules (title max length, date format)
4. Link to database schema in specs/1-todo-backend/

### Task 2: Generate Stateless Chat Endpoint

**User Request:**
> "Generate the stateless chat endpoint"

**Assistant Actions:**
1. Provide FastAPI endpoint structure:
   ```python
   @app.post("/chat")
   async def chat(request: ChatRequest) -> ChatResponse:
       # 1. Fetch conversation history from DB
       # 2. Instantiate OpenAI Agent with MCP tools
       # 3. Execute agent with user message + history
       # 4. Save new messages to DB
       # 5. Return assistant response
   ```
2. Show request/response schemas
3. Highlight stateless design: no in-memory state, fresh agent per request
4. Reference specs/4-ai-agent-behavior/api.spec.md

### Task 3: Agent Behavior for Task Completion

**User Request:**
> "Suggest agent behavior for 'mark task 3 complete'"

**Assistant Actions:**
1. Show intent detection pattern:
   - Keywords: "mark", "complete", "done", "finish"
   - Extract task reference: ID (3) or name
2. Tool orchestration:
   - If ID provided: call `complete_task(task_id=3)`
   - If name provided: call `list_tasks()` → fuzzy match → `complete_task(task_id=resolved_id)`
3. Response template:
   ```
   "✓ Marked task #3 'Buy groceries' as complete!"
   ```
4. Error handling:
   - Task not found: "I couldn't find task #3. Try /list to see your tasks."
   - Already completed: "Task #3 is already complete."

### Task 4: Remind MCP Tools Specification

**User Request:**
> "Remind me of MCP tools specification"

**Assistant Actions:**
1. List all Phase 3 MCP tools:
   - `create_task(user_id, title, description?, due_date?, priority?)`
   - `list_tasks(user_id, status?, limit?, offset?)`
   - `update_task(user_id, task_id, title?, description?, status?, due_date?, priority?)`
   - `delete_task(user_id, task_id)`
   - `get_task(user_id, task_id)` [optional]
2. Show common patterns:
   - All tools require `user_id` (from JWT token)
   - Optional parameters for filtering/partial updates
   - Consistent error responses
3. Reference full spec: `specs/4-ai-agent-behavior/mcp-tools.spec.md`

## Error Handling and Best Practices

### MCP Tool Errors
- **Task Not Found:** Return `{"error": "not_found", "message": "Task ID {id} does not exist"}`
- **Invalid Input:** Return `{"error": "validation_error", "details": {...}}`
- **Database Error:** Return `{"error": "internal_error", "message": "Could not complete operation"}`

### Agent Behavior Best Practices
1. **Always confirm destructive actions:** "Are you sure you want to delete all completed tasks? (y/n)"
2. **Provide context in responses:** "✓ Added task #7: 'Buy groceries'" (not just "Done")
3. **Handle ambiguity gracefully:** "I found 2 tasks with 'meeting'. Which one? [1] Meeting with John [2] Team meeting"
4. **Fail informatively:** "I couldn't complete that task because it doesn't exist. Try /list to see your tasks."

### Stateless Design Patterns
- **No session storage:** Fetch conversation from DB on every request
- **Idempotent operations:** Same request → same result (use task IDs, not positions)
- **Fresh agent per request:** Instantiate OpenAI Agent with tools each time

## Chaining with Spec-Kit Plus Commands

### Workflow 1: New Feature Development
```bash
# Step 1: Create specification
/sp.specify Add priority management to todo tasks

# Step 2: Generate plan (use /todo_mcp_helper for MCP tool guidance)
/sp.plan

# Step 3: Generate tasks
/sp.tasks

# Step 4: Implement (use /todo_mcp_helper during implementation)
/sp.implement
```

### Workflow 2: Agent Behavior Design
```bash
# Step 1: Design agent behavior specification
/todo_mcp_helper Create agent.spec.md for todo chatbot

# Step 2: Review MCP tool contracts
/todo_mcp_helper Show all MCP tools and parameters

# Step 3: Implement system prompt
# (Assistant generates system prompt with tool descriptions)

# Step 4: Test with example conversations
/todo_mcp_helper Test: "add buy milk" → which tool?
```

### Workflow 3: API Endpoint Creation
```bash
# Step 1: Design API specification
/todo_mcp_helper Design POST /chat endpoint

# Step 2: Generate FastAPI code
/todo_mcp_helper Implement stateless chat endpoint

# Step 3: Add to plan
/sp.plan (updates with new endpoint)

# Step 4: Commit work
/sp.git.commit_pr
```

## Quick Reference Tables

### MCP Tools Summary

| Tool Name | Purpose | Required Params | Optional Params |
|-----------|---------|-----------------|-----------------|
| `create_task` | Add new task | user_id, title | description, due_date, priority |
| `list_tasks` | Get tasks | user_id | status, limit, offset |
| `update_task` | Modify task | user_id, task_id | title, description, status, due_date, priority |
| `delete_task` | Remove task | user_id, task_id | - |

### NLP Intent Mapping

| User Intent | Keywords | MCP Tool | Notes |
|-------------|----------|----------|-------|
| CREATE | add, create, new, remind | `create_task` | Extract title from command |
| READ | show, list, what, display | `list_tasks` | Respect status filter |
| UPDATE | change, update, modify, edit | `update_task` | Resolve task by ID or name |
| DELETE | delete, remove, clear | `delete_task` | Always confirm first |
| COMPLETE | done, finish, complete, mark | `update_task(status='completed')` | Shortcut for status update |

### Agent System Prompt Template

```markdown
You are a helpful todo assistant. You can:
- Add tasks: "add [task]" or "remind me to [task]"
- List tasks: "show my tasks" or "what do I need to do?"
- Complete tasks: "mark task [id/name] as done"
- Update tasks: "change task [id/name] to [new title]"
- Delete tasks: "delete task [id/name]"

You have access to these MCP tools:
- create_task(user_id, title, description?, due_date?, priority?)
- list_tasks(user_id, status?, limit?, offset?)
- update_task(user_id, task_id, title?, description?, status?, due_date?, priority?)
- delete_task(user_id, task_id)

Important:
1. If user references task by name, call list_tasks first to find the task_id
2. Always confirm before deleting tasks
3. Provide friendly confirmations after successful operations
4. Handle errors gracefully with helpful suggestions
```

## Integration Points

### With Spec-Kit Plus
- **Before `/sp.plan`:** Use `/todo_mcp_helper` to clarify MCP tool requirements
- **During `/sp.implement`:** Use `/todo_mcp_helper` for code templates and patterns
- **After `/sp.implement`:** Use `/todo_mcp_helper` to validate agent behavior

### With Phase 1-2 Features
- **JWT Auth (Phase 2):** Extract `user_id` from JWT token for all MCP tool calls
- **Todo Backend (Phase 1):** MCP tools call existing CRUD endpoints or DB directly
- **Frontend (Phase 3):** ChatKit sends messages to `/chat`, displays responses

## Troubleshooting

### Issue: Agent not calling MCP tools
**Solution:** Check system prompt includes tool descriptions and agent has `tools=mcp_tools` parameter

### Issue: Stateless context lost between messages
**Solution:** Verify chat endpoint fetches full conversation history from DB before agent execution

### Issue: Ambiguous task references
**Solution:** Implement name resolution pattern: list_tasks → fuzzy match → show options if multiple matches

### Issue: MCP tool errors not handled
**Solution:** Wrap tool calls in try/except, return structured error responses to agent

## Output Format

When invoked, this skill will:
1. Analyze the user's request
2. Identify relevant Phase 3 components (MCP tools, agent behavior, API design)
3. Provide code templates, specifications, or guidance
4. Suggest next steps in Spec-Kit Plus workflow
5. Reference existing specs and design documents

## Notes

- All MCP tools must be stateless and idempotent
- Agent receives fresh conversation context on every request
- User authentication handled via JWT (user_id extracted from token)
- All specifications stored in `specs/4-ai-agent-behavior/`
- Follow Spec-Driven Development (SDD) workflow for all changes

---

**Version:** 1.0
**Last Updated:** 2026-02-07
**Maintainer:** Phase 3 Development Team
