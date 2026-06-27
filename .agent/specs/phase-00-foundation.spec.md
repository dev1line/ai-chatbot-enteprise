---
phase: "00"
slug: foundation
title: "Foundation & Project Setup"
status: todo
depends_on: []
source_prompt: "prompts/phase-00-foundation/prompt.md"
---

# Phase 00 — Foundation & Project Setup (SPEC)

## Context
The first phase. Set up the repo skeleton, environment, and tooling for later phases to build on.

## Objective
Create a monorepo `backend/` + `frontend/` + `infra/`, configure the environment, Docker, and basic CI.
**LOCAL-FIRST/DOCKER-FIRST**: everything runs locally via Docker Compose, with no dependency on Azure.

## Scope
- **In:** directory scaffold, dependency manifests, `.env.example` with environment flags, full-stack local Docker Compose (Postgres + Vector DB + backend + frontend), Makefile/scripts distinguishing modes, pre-commit, CI lint/test skeleton.
- **Out:** RAG, function calling, voice, UI logic; Azure/IaC infrastructure (Phase 7).

## Deliverables
- Complete directory tree + manifests.
- `docker-compose.yml` running the full stack locally.
- Makefile `dev-up/dev-down/test` + placeholder `infra-*`.
- `.env.example` with `APP_ENV` flag + providers.
- CI workflow file.

## Acceptance Criteria
- [ ] `make dev-up` starts the full stack locally without Azure.
- [ ] `GET /health` returns 200 with `app_env`.
- [ ] Vector DB container (Milvus/Qdrant) runs & is reachable.
- [ ] `pytest` runs locally/in container (at least 1 health test passes).
- [ ] Frontend opens a blank page.
- [ ] Switching providers via ENV requires no code changes.
- [ ] No hardcoded secrets; all config via env.

## Guardrails
- LOCAL-FIRST; `APP_ENV` flag + provider swappability mandatory.
- Do NOT commit the real `.env`.
- Pin dependency versions.
- Follow the structure in `docs/01-architecture.md` section 3.

## Links
- Tasks: `.agent/tasks/phase-00-foundation.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
