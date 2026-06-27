---
phase: "01"
slug: backend-core
title: "Backend Core & Architecture"
status: todo
depends_on: ["00"]
source_prompt: "prompts/phase-01-backend-core/prompt.md"
---

# Phase 01 — Backend Core & Architecture (SPEC)

## Context
Continuing from Phase 0. Build the backend foundation: data layer, auth, RBAC, Repository Pattern.

## Objective
A FastAPI app with a clear structure: Prisma + PostgreSQL, JWT auth, RBAC, Repository Pattern, standard error handling & logging.

## Scope
- **In:** Prisma schema, migrations, repositories, auth/JWT, RBAC middleware, base chat endpoint (mock LLM), logging, exception handlers.
- **Out:** RAG retrieval, real function calling, voice. LLM mocked for now.

## Deliverables
- Prisma schema + working migration.
- Repositories + auth + RBAC + chat endpoint (mock).
- Unit tests for repository & auth.

## Acceptance Criteria
- [ ] Register/login returns a valid JWT.
- [ ] `POST /api/chat` requires auth, stores the message, returns a mock answer.
- [ ] RBAC blocks users lacking permission (403).
- [ ] Routers do NOT call Prisma directly (only via repositories).
- [ ] `pytest` for repo/auth passes.

## Guardrails
- No direct DB calls outside the repository layer.
- RBAC is extensible to the tool layer (Phase 3).
- All secrets via env / Key Vault.
- Logs contain no sensitive data.

## Links
- Tasks: `.agent/tasks/phase-01-backend-core.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/02-coding-standards.md`, `.agent/rules/04-security-guardrails.md`
