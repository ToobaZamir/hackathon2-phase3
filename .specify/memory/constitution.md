<!-- Sync Impact Report:
Version change: N/A (initial creation) → 1.0.0
Modified principles: N/A
Added sections: All sections added based on user input
Removed sections: N/A
Templates requiring updates: N/A
Follow-up TODOs: None
-->
# Spec-Driven Full-Stack Multi-User Todo Web Application Constitution

## Core Principles

### Spec-First Development
No implementation before specification. All features must originate from a written spec before implementation begins. Zero manual coding (Claude Code only). All system behaviors must be explicitly defined with no assumptions.

### Security-by-Design
JWT-based authentication enforced everywhere. User data isolation with strict ownership enforcement. Every API request must require a valid JWT (except signup/login). JWT signature must be verified on backend. JWT must be validated for expiration. User ID must be extracted from token, not from request body. URL user_id must match token user_id. Cross-user access is forbidden. Backend enforces ownership, not frontend.

### Deterministic Reproducibility
Same prompts equal same results. All business rules must be testable. All endpoints protected by JWT. Users can only access their own tasks. No unauthenticated data access possible.

### API-First Architecture
RESTful API compliance with HTTP semantics, status codes, and resource-based routes. All endpoints must return structured JSON. Errors must be explicit and machine-readable. Frontend and backend communicate only via REST. Stateless backend design.

### Separation of Concerns
Frontend, backend, auth, and database responsibilities clearly separated. Frontend must never directly access the database. Backend must never trust frontend identity without JWT verification. All user actions must be authorized server-side. All system behaviors must be explicitly defined.

### Traceability
Every feature maps to a spec requirement. All features implemented exactly as specified. Full CRUD functionality implemented. Task completion toggle works correctly.

## Key Standards and Constraints

Backend: Python FastAPI only. ORM: SQLModel only. Database: Neon Serverless PostgreSQL only. Frontend: Next.js 16+ (App Router) only. Authentication: Better Auth only. Auth mechanism: JWT tokens only. No server-side sessions. No monolithic architecture. No hardcoded credentials. No direct database access from frontend. No manual code edits (Claude Code only). Must follow Agentic Dev Stack: Spec → Plan → Tasks → Implement. Must support multi-user usage. Must be cloud deployable. Must be stateless.

Non-negotiable security rules: Every API request must require a valid JWT (except signup/login). JWT signature must be verified on backend. JWT must be validated for expiration. User ID must be extracted from token, not from request body. URL user_id must match token user_id. Cross-user access is forbidden. Backend enforces ownership, not frontend. 401 for unauthenticated. 403 for unauthorized. 404 for inaccessible resources.

## Development Workflow

Must follow Agentic Dev Stack: Spec → Plan → Tasks → Implement. All features must originate from a written spec before implementation. All system behaviors must be explicitly defined with no assumptions. Environment-based configuration only (no hardcoding secrets). All business rules must be testable. Stateless backend design. All endpoints must return structured JSON. Errors must be explicit and machine-readable.

## Governance

This constitution governs all development practices for the Spec-Driven Full-Stack Multi-User Todo Web Application. All implementation must comply with these principles. Any deviation requires explicit constitutional amendment. Code reviews must verify compliance with all security rules and architectural constraints. Implementation must strictly follow the Agentic Dev Stack workflow.

**Version**: 1.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09