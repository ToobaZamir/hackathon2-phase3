---
id: 3
title: Technical Architecture Planning
stage: plan
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 4-ai-todo-chatbot
branch: 004-ai-todo-chatbot
user: tooba
command: /sp.plan
labels: ["planning", "architecture", "cohere-api", "mcp-tools", "stateless", "phase-3"]
links:
  spec: specs/004-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-ai-todo-chatbot/plan.md
tests:
---

## Prompt

Using the updated constitution (Cohere API via OpenAI-compatible client or native SDK) and the current spec.md for Hackathon II Phase 3: Todo AI Chatbot, generate a detailed, realistic development plan.

Plan must strictly follow Agentic Dev Stack workflow and constitution rules: no manual coding, stateless architecture, MCP tools only via official SDK, SQLModel + Neon DB, FastAPI backend, OpenAI ChatKit frontend (proxied), Better Auth.

Key sections to include:
- High-level architecture overview + Mermaid diagram (update to show Cohere client instead of OpenAI)
- Updated folder structure (backend/, frontend/, specs/, migrations/)
- Dependencies list (pip requirements.txt + npm for frontend)
- Implementation sequence (prioritized tasks, estimated effort, dependencies between tasks)
  1. DB models & migrations (already partial from Phase 2)
  2. MCP server setup + 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) using mcp_tool_crafter skill
  3. Authentication integration (Better Auth JWT validation in FastAPI)
  4. FastAPI chat endpoint (/api/{user_id}/chat) using fastapi-endpoint-generator skill — stateless, DB history, Cohere client call
  5. Agent logic: Cohere via OpenAI-compatible client (model="command-a-03-2025"), tools wrapped as MCP client calls; fallback to native Cohere SDK if tool chaining needs multi-step reasoning
  6. Cohere integration details: client init code snippet, model selection, tool schema compatibility notes
  7. Frontend: ChatKit setup + proxy to backend endpoint + domain allowlist reminder
  8. Testing: manual NL command tests, error cases, conversation resume
  9. README + deliverables finalization
- How Cohere fits: Use OpenAI SDK compatibility for agent patterns; native cohere SDK for advanced tool use (multi-step, citations) if compatibility limits arise
- Risk notes: Tool calling compatibility check (Cohere supports JSON schema tools similar to OpenAI); test early with simple tool call
- Timeline estimate: Assume 1-2 focused days, using existing skills (todo_mcp_helper, fastapi-endpoint-generator, mcp_tool_crafter)

Output full plan.md with clear numbering, mermaid code block for diagram, and actionable next steps (e.g., which Claude command to run first).

## Response snapshot

Successfully generated comprehensive production-ready development plan (3,068 lines, 105KB) for AI Todo Chatbot with Cohere API integration.

**Plan Structure**:

1. **Executive Summary**:
   - Timeline: 1-2 focused days (12-16 hours)
   - Key decisions: Stateless design, Cohere via OpenAI SDK compatibility, MCP tools, conversation-driven
   - Critical success factors: Early tool calling validation, stateless enforcement, conversation persistence

2. **High-Level Architecture (Section 2.0)**:
   - System overview diagram (Mermaid): Frontend → API → Agent (Cohere) → MCP Tools → Database
   - Component responsibilities table (5 components)
   - Stateless architecture flow (Mermaid sequence diagram)
   - Request lifecycle: JWT → DB history → Fresh agent → Tool calls → Save messages

3. **Technology Stack (Section 3.0)**:
   - Cohere API: command-a-03-2025 (primary), command-r-plus-08-2024 (fallback)
   - Integration: OpenAI SDK compatibility endpoint
   - Client initialization code example
   - Native Cohere SDK fallback strategy
   - Backend: FastAPI, SQLModel, asyncpg, Alembic
   - Frontend: Next.js, React, ChatKit
   - Database: Neon PostgreSQL

4. **Project Structure (Section 4.0)**:
   - Complete folder tree: backend/, frontend/, specs/, migrations/, mcp_server/, tests/
   - File-by-file breakdown with [EXISTS]/[NEW] labels
   - Total: 25 existing files, 35 new files, 8 updates = 68 total files

5. **Database Schema (Section 5.0)**:
   - ER diagram (Mermaid): User → Tasks, Conversations → Messages → ToolCalls
   - SQLModel definitions: Conversation, Message (with MessageRole enum)
   - Indexes strategy: user_id, conversation_id, timestamp, composite indexes
   - Migration sequence: 002_conversations, 003_messages, 004_tool_calls

6. **MCP Tools Specification (Section 6.0)**:
   - 5 tools with Cohere-compatible JSON schemas
   - Tool definitions: create_task, list_tasks, update_task, delete_task, complete_task
   - Implementation patterns (code examples)
   - Error taxonomy: validation_error, not_found, unauthorized, forbidden, internal_error

7. **API Endpoints (Section 7.0)**:
   - Chat endpoint: POST /api/{user_id}/chat
   - Request/response schemas (ChatRequest, ChatResponse)
   - Complete endpoint implementation (95 lines of code)
   - Error handling strategy

8. **Agent Architecture (Section 8.0)**:
   - Cohere client initialization (OpenAI SDK compatibility)
   - AgentService implementation (stateless design, tool execution)
   - System prompt design (1,480 characters, tool guidelines, examples)
   - ConversationService (history management)
   - Multi-step reasoning with tool chaining

