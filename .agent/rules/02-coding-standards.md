# Rule 02 — Coding Standards

## Backend (Python / FastAPI)
- Formatting & lint: **black** + **ruff** (via `.pre-commit-config.yaml`).
- Structure: `app/{api,core,orchestration,rag,tools,voice,repositories,schemas}`.
- **Repository Pattern**: routers do NOT call Prisma/DB directly — only via `repositories/`.
- Config via `pydantic-settings` (`app/core/config.py`); do not read env in scattered places.
- Validation with Pydantic schemas (`app/schemas/`).
- Errors: use global exception handlers; do not expose internal details to the client.
- Structured logging: `request_id`, `user_id`, `latency`; do not log sensitive data.
- Full type hints for public functions.

## Frontend (React + TypeScript + Vite)
- TypeScript `strict`; no careless `any`.
- Separate `components/`, `hooks/`, `api/`.
- Typed API client; handle 401/403 and network errors with a fallback message.
- UX: responsive, accessible, with loading/streaming/recording indicators.

## General
- Clear file/variable names; no redundant comments that merely restate the code.
- Comments should only explain the **reason / constraint**, not narrate.
- Pin dependency versions; do not bump versions outside the task's scope.
- Add tests for new code; run `make test` before opening a PR.

## Definition of Done (for each task)
- [ ] Code runs locally via Docker (Phases 0–6).
- [ ] Lint/format passes (ruff/black, tsc).
- [ ] Relevant tests pass.
- [ ] Complies with the phase's Guardrails in the spec.
- [ ] Sub-checklist in `.tasks.md` is fully ticked.
- [ ] Commit has the `Task:` trailer; `Status` updated to `done`.
