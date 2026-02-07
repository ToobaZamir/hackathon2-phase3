# ADR 001: Selection of Cohere API for LLM Provider

**Date**: 2026-02-07
**Status**: Accepted
**Decision Makers**: Architecture Team
**Phase**: Phase 3 - AI Todo Chatbot

---

## Context

For Hackathon II Phase 3, we need to select an LLM provider to power the AI todo assistant. The system requires:

- **Tool calling capabilities** for MCP tool integration (5 CRUD operations)
- **Multi-step reasoning** for complex user intents (e.g., "complete buy groceries" requires list → complete)
- **Natural language understanding** for conversational task management
- **Cost-effective pricing** for tool-heavy workflows
- **Reliable API** with good uptime and documentation

Initial constitution (v2.0.0) specified OpenAI API, but we reconsidered this decision during technical planning.

## Decision

**We will use Cohere API (specifically command-a-03-2025 model) instead of OpenAI API.**

### Implementation Strategy

1. **Primary Integration**: OpenAI SDK with Cohere compatibility endpoint
   - Base URL: `https://api.cohere.ai/compatibility/v1`
   - Model: `command-a-03-2025` (optimized for tool use)
   - Allows minimal code changes from OpenAI patterns

2. **Fallback Option**: Native Cohere SDK
   - Available if compatibility layer has limitations
   - Provides access to advanced Cohere features (citations, multi-step)

3. **Alternative Model**: `command-r-plus-08-2024`
   - For complex reasoning tasks requiring long context (128k tokens)

## Rationale

### Cost/Performance Benefits

- **Better pricing** for tool-calling workflows compared to OpenAI GPT-4
- **Optimized models** specifically designed for agentic workflows (command-a series)
- **Lower latency** for tool-heavy interactions

### Technical Advantages

1. **Strong Tool Calling**:
   - Native JSON schema support (compatible with OpenAI function calling format)
   - Excellent at detecting user intent and mapping to tools
   - Reliable multi-step reasoning for tool chaining

2. **Multilingual Capabilities**:
   - Strong support for non-English languages
   - Useful for future international expansion (out of scope for Phase 3 but valuable)

3. **OpenAI SDK Compatibility**:
   - Can use familiar OpenAI SDK patterns
   - Minimal code refactoring required
   - Easy to swap back if needed

4. **Multi-Step Reasoning**:
   - Handles complex workflows: "Complete buy groceries" → list_tasks() → complete_task(id)
   - Better at maintaining conversation context
   - Strong performance on ambiguous requests

### Risks Mitigated

- **Lock-in Risk**: OpenAI SDK compatibility means we're not fully locked into Cohere
- **Tool Calling Risk**: Early testing confirmed excellent tool calling support
- **Cost Risk**: Better pricing structure for our use case
- **Migration Risk**: Can switch back to OpenAI with minimal code changes (just change base_url and model)

## Alternatives Considered

### Alternative 1: OpenAI GPT-4 (Original Plan)

**Pros**:
- Familiar API and SDK
- Excellent tool calling support
- Strong documentation and community

**Cons**:
- Higher cost for tool-heavy workflows
- No specific agentic optimization
- Limited multilingual capabilities compared to Cohere

**Rejected**: Cost concerns for tool-intensive chatbot

### Alternative 2: Anthropic Claude

**Pros**:
- Excellent reasoning capabilities
- Strong tool use support
- Good multilingual support

**Cons**:
- Different SDK/API patterns
- More expensive than Cohere
- No OpenAI compatibility layer

**Rejected**: Higher cost, more integration work

### Alternative 3: Open-Source Models (Llama, Mistral)

**Pros**:
- Lower operational cost
- Full control over deployment
- No API rate limits

**Cons**:
- Requires infrastructure setup
- Tool calling less mature
- Latency concerns for real-time chat
- Complexity for hackathon timeline

**Rejected**: Too complex for hackathon scope

## Consequences

### Positive

1. **Cost Savings**: Reduced API costs for tool-heavy chatbot
2. **Better Performance**: Optimized models for agentic workflows
3. **Multilingual Ready**: Strong foundation for future expansion
4. **Easy Migration**: OpenAI SDK compatibility provides flexibility

### Negative

1. **New Provider Risk**: Less familiar with Cohere API quirks
2. **Documentation**: Slightly less community content compared to OpenAI
3. **Monitoring**: Need to set up monitoring for new provider

### Neutral

1. **Learning Curve**: Minimal due to OpenAI SDK compatibility
2. **Testing Required**: Need to validate tool calling works as expected
3. **API Key Management**: New environment variable (COHERE_API_KEY)

## Implementation Details

### Configuration

```python
# backend/src/core/config.py
cohere_api_key: str = os.getenv("COHERE_API_KEY")
cohere_model: str = os.getenv("COHERE_MODEL", "command-a-03-2025")
cohere_base_url: str = os.getenv("COHERE_BASE_URL", "https://api.cohere.ai/compatibility/v1")
```

### Client Initialization

```python
# backend/src/agent/cohere_client.py
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("COHERE_API_KEY"),
    base_url="https://api.cohere.ai/compatibility/v1"
)
```

### Tool Schema Format

MCP tools use OpenAI function calling format (JSON schema), which Cohere supports natively:

```python
{
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Creates a new task",
        "parameters": {
            "type": "object",
            "properties": {...},
            "required": [...]
        }
    }
}
```

## Validation

### Acceptance Criteria

- [X] Tool calling works with all 5 MCP tools
- [X] Multi-step reasoning handles tool chaining
- [X] Natural language understanding parses user intents correctly
- [X] OpenAI SDK compatibility layer functions as expected
- [X] Error handling gracefully handles API failures

### Testing Plan

1. **Unit Tests**: Tool calling with mock responses
2. **Integration Tests**: End-to-end chat flow with Cohere
3. **Manual Tests**: All 6 user stories with natural language commands
4. **Performance Tests**: Response time <3s for 90% of requests

## Related Documents

- **Constitution Amendment**: v2.0.1 (Phase 3 Cohere migration)
- **Specification**: `specs/004-ai-todo-chatbot/spec.md`
- **Architecture Plan**: `specs/004-ai-todo-chatbot/plan.md` (Section 3.1)
- **System Prompt**: `backend/src/agent/system_prompt.py`

## Revision History

- **v1.0 (2026-02-07)**: Initial ADR documenting Cohere selection
- **Status**: Accepted and implemented in Phase 3

---

**Decision Owner**: Architecture Team
**Reviewers**: Technical Lead, Product Manager
**Implementation**: Phase 3 (Complete)
