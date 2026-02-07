---
id: 2
title: Cohere API Migration Amendment
stage: constitution
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 004-ai-todo-chatbot
user: tooba
command: /sp.constitution
labels: ["constitution", "amendment", "cohere-api", "llm-provider", "phase-3"]
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

Update the existing constitution.md for Hackathon II Phase 3: Todo AI Chatbot to switch from OpenAI to Cohere API.

Key changes:
- AI Provider: Cohere (instead of OpenAI)
- API Key Environment Variable: COHERE_API_KEY (instead of OPENAI_API_KEY)
- Models: Use Cohere's Command family models optimized for tool use and agents, e.g.:
  - Primary: command-a-03-2025 (or latest Command A variant for strong agentic/tool calling)
  - Alternative: command-r-plus-08-2024 (for complex multi-step reasoning and long context)
- Integration Method: Use Cohere via OpenAI-compatible endpoint for minimal code changes:
  - Base URL: https://api.cohere.ai/compatibility/v1
  - Client: from openai import OpenAI; client = OpenAI(api_key=COHERE_API_KEY, base_url="https://api.cohere.ai/compatibility/v1")
  - This allows keeping OpenAI Agents SDK (if compatible) or falling back to Cohere native SDK for tool use.
- Tool Use: Cohere fully supports tool calling (similar to OpenAI function calling) — ensure MCP tools are defined in Cohere-compatible JSON schema format.
- Reasons for switch: Better cost/performance for tool-heavy agent workflows, strong multilingual support (useful for natural language todos), and reliable multi-step reasoning.
- No other changes to stack: Still use OpenAI Agents SDK where possible via compatibility layer, MCP Python SDK for tools, FastAPI, SQLModel, Neon DB, ChatKit frontend, Better Auth.
- All other principles remain: Stateless server, no manual coding, MCP tools exposure, agent chaining, confirmations, error handling, hackathon deliverables.

Regenerate or append to constitution.md with these updates clearly marked (e.g., in a "Updates" section with date). Keep the document immutable otherwise — only this AI provider change is approved.

Output the full updated constitution.md content.

## Response snapshot

Successfully updated Phase 3 constitution from version 2.0.0 → 2.0.1 (PATCH) with Cohere API migration.

**Changes Made**:

1. **Principle 3 - Stateless Architecture** (line 72):
   - Updated: "OpenAI Agent" → "AI Agent (Cohere-powered)"

2. **Principle 5 - AI Agent Integration** (lines 103-124):
   - **Complete rewrite** with Cohere-specific requirements:
     - LLM Provider: Cohere API only
     - Primary Model: `command-a-03-2025`
     - Alternative Model: `command-r-plus-08-2024`
     - API Configuration: OpenAI SDK with Cohere compatibility endpoint
     - Base URL: `https://api.cohere.ai/compatibility/v1`
     - Environment Variable: `COHERE_API_KEY`
   - Added rationale: cost/performance, multilingual NLP, multi-step reasoning, tool calling

3. **Principle 4 - MCP Tool Integration** (line 93):
   - Added: "Tool Schema Format: Cohere-compatible JSON schema"

4. **Principle 7 - Security-by-Design** (line 161):
   - Updated: Secrets include `COHERE_API_KEY`

5. **Principle 9 - Separation of Concerns** (lines 212, 219):
   - Updated Backend: "Agent orchestration (Cohere API integration)"
   - Updated AI Agent: "Cohere-powered via OpenAI SDK compatibility"

6. **Technology Stack Constraints** (lines 265-271):
   - **Complete rewrite** of AI Integration section:
     - LLM Provider: Cohere API only
     - Primary/Alternative models specified
     - Integration method documented
     - API Key environment variable
   - Prohibited: Alternative LLM providers (OpenAI native, Anthropic direct)

7. **Development Workflow - Phase 2 Planning** (line 336):
   - Added: "Agent behavior design (Cohere-specific tool calling patterns)"

8. **Development Workflow - Constitution Check** (line 343, 403):
   - Updated: "Cohere API, not OpenAI"
   - Updated: "COHERE_API_KEY in environment"

9. **Stateless Design Patterns - Chat Endpoint** (lines 435-442):
   - Added code example showing Cohere client initialization via OpenAI SDK compatibility

10. **Stateless Design Patterns - MCP Tool Call** (line 465):
    - Updated: "Cohere-compatible JSON format"

11. **Validation Checklists** (lines 567, 590):
    - Added: Check for Cohere API (not OpenAI)
    - Added: COHERE_API_KEY properly configured

12. **ADR Decision Criteria** (line 600):
    - Added example: "Choice of Cohere over OpenAI (LLM provider selection)"

13. **NEW SECTION - Amendment History** (lines 610-641):
    - Documented full migration details
    - Rationale: cost/performance, multilingual, reasoning, tool calling
    - Impact assessment: minimal code changes, compatible schemas
    - Follow-up actions: ADR, spec updates, testing

**Version Bump**: 2.0.0 → 2.0.1 (PATCH)
- **Rationale**: Implementation detail clarification, not architectural change
- Core principles unchanged (stateless, MCP, security, workflow)
- Only LLM provider implementation detail updated

**Sync Impact Report** (updated in HTML comment):
- Modified principles: AI Agent Integration, Stateless Architecture, Technology Stack
- Amendment type: PATCH
- Reason: Better cost/performance for tool-heavy workflows
- Added: Amendment History section
- Follow-up TODOs: ADR creation, spec updates, MCP schema verification

## Outcome

- ✅ Impact: Constitution updated with Cohere API integration while preserving all architectural principles
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md (2.0.1)
- 🔁 Next prompts:
  1. Create ADR documenting OpenAI → Cohere migration rationale
  2. Update specs/004-ai-todo-chatbot/spec.md dependencies (OpenAI → Cohere)
  3. Verify MCP tool JSON schemas are Cohere-compatible
  4. Run `/sp.plan` with Cohere-specific technical details
  5. Update README with Cohere API setup instructions
- 🧠 Reflection: Amendment successfully completed with minimal architectural disruption. OpenAI SDK compatibility endpoint allows reusing patterns while gaining Cohere's cost/performance advantages. All other principles (stateless, MCP, FastAPI, SQLModel) remain unchanged. Ready for planning phase with Cohere integration.

## Evaluation notes (flywheel)

- Failure modes observed: None - clear migration path provided by user
- Graders run and results (PASS/FAIL): Manual review (PASS - all requirements incorporated)
- Prompt variant (if applicable): Constitutional amendment with specific technology substitution
- Next experiment (smallest change to try): Consider adding performance benchmarks comparing OpenAI vs Cohere for tool-calling tasks in future ADR
