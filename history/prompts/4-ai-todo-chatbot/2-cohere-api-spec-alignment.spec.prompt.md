---
id: 2
title: Cohere API Spec Alignment
stage: spec
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 4-ai-todo-chatbot
branch: 004-ai-todo-chatbot
user: tooba
command: /sp.specify
labels: ["specification", "cohere-api", "alignment", "constitution-sync", "phase-3"]
links:
  spec: specs/004-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-ai-todo-chatbot/spec.md
tests:
---

## Prompt

Update the existing spec.md for Hackathon II Phase 3: Todo AI Chatbot to align with the updated constitution (Cohere API instead of OpenAI).

Key changes needed:
- Replace all OpenAI API references with Cohere API
- Update AI provider details: Cohere via OpenAI-compatible endpoint
- Specify models: command-a-03-2025 (primary), command-r-plus-08-2024 (alternative)
- Update environment variable: COHERE_API_KEY (instead of OPENAI_API_KEY)
- Add client initialization pattern: `client = OpenAI(api_key=os.getenv("COHERE_API_KEY"), base_url="https://api.cohere.ai/compatibility/v1")`
- Update constitution reference from v2.0.0 to v2.0.1
- Keep all user stories, functional requirements, MCP tools, and acceptance criteria unchanged (technology-agnostic)

Regenerate or update spec.md with these changes clearly marked (e.g., add an "Updates" section at the top with date and summary: "Updated on [date] to use Cohere API per constitution revision").

## Response snapshot

Successfully updated spec.md to align with Cohere API migration per constitution v2.0.1.

**Changes Made**:

1. **Added Updates Section** (after line 6):
   - Documented 2026-02-07 Cohere API migration
   - Listed key changes: LLM provider, models, integration method, environment variable
   - Clarified that functional requirements remain unchanged (technology-agnostic)

2. **Edge Cases** (line 128-129):
   - Updated: "OpenAI API is rate-limited" → "Cohere API is rate-limited"

3. **FR-002 - Core Conversation & Agent** (line 137):
   - Updated: "OpenAI Agents SDK" → "Cohere API via OpenAI-compatible client"

4. **Technology Stack Constraints** (line 209):
   - Updated: "OpenAI Agents SDK (AI logic)" → "Cohere API with OpenAI SDK compatibility (AI logic)"
   - Added: AI Models section specifying command-a-03-2025 (primary) and command-r-plus-08-2024 (alternative)
   - Added: API Integration pattern with code example

5. **Assumptions** (line 222):
   - Updated: "OpenAI API Availability" → "Cohere API Availability"
   - Added note: Cohere supports multilingual capabilities for future phases

6. **External Systems Dependencies** (line 229):
   - Complete rewrite of OpenAI API dependency → Cohere API dependency
   - Added: Base URL, Environment Variable, Models details

7. **Development Dependencies** (line 243):
   - Updated: Constitution v2.0.0 → v2.0.1

8. **Notes for Implementation** (line 332):
   - Added: MCP Tool Contracts must use Cohere-compatible format
   - Added: Agent System Prompt optimized for Cohere's command models
   - Added: Agent Client Initialization code example
   - Updated: Constitutional compliance references v2.0.1

9. **Ready for Planning** (line 337):
   - Updated: "ready for /sp.plan to generate technical architecture with Cohere API integration"

**Technology-Agnostic Sections Preserved**:
- All 6 user stories (P1-P3) unchanged
- All 28 functional requirements unchanged (FR-001 through FR-028)
- All 12 success criteria unchanged
- All acceptance scenarios unchanged
- MCP tools specification unchanged (create, list, complete, delete, update)

**Version Notes**:
- Specification updated to reflect constitution v2.0.1 (Cohere API migration)
- No architectural changes—only AI provider implementation details updated
- All user-facing requirements remain technology-agnostic

## Outcome

- ✅ Impact: Specification successfully aligned with Cohere API per constitution v2.0.1 while preserving all functional requirements and acceptance criteria
- 🧪 Tests: N/A (specification document update only)
- 📁 Files: specs/004-ai-todo-chatbot/spec.md (updated with Cohere API details)
- 🔁 Next prompts:
  1. Run `/sp.plan` to generate technical architecture with Cohere API integration details
  2. Create ADR documenting OpenAI → Cohere migration rationale (as noted in constitution amendment)
  3. Verify MCP tool JSON schemas are Cohere-compatible during planning phase
  4. Use `/sp.tasks` to break plan into implementable tasks with Cohere-specific patterns
  5. Execute `/sp.implement` to generate code with Cohere client initialization
- 🧠 Reflection: Specification update completed with surgical precision—only AI provider references updated, all functional requirements preserved. The technology-agnostic nature of the original spec made this alignment straightforward. Updates section provides clear audit trail. Constitution v2.0.1 reference ensures consistency across all artifacts. Ready for planning phase with Cohere-specific technical details.

## Evaluation notes (flywheel)

- Failure modes observed: None - clear migration requirements provided by user and constitution amendment
- Graders run and results (PASS/FAIL): Manual review (PASS - all Cohere references updated, functional requirements unchanged)
- Prompt variant (if applicable): Specification update to align with constitutional amendment
- Next experiment (smallest change to try): Consider adding performance comparison notes (Cohere vs OpenAI) in future ADR to validate cost/performance rationale
