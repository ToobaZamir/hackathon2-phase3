---
description: "Dependency-ordered task list for AI Todo Chatbot implementation"
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/004-ai-todo-chatbot/`
**Prerequisites**: plan.md (Phase 3 architecture), spec.md (6 user stories P1-P3)

**Tests**: Tests are NOT included per spec requirements. Testing will be manual validation of natural language commands.

**Organization**: Tasks are grouped by implementation phase following the plan's 8-phase structure, then mapped to user stories where applicable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/mcp_server/`, `backend/tests/`
- **Frontend**: `frontend-todo-app/src/`
- **Specs**: `specs/004-ai-todo-chatbot/`
- **Migrations**: `backend/alembic/versions/`

---

## Phase 1: Database Setup (Conversation & Message Persistence)

**Purpose**: Extend database schema to support stateless conversation storage

**Goal**: Enable conversation history persistence for stateless agent architecture

- [ ] T001 [P] Create Conversation SQLModel in backend/src/models/conversation.py
- [ ] T002 [P] Create Message SQLModel with MessageRole enum in backend/src/models/message.py
- [ ] T003 Generate Alembic migration 002_add_conversations_table.py in backend/alembic/versions/
- [ ] T004 Generate Alembic migration 003_add_messages_table.py in backend/alembic/versions/
- [ ] T005 Run migrations with `alembic upgrade head` and verify tables in Neon DB
- [ ] T006 Create ConversationService with CRUD operations in backend/src/services/conversation_service.py

**Checkpoint**: Database schema supports conversations and messages - ready for MCP tools

---

## Phase 2: MCP Server Implementation (Tool Layer)

**Purpose**: Implement 5 MCP tools with Cohere-compatible JSON schemas

**Goal**: Provide standardized tool interface between AI agent and database operations

- [ ] T007 Create MCP server directory structure: backend/mcp_server/tools/ and backend/mcp_server/schemas/
- [ ] T008 Define Cohere-compatible tool schemas in backend/mcp_server/schemas/tool_definitions.py
- [ ] T009 [P] [US1] Implement create_task tool in backend/mcp_server/tools/create_task.py
- [ ] T010 [P] [US2] Implement list_tasks tool with status filter in backend/mcp_server/tools/list_tasks.py
- [ ] T011 [P] [US3] Implement complete_task tool in backend/mcp_server/tools/complete_task.py
- [ ] T012 [P] [US4] Implement delete_task tool in backend/mcp_server/tools/delete_task.py
- [ ] T013 [P] [US5] Implement update_task tool in backend/mcp_server/tools/update_task.py
- [ ] T014 Create __init__.py with tool exports in backend/mcp_server/tools/__init__.py
- [ ] T015 Create MCP server initialization in backend/mcp_server/server.py

**Checkpoint**: All 5 MCP tools implemented with Cohere-compatible schemas - ready for agent integration

---

## Phase 3: Authentication & Configuration

**Purpose**: Configure Cohere API credentials and verify JWT validation

**Goal**: Ensure secure access to chat endpoint with Cohere API integration

- [ ] T016 [P] Update config to add COHERE_API_KEY and COHERE_MODEL in backend/src/core/config.py
- [ ] T017 [P] Create .env.example with all Phase 3 environment variables in backend/.env.example
- [ ] T018 Verify JWT middleware get_current_user() function in backend/src/core/auth.py

**Checkpoint**: Configuration ready - Cohere API key configured, JWT validation verified

---

## Phase 4: Chat Endpoint (Stateless FastAPI Route)

**Purpose**: Implement stateless chat endpoint with conversation persistence

**Goal**: Accept user messages, orchestrate agent execution, persist conversation history

**User Stories Served**: All stories (US1-US6) - shared infrastructure

