---
phase: "00"
slug: foundation
spec: ".agent/specs/phase-00-foundation.spec.md"
---

# Phase 00 — Foundation & Project Setup (TASKS)

> Rules: `.agent/rules/03-task-management.md` + `.agent/rules/01-git-workflow.md`.
> Claim a task: fill in `Assignee` (id in `progress/assignees.yaml`) + change `Status` → `in_progress`.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Monorepo directory structure | - | todo | - |
| T2 | Backend deps (pyproject) | - | todo | - |
| T3 | Frontend Vite + React + TS | - | todo | - |
| T4 | Config + environment flags + .env.example | - | todo | - |
| T5 | Docker Compose local-first | - | todo | - |
| T6 | Makefile / scripts | - | todo | - |
| T7 | Health check endpoint | - | todo | - |
| T8 | Quality: pre-commit + CI | - | todo | - |
| T9 | README backend/frontend | - | todo | - |

---

### T1 — Monorepo directory structure
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH00-T1-scaffold`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Create `backend/app/{api,core,orchestration,rag,tools,voice,repositories,schemas}`
- [ ] Create `backend/{prisma,tests}`
- [ ] Create `frontend/src/{components,hooks,api}`
- [ ] Create `infra/`
- [ ] Commit with the `Task: PH00-T1` trailer

**Notes:**

### T2 — Backend deps (pyproject)
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH00-T2-backend-deps`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `backend/pyproject.toml`: fastapi, uvicorn, pydantic-settings, prisma
- [ ] Add langchain, openai (azure), tenacity, pybreaker, python-multipart, pytest
- [ ] Pin clear versions for every dependency
- [ ] Installs and runs inside the container
- [ ] Commit with the `Task: PH00-T2` trailer

**Notes:**

### T3 — Frontend Vite + React + TS
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH00-T3-frontend-init`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Initialize Vite + React + TypeScript (`frontend/package.json`)
- [ ] `tsconfig.json` strict mode
- [ ] A blank page builds & runs
- [ ] Commit with the `Task: PH00-T3` trailer

**Notes:**

### T4 — Config + environment flags + .env.example
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH00-T4-config-env`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/core/config.py` uses `pydantic-settings` to read env
- [ ] Expose `APP_ENV` (`local|docker|staging|prod`)
- [ ] Expose providers: `LLM_PROVIDER`, `VECTOR_DB_PROVIDER`, `OCR_PROVIDER`, `STT_PROVIDER`, `TTS_PROVIDER`, `SECRETS_PROVIDER`
- [ ] `.env.example` with all variables + a comment "Azure only enabled in staging/prod"
- [ ] Do NOT commit the real `.env`
- [ ] Commit with the `Task: PH00-T4` trailer

**Notes:**

### T5 — Docker Compose local-first
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH00-T5-docker-compose`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `postgres` service + volume
- [ ] Local vector DB service (Milvus or Qdrant)
- [ ] `backend` + `frontend` services
- [ ] `docker compose up` runs the full stack without Azure
- [ ] Commit with the `Task: PH00-T5` trailer

**Notes:**

### T6 — Makefile / scripts
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH00-T6-makefile`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `make dev-up` / `make dev-down` (local docker)
- [ ] `make logs`, `make test`
- [ ] Placeholder `make infra-*` (not yet implemented, for Phase 7)
- [ ] Commit with the `Task: PH00-T6` trailer

**Notes:**

### T7 — Health check endpoint
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH00-T7-health`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `GET /health` returns `{"status":"ok","app_env":"<APP_ENV>"}`
- [ ] pytest for health passes
- [ ] Commit with the `Task: PH00-T7` trailer

**Notes:**

### T8 — Quality: pre-commit + CI
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH00-T8-quality`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `.pre-commit-config.yaml` (ruff + black)
- [ ] Complete `.gitignore` (excludes `.env`, artifacts)
- [ ] GitHub Actions CI runs lint + pytest (local/container, no Azure needed)
- [ ] Commit with the `Task: PH00-T8` trailer

**Notes:**

### T9 — README backend/frontend
- **Assignee:** -
- **Status:** todo
- **Branch:** `docs/PH00-T9-readme`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Backend README: commands to run locally via Docker + explanation of `APP_ENV`
- [ ] Frontend README: commands to run + configuration
- [ ] Commit with the `Task: PH00-T9` trailer

**Notes:**
