---
id: 1
title: Phase 3 Constitution Creation
stage: constitution
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: tooba
command: /sp.constitution
labels: ["constitution", "phase-3", "stateless", "mcp-tools", "openai-agents", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

Create a constitution for Hackathon II Phase 3: Todo AI Chatbot project.

Core principles:
- Follow Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement via Claude Code only. No manual coding allowed.
- Use only the specified tech stack: FastAPI (backend), OpenAI ChatKit (frontend), OpenAI Agents SDK (AI logic), Official MCP Python SDK (tools), SQLModel (ORM), Neon Serverless PostgreSQL (DB), Better Auth (authentication).
- All server components MUST be stateless: No in-memory state, persist everything (tasks, conversations, messages) to database.
- MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) must be exposed via Official MCP SDK server, stateless, and use SQLModel for DB ops.
- Agent must use MCP tools via client calls; chain tools if needed (e.g., list before delete if ambiguous).
- Chat endpoint (/api/{user_id}/chat) must be stateless, fetch/store history from DB, run agent, return response + tool_calls.
- Always confirm actions in friendly natural language (e.g., "Task added successfully: Buy groceries").
- Handle errors gracefully (e.g., "Task not found", 404/401 responses).
- Use Pydantic v2+, async endpoints where possible, proper HTTP status codes.
- Authentication: Use Better Auth sessions/JWT, validate user_id in every endpoint.
- No external dependencies beyond listed stack; prioritize scalability and hackathon judging criteria (process transparency, README with setup).
- All code generation must be iterative, review prompts/iterations.

Generate the full constitution.md in .specify/memory/ or appropriate folder.

## Response snapshot

Created comprehensive Phase 3 constitution (version 2.0.0) with 10 core principles:

1. **Spec-First Development** - Agentic Dev Stack workflow enforcement
2. **Agentic Development Workflow** - Four-phase process (Spec → Plan → Tasks → Implement)
3. **Stateless Architecture** - No in-memory state, fresh agent instantiation, DB persistence
4. **MCP Tool Integration** - Five required tools via Official MCP Python SDK
5. **AI Agent Integration** - OpenAI Agents SDK with tool orchestration
6. **Natural Language Interface** - Intent detection, entity extraction, friendly confirmations
7. **Security-by-Design** - Better Auth JWT validation, zero-trust authorization
8. **API-First Architecture** - RESTful FastAPI endpoints with proper HTTP semantics
9. **Separation of Concerns** - Clear boundaries (Frontend/Backend/MCP/Agent/Database)
10. **Traceability and Process Transparency** - PHRs, specs, plans, tasks, ADRs

Added comprehensive sections:
- Technology Stack Constraints (mandatory and prohibited)
- Development Workflow (5 phases with entry/exit conditions)
- Stateless Design Patterns (Chat endpoint flow, MCP tool call pattern)
- Error Handling Standards (user-facing, API, MCP tool errors)
- Validation and Compliance (pre/post-implementation checklists, ADR criteria)
- Governance (amendment process, compliance review, hackathon alignment)

Sync Impact Report:
- Version: 1.0.0 → 2.0.0 (MAJOR bump due to principle additions)
- Modified: 4 existing principles enhanced
- Added: 5 new principles (Stateless, MCP, Agent, NLP, Traceability)
- Templates: All aligned (plan-template, spec-template, tasks-template)

## Outcome

- ✅ Impact: Complete constitutional foundation for Phase 3 development with strict stateless, MCP, and agent integration requirements
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (2.0.0)
- 🔁 Next prompts:
  1. Use `/sp.specify` to create Phase 3 feature specifications
  2. Use `/sp.plan` with constitution checks for technical planning
  3. Create ADRs for stateless architecture and MCP tool design decisions
  4. Update README with Phase 3 architecture overview
- 🧠 Reflection: Constitution provides comprehensive guidance for stateless AI chatbot development, ensures hackathon evaluation criteria are met (process transparency, reproducibility), and establishes clear constraints to prevent scope creep. The 10 principles create a strong foundation for Phase 3 implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None - user provided comprehensive and detailed requirements
- Graders run and results (PASS/FAIL): Manual review (PASS - all user requirements incorporated)
- Prompt variant (if applicable): Standard constitution creation with Phase 3 hackathon focus
- Next experiment (smallest change to try): Consider adding explicit metrics for hackathon scoring (e.g., PHR completeness thresholds, documentation coverage requirements)