- [ ] T019 [P] [US6] Create ChatRequest and ChatResponse schemas in backend/src/schemas/chat.py
- [ ] T020 [US6] Implement stateless chat endpoint POST /api/{user_id}/chat in backend/src/api/v1/chat.py
- [ ] T021 [US6] Register chat router in FastAPI app in backend/src/main.py
- [ ] T022 [US6] Add JWT validation and user_id authorization to chat endpoint
- [ ] T023 [US6] Implement conversation get/create logic using ConversationService
- [ ] T024 [US6] Implement conversation history fetching from database
- [ ] T025 [US6] Implement message persistence (user + assistant) after agent execution
- [ ] T026 [US6] Add error handling for 401/403/404/500 responses

**Checkpoint**: Chat endpoint functional (placeholder agent) - ready for Cohere agent integration

---

## Phase 5: Agent Logic (Cohere API Integration)

**Purpose**: Integrate Cohere API with OpenAI SDK compatibility for tool calling

**Goal**: Enable natural language understanding and MCP tool orchestration

**User Stories Served**: All stories (US1-US6) - AI agent interprets intents

- [ ] T027 Create system prompt with tool guidelines and examples in backend/src/agent/system_prompt.py
- [ ] T028 Create agent directory structure: backend/src/agent/__init__.py
- [ ] T029 Implement Cohere client wrapper (OpenAI SDK compatibility) in backend/src/agent/cohere_client.py
- [ ] T030 Implement AgentService with stateless design in backend/src/services/agent_service.py
- [ ] T031 Implement tool execution logic (_execute_tool method) in AgentService
- [ ] T032 Implement multi-step reasoning (tool chaining) in AgentService
- [ ] T033 Integrate AgentService into chat endpoint (replace placeholder)
- [ ] T034 Add tool call logging to message persistence

**Checkpoint**: Cohere agent fully integrated - can process NL commands and call MCP tools

---

## Phase 6: User Story 1 - Quick Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks by typing natural language commands like "Add buy groceries"

**Independent Test**: Send "Add buy groceries" to chat endpoint, verify task created in DB, confirm agent responds "✓ Added task #N: Buy groceries"

### Implementation for User Story 1

- [ ] T035 [US1] Verify create_task tool (T009) handles title extraction from natural language
- [ ] T036 [US1] Update system prompt to include task creation examples ("Add...", "Remind me to...", "Create task...")
- [ ] T037 [US1] Test agent intent detection for task creation commands
- [ ] T038 [US1] Add validation for empty/too-long task titles in create_task tool
- [ ] T039 [US1] Test error handling: "Add" without task title → agent asks "What would you like to add?"

**Checkpoint**: ✅ User Story 1 complete - Users can create tasks via natural language

---

## Phase 7: User Story 2 - Task Viewing and Status Filtering (Priority: P1)

**Goal**: Users can view tasks filtered by status (all/pending/completed) via "Show my tasks", "List pending tasks"

**Independent Test**: Create 3 pending and 2 completed tasks, send "Show pending tasks", verify only 3 tasks returned with friendly formatting

### Implementation for User Story 2

- [ ] T040 [US2] Verify list_tasks tool (T010) supports status parameter (all/pending/completed)
- [ ] T041 [US2] Update system prompt with task listing examples ("Show my tasks", "What do I need to do?")
- [ ] T042 [US2] Test agent intent detection for list commands with different phrasings
- [ ] T043 [US2] Implement friendly task list formatting in agent responses (bullets, IDs, titles)
- [ ] T044 [US2] Add empty state handling: No tasks → "You don't have any tasks yet. Would you like to add one?"
- [ ] T045 [US2] Test status filter inference: "What do I need to do?" → status="pending"

**Checkpoint**: ✅ User Story 2 complete - Users can view and filter tasks

---

## Phase 8: User Story 3 - Task Completion (Priority: P2)

**Goal**: Users can mark tasks complete by ID or name: "Complete task 3", "Mark buy groceries done"

**Independent Test**: Create task "buy groceries", send "Complete buy groceries", verify task status=completed, confirm agent response

### Implementation for User Story 3