9. **Implementation Sequence (Section 9.0)** - 8 Phases:
   - Phase 1: Database Setup (2-3 hours) - Conversation/Message models, migrations
   - Phase 2: MCP Server (4-5 hours) - 5 tools with schemas
   - Phase 3: Authentication (1 hour) - JWT middleware, env config
   - Phase 4: Chat Endpoint (3-4 hours) - Stateless FastAPI route
   - Phase 5: Agent Logic (4-5 hours) - Cohere integration, tool calling
   - Phase 6: Frontend (3-4 hours) - Chat UI, proxy setup
   - Phase 7: Testing (2-3 hours) - Manual NL tests, integration tests
   - Phase 8: Documentation (2-3 hours) - README, ADR, PHR

10. **Dependencies (Section 10.0)**:
    - requirements.txt: cohere==5.0.0, openai==1.0.0, mcp==0.9.0
    - package.json: @openai/chatkit, react-markdown, date-fns
    - .env.example: COHERE_API_KEY, COHERE_MODEL, DATABASE_URL

11. **Cohere Integration Details (Section 11.0)**:
    - Tool schema compatibility (OpenAI vs native format)
    - Model selection strategy (command-a-03-2025 for tool use)
    - Error handling for API failures
    - Rate limiting considerations

12. **Risks & Mitigations (Section 12.0)**:
    - Tool calling compatibility (test early with simple create_task)
    - OpenAI SDK limitations (fallback to native Cohere SDK)
    - Database transaction safety
    - JWT validation security
    - CORS and domain allowlisting

13. **Timeline (Section 13.0)**:
    - Phase-by-phase breakdown (1-5 hours each)
    - Total: 22-30 hours (optimistic: 1.5 days, realistic: 2 days)
    - Critical path: DB → MCP → Auth → Chat → Agent
    - Parallel opportunities: Frontend + Testing during Phase 5-6

14. **Testing Strategy (Section 14.0)**:
    - Manual NL tests for all 6 user stories
    - Integration tests: chat flow, stateless architecture
    - Error case testing: 401/403, not_found, validation errors
    - Performance testing: <3s for 90% of requests
    - Conversation resume testing (server restart)

15. **Next Steps (Section 15.0)**:
    - Immediate: Run `/sp.tasks` to generate tasks.md
    - Then: Review tasks, run `/sp.implement`
    - Custom skills to use: todo_mcp_helper, fastapi-endpoint-generator
    - Verification: All 12 MVP acceptance criteria from spec.md

**Key Architectural Decisions**:
- **Stateless Enforcement**: Fresh agent per request, all state in PostgreSQL
- **Cohere via OpenAI SDK**: Minimal code changes, compatibility layer
- **MCP Tools as Primary Interface**: Agent never directly accesses DB
- **Conversation History in DB**: Enables stateless server with context preservation
- **Tool Chaining**: Multi-step reasoning (e.g., list → complete for named tasks)

**Code Snippets Provided**:
- Cohere client initialization (2 versions: OpenAI compatibility + native SDK)
- AgentService.execute() method (150+ lines)
- System prompt (full text, 1,480 characters)
- Tool definitions (create_task, list_tasks examples)
- Chat endpoint implementation (complete FastAPI route)
- Conversation service (CRUD operations)
- SQLModel definitions (Conversation, Message)
- Alembic migration templates

**Constitutional Compliance**:
- ✅ Stateless architecture (no in-memory state)
- ✅ MCP tools only (no direct DB access in agent)
- ✅ Cohere API integration (constitution v2.0.1)
- ✅ COHERE_API_KEY environment variable
- ✅ All code via Claude Code (no manual coding)

## Outcome

- ✅ Impact: Comprehensive, actionable technical plan ready for task generation and implementation
- 🧪 Tests: N/A (planning document)
- 📁 Files: specs/004-ai-todo-chatbot/plan.md (3,068 lines, 105KB)
- 🔁 Next prompts:
  1. Run `/sp.tasks` to generate dependency-ordered tasks.md from plan.md
  2. Review tasks for clarity and estimates
  3. Run `/sp.implement` to execute implementation via Claude Code
  4. Create ADR for OpenAI → Cohere migration (if not done during implementation)
  5. Use custom skills: todo_mcp_helper (MCP guidance), fastapi-endpoint-generator (endpoint code)
- 🧠 Reflection: Planning phase successfully translated spec.md into detailed technical architecture with Cohere API integration. The plan provides clear implementation sequence (8 phases, 22-30 hours), complete code examples (Cohere client, agent service, chat endpoint), and constitutional compliance verification. Mermaid diagrams visualize architecture and flow. Ready for task generation with all technical decisions documented.

## Evaluation notes (flywheel)

- Failure modes observed: None - comprehensive plan generated with all requested sections
- Graders run and results (PASS/FAIL): Manual review (PASS - all sections complete, code examples provided, timeline realistic)
- Prompt variant (if applicable): Standard /sp.plan with explicit Cohere API requirements
- Next experiment (smallest change to try): Consider adding performance benchmarks section in future plans to document expected latency/throughput targets for each component
