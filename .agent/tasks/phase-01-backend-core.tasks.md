---
phase: "01"
slug: backend-core
spec: ".agent/specs/phase-01-backend-core.spec.md"
---

# Phase 01 — Backend Core & Architecture (TASKS)

> Rules: `.agent/rules/03-task-management.md` + `.agent/rules/01-git-workflow.md`.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Prisma schema | - | todo | - |
| T2 | Migration + generate client | - | todo | - |
| T3 | Repository Pattern | - | todo | - |
| T4 | Auth / JWT | - | todo | - |
| T5 | RBAC | - | todo | - |
| T6 | Pydantic schemas | - | todo | - |
| T7 | Chat endpoint (mock) | - | todo | - |
| T8 | Cross-cutting (logging, exceptions, CORS) | - | todo | - |

---

### T1 — Prisma schema
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T1-prisma-schema`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Models `User`, `Role`, `Conversation`, `Message`, `Document` (metadata)
- [ ] Relations between the models
- [ ] Role enum: `ADMIN`, `ENGINEER`, `VIEWER`
- [ ] Commit with the `Task: PH01-T1` trailer

**Notes:**

### T2 — Migration + generate client
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T2-migration`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Migration runs successfully on local Postgres
- [ ] Generate the Prisma client
- [ ] Commit with the `Task: PH01-T2` trailer

**Notes:**

### T3 — Repository Pattern
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T3-repository-pattern`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `UserRepository`
- [ ] `ConversationRepository`
- [ ] `MessageRepository`
- [ ] Isolate all DB queries — routers do NOT call Prisma directly
- [ ] Unit tests for the repository pass
- [ ] Commit with the `Task: PH01-T3` trailer

**Notes:**

### T4 — Auth / JWT
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T4-auth`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/core/security.py`: JWT issue/verify
- [ ] Password hashing
- [ ] `get_current_user` dependency
- [ ] Register/login returns a valid JWT
- [ ] Unit tests for auth pass
- [ ] Commit with the `Task: PH01-T4` trailer

**Notes:**

### T5 — RBAC
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T5-rbac`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/core/rbac.py`: `require_role(...)` dependency/decorator
- [ ] Design extensible to the tool layer (Phase 3)
- [ ] User lacking permission → 403
- [ ] Commit with the `Task: PH01-T5` trailer

**Notes:**

### T6 — Pydantic schemas
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T6-schemas`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Request/response schemas for chat
- [ ] Request/response schemas for auth
- [ ] Commit with the `Task: PH01-T6` trailer

**Notes:**

### T7 — Chat endpoint (mock)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T7-chat-endpoint`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `POST /api/chat` requires auth
- [ ] Store Conversation/Message via the repository
- [ ] Return a mock response (placeholder orchestrator)
- [ ] Commit with the `Task: PH01-T7` trailer

**Notes:**

### T8 — Cross-cutting (logging, exceptions, CORS)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH01-T8-cross-cutting`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Structured logging (request_id, user_id, latency)
- [ ] Global exception handlers (do not expose internal details)
- [ ] CORS configuration
- [ ] Logs contain no sensitive data
- [ ] Commit with the `Task: PH01-T8` trailer

**Notes:**