- [ ] T046 [US3] Verify complete_task tool (T011) marks tasks as completed
- [ ] T047 [US3] Update system prompt with completion examples ("Complete task X", "Mark X done", "I finished X")
- [ ] T048 [US3] Implement tool chaining: name reference → list_tasks → complete_task with task_id
- [ ] T049 [US3] Test ambiguous name handling: multiple matches → agent lists options and asks clarification
- [ ] T050 [US3] Test error handling: "Complete task 999" → "I couldn't find task #999. Try 'show my tasks'."
- [ ] T051 [US3] Add celebratory confirmation messages: "✓ Marked task #N 'Title' as complete! Great job!"

**Checkpoint**: ✅ User Story 3 complete - Users can complete tasks by ID or name

---

## Phase 9: User Story 4 - Task Deletion (Priority: P3)

**Goal**: Users can delete tasks with confirmation: "Delete task 5" → confirmation prompt → "yes" → task deleted

**Independent Test**: Create task, send "Delete task N", verify agent asks confirmation, send "yes", verify task deleted from DB

### Implementation for User Story 4

- [ ] T052 [US4] Verify delete_task tool (T012) permanently removes tasks
- [ ] T053 [US4] Update system prompt with deletion examples and ALWAYS confirm before delete rule
- [ ] T054 [US4] Implement confirmation flow: First call lists task details, asks "Are you sure? Type 'yes' to confirm"
- [ ] T055 [US4] Implement confirmation detection in conversation context (remember pending deletion)
- [ ] T056 [US4] Test bulk deletion: "Delete all completed tasks" → list completed → ask confirmation
- [ ] T057 [US4] Test cancellation: "Delete task 5" → "Are you sure?" → "no" → "Okay, task not deleted"

**Checkpoint**: ✅ User Story 4 complete - Users can safely delete tasks with confirmation

---

## Phase 10: User Story 5 - Task Updates (Priority: P3)

**Goal**: Users can update task title/description: "Change task 1 to 'Buy organic milk'"

**Independent Test**: Create task "Buy milk", send "Update task N to 'Buy organic milk'", verify title changed, confirm agent response

### Implementation for User Story 5

- [ ] T058 [US5] Verify update_task tool (T013) updates title and description fields
- [ ] T059 [US5] Update system prompt with update examples ("Update task X to Y", "Change X to Y")
- [ ] T060 [US5] Implement tool chaining: name reference → list_tasks → update_task with task_id
- [ ] T061 [US5] Test description updates: "Add description to task 3: Get 2% milk from Whole Foods"
- [ ] T062 [US5] Test error handling: invalid task ID → friendly error message
- [ ] T063 [US5] Add confirmation messages: "✓ Updated task #N to 'New Title'"

**Checkpoint**: ✅ User Story 5 complete - Users can update task details

---

## Phase 11: User Story 6 - Conversation Continuity (Priority: P2)

**Goal**: Conversation history persists across sessions - users can resume after server restart

**Independent Test**: Create tasks in conversation, stop server, restart server, send new message with same conversation_id, verify agent has context

### Implementation for User Story 6

- [ ] T064 [US6] Verify conversation history fetching in chat endpoint (T024)
- [ ] T065 [US6] Test stateless architecture: Create conversation → restart server → resume conversation
- [ ] T066 [US6] Verify agent receives full history on each request
- [ ] T067 [US6] Test new conversation creation: No conversation_id → create new → return conversation_id
- [ ] T068 [US6] Test conversation_id persistence: Frontend stores conversation_id, passes on subsequent requests
- [ ] T069 [US6] Verify no in-memory state: Agent instantiated fresh every request

**Checkpoint**: ✅ User Story 6 complete - Conversations persist across server restarts (stateless architecture proven)

---

## Phase 12: Frontend Integration

**Purpose**: Build chat UI that proxies to backend chat endpoint

**Goal**: Provide user-friendly interface for conversational task management

- [ ] T070 [P] Create chat page component in frontend-todo-app/src/app/chat/page.tsx
- [ ] T071 [P] Create ChatInterface container component in frontend-todo-app/src/components/ChatInterface.tsx
- [ ] T072 [P] Create MessageList display component in frontend-todo-app/src/components/MessageList.tsx
- [ ] T073 [P] Create MessageInput text input component in frontend-todo-app/src/components/MessageInput.tsx
- [ ] T074 [P] Create chat TypeScript types in frontend-todo-app/src/types/chat.ts
- [ ] T075 Add sendChatMessage API function in frontend-todo-app/src/lib/api.ts
- [ ] T076 Implement state management: messages, conversationId, loading states
- [ ] T077 Implement JWT passing in Authorization header
- [ ] T078 Add error handling: 401 → redirect to login, 403 → show error, 500 → retry prompt
- [ ] T079 Implement conversation ID persistence (localStorage or session storage)
- [ ] T080 Add loading spinner during agent processing
- [ ] T081 Style chat UI with Tailwind CSS (message bubbles, timestamps, user/assistant differentiation)

**Checkpoint**: Frontend chat UI functional - users can interact with AI agent through web interface

---

## Phase 13: Manual Testing & Validation

**Purpose**: Comprehensive manual testing of all 6 user stories and acceptance criteria

**Goal**: Validate all 12 MVP acceptance criteria from spec.md

- [ ] T082 Test US1: "Add buy groceries" → verify task created → confirm friendly response
- [ ] T083 Test US2: "Show my tasks" and "List pending tasks" → verify filtering works
- [ ] T084 Test US3: "Complete task 3" and "Mark buy groceries done" → verify status updates
- [ ] T085 Test US4: "Delete task 5" → verify confirmation → "yes" → verify deletion
- [ ] T086 Test US5: "Update task 2 to 'Buy organic milk'" → verify title changes
- [ ] T087 Test US6: Create tasks → stop server → restart → resume conversation → verify context maintained
- [ ] T088 Test authentication: Invalid JWT → expect 401, wrong user_id → expect 403
- [ ] T089 Test error handling: "Complete task 999" → friendly error, "Add" alone → clarification request
- [ ] T090 Test ambiguous references: "Complete buy" when 2 tasks match → agent lists options
- [ ] T091 Test empty states: "Show my tasks" with no tasks → friendly empty message
- [ ] T092 Test conversation creation: No conversation_id → new conversation created → ID returned
- [ ] T093 Test tool chaining: "Complete buy groceries" → list_tasks → complete_task → success

**Checkpoint**: All 12 MVP acceptance criteria verified manually

---

## Phase 14: Documentation & Polish

**Purpose**: Complete project documentation for hackathon submission

**Goal**: Enable judges to understand architecture, setup, and evaluate process transparency

- [ ] T094 [P] Update README.md with Phase 3 architecture overview, Cohere setup, chat endpoint docs
- [ ] T095 [P] Update backend/.env.example with all required environment variables and descriptions
- [ ] T096 [P] Update backend/requirements.txt with cohere, openai, mcp packages
- [ ] T097 [P] Update frontend-todo-app/package.json with react-markdown, date-fns if used
- [ ] T098 Create ADR for OpenAI → Cohere migration decision in history/adr/
- [ ] T099 Add demo scenario instructions to README (5 judge demo scenarios from spec.md)
- [ ] T100 Add architecture diagram (Mermaid) to README or docs/
- [ ] T101 Verify all PHRs created for spec, plan, tasks phases
- [ ] T102 Add COHERE_API_KEY setup instructions to README
- [ ] T103 Add quickstart section: Clone → Install → Configure → Run → Test
- [ ] T104 Final verification: Run through all 5 demo scenarios for hackathon judges

**Checkpoint**: ✅ Documentation complete - project ready for hackathon submission and judging

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Database)**: No dependencies - can start immediately
- **Phase 2 (MCP Tools)**: Depends on Phase 1 (needs Task model from Phase 1/2, Conversation/Message models from T001-T002)
- **Phase 3 (Auth/Config)**: Can run in parallel with Phase 1-2
- **Phase 4 (Chat Endpoint)**: Depends on Phase 1 (ConversationService), Phase 3 (JWT middleware)
- **Phase 5 (Agent Logic)**: Depends on Phase 2 (MCP tools), Phase 4 (chat endpoint)
- **Phase 6-11 (User Stories)**: Depend on Phase 5 (agent must be integrated)
  - US1-US5 can proceed in parallel once Phase 5 complete (different tools/intents)
  - US6 can run in parallel with US1-US5 (tests architecture, not specific tool)
- **Phase 12 (Frontend)**: Can start after Phase 4 (chat endpoint exists), fully functional after Phase 5
- **Phase 13 (Testing)**: Depends on all user story phases (6-11) being complete
- **Phase 14 (Documentation)**: Depends on implementation complete (Phase 13)

### User Story Dependencies

All user stories (US1-US6) are **independently testable** once foundational phases (1-5) complete:

- **US1 (Task Creation)**: No dependencies on other stories - uses create_task tool only
- **US2 (Task Viewing)**: No dependencies on other stories - uses list_tasks tool only
- **US3 (Task Completion)**: Can work independently but enhanced by US2 (list for name-based completion)
- **US4 (Task Deletion)**: Can work independently but enhanced by US2 (list for confirmation display)
- **US5 (Task Updates)**: Can work independently but enhanced by US2 (list for name-based updates)
- **US6 (Conversation Continuity)**: Tests infrastructure, not dependent on specific tools

### Critical Path

1. Phase 1 (Database) → Phase 2 (MCP Tools) → Phase 5 (Agent) → US1 (MVP) → Testing → Documentation
2. Estimated time: 2-3 hours + 4-5 hours + 4-5 hours + 1-2 hours + 2 hours + 2 hours = **15-19 hours** (2 days)

### Parallel Opportunities

**Within Phases**:
- Phase 1: T001-T002 (models) can run in parallel
- Phase 2: T009-T013 (all 5 tools) can run in parallel after T008 (schemas)
- Phase 3: T016-T017 (config files) can run in parallel
- Phase 4: T019 (schemas) parallel with T020 (endpoint) after planning
- Phase 12: T070-T074 (all frontend components) can run in parallel

**Across Phases**:
- Phase 3 can run in parallel with Phase 1-2
- Phase 12 (Frontend) can start early, in parallel with Phase 5-11
- User Stories 1-6 (Phase 6-11) can be worked on in parallel by different developers after Phase 5

**Multi-Developer Strategy**:
1. All developers: Complete Phase 1-5 together (foundational)
2. Split work:
   - Developer A: US1 + US3 (task creation + completion)
   - Developer B: US2 + US4 (task viewing + deletion)
   - Developer C: US5 + US6 (task updates + conversation continuity)
   - Developer D: Frontend (Phase 12)
3. Converge: Testing + Documentation

---

## Parallel Example: Phase 2 (MCP Tools)

After T008 (tool schemas) complete, launch all tool implementations in parallel:

```bash
# Launch all 5 MCP tools simultaneously:
Task T009: "Implement create_task tool in backend/mcp_server/tools/create_task.py"
Task T010: "Implement list_tasks tool in backend/mcp_server/tools/list_tasks.py"
Task T011: "Implement complete_task tool in backend/mcp_server/tools/complete_task.py"
Task T012: "Implement delete_task tool in backend/mcp_server/tools/delete_task.py"
Task T013: "Implement update_task tool in backend/mcp_server/tools/update_task.py"
```

All tools use the same schema format, different DB operations, no dependencies between them.

---

## Implementation Strategy

### MVP First (User Story 1 Only - Fastest Path to Demo)

1. ✅ Phase 1: Database Setup (2-3 hours)
2. ✅ Phase 2: MCP Tools - **Only T009 (create_task)** (1 hour)
3. ✅ Phase 3: Auth/Config (1 hour)
4. ✅ Phase 4: Chat Endpoint (3-4 hours)
5. ✅ Phase 5: Agent Logic (4-5 hours)
6. ✅ Phase 6: User Story 1 Implementation (1-2 hours)
7. ✅ Phase 12: Basic Frontend (2-3 hours)
8. **STOP and VALIDATE**: Test "Add buy groceries" end-to-end
9. **DEMO READY** - Can show task creation via natural language

**Total MVP Time**: ~14-19 hours (1.5-2 days)

### Full Feature Delivery (All 6 User Stories)

1. Complete MVP (US1) per above
2. Add US2 (Task Viewing) - Implement T010 (list_tasks) + T040-T045 (2 hours)
3. Add US3 (Task Completion) - Implement T011 (complete_task) + T046-T051 (2 hours)
4. Add US4 (Task Deletion) - Implement T012 (delete_task) + T052-T057 (2 hours)
5. Add US5 (Task Updates) - Implement T013 (update_task) + T058-T063 (2 hours)
6. Validate US6 (Conversation Continuity) - Test stateless architecture T064-T069 (1 hour)
7. Complete Frontend Polish (Phase 12) - T075-T081 (2-3 hours)
8. Manual Testing (Phase 13) - All 12 acceptance criteria T082-T093 (2-3 hours)
9. Documentation (Phase 14) - T094-T104 (2-3 hours)

**Total Full Delivery Time**: MVP (14-19h) + Additional Features (13-16h) = **27-35 hours** (3-4 days)

### Incremental Delivery (Recommended)

1. **Day 1**: Phase 1-5 (Foundation) → **Agent can respond but limited tools**
2. **Day 1 EOD**: Phase 6 (US1) → **MVP Demo: Task creation works**
3. **Day 2 AM**: Phase 7-9 (US2-US4) → **Core CRUD complete**
4. **Day 2 PM**: Phase 10-11 (US5-US6) → **All features complete**
5. **Day 2 EOD**: Phase 12 (Frontend) → **UI functional**
6. **Day 3**: Phase 13-14 (Testing + Docs) → **Hackathon ready**

Each phase adds value without breaking previous functionality.

---

## Task Count Summary

- **Phase 1** (Database): 6 tasks
- **Phase 2** (MCP Tools): 9 tasks
- **Phase 3** (Auth/Config): 3 tasks
- **Phase 4** (Chat Endpoint): 8 tasks
- **Phase 5** (Agent Logic): 8 tasks
- **Phase 6** (US1 - Task Creation): 5 tasks
- **Phase 7** (US2 - Task Viewing): 6 tasks
- **Phase 8** (US3 - Task Completion): 6 tasks
- **Phase 9** (US4 - Task Deletion): 6 tasks
- **Phase 10** (US5 - Task Updates): 6 tasks
- **Phase 11** (US6 - Conversation Continuity): 6 tasks
- **Phase 12** (Frontend): 12 tasks
- **Phase 13** (Testing): 12 tasks
- **Phase 14** (Documentation): 11 tasks

**Total**: 104 tasks

**Parallelizable**: 25 tasks marked [P] (24% can run in parallel)

**MVP Subset** (US1 only): 45 tasks (Phases 1-6 + minimal Phase 12)

---

## Notes

- Each task includes exact file path for implementation
- [P] tasks can run in parallel (different files, no cross-dependencies)
- [USN] labels map tasks to specific user stories for traceability
- Tests are OPTIONAL - manual validation per spec.md acceptance criteria
- Commit after each logical task group (e.g., all Phase 2 tools together)
- Stop at any checkpoint to validate independently
- Frontend (Phase 12) can start early and run in parallel with backend phases
- Constitution v2.0.1 compliance: Stateless, Cohere API, MCP tools only, no manual coding
