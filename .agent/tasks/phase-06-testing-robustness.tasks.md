---
phase: "06"
slug: testing-robustness
spec: ".agent/specs/phase-06-testing-robustness.spec.md"
---

# Phase 06 — Testing & Robustness (TASKS)

> Rules: `.agent/rules/04-security-guardrails.md` — SQL security tests are a must-have.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Unit tests | - | todo | - |
| T2 | SQL tool security tests | - | todo | - |
| T3 | Integration tests | - | todo | - |
| T4 | RAG evaluation | - | todo | - |
| T5 | Circuit Breaker | - | todo | - |
| T6 | Retry | - | todo | - |
| T7 | Fallback | - | todo | - |
| T8 | CI | - | todo | - |

---

### T1 — Unit tests
- **Assignee:** -
- **Status:** todo
- **Branch:** `test/PH06-T1-unit`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Test repositories
- [ ] Test auth/RBAC
- [ ] Test tool validators (especially SQL)
- [ ] Commit with the `Task: PH06-T1` trailer

**Notes:**

### T2 — SQL tool security tests
- **Assignee:** -
- **Status:** todo
- **Branch:** `test/PH06-T2-sql-security`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Attack case set: DROP/DELETE/UPDATE/INSERT
- [ ] Multi-statement `;`
- [ ] Comment injection
- [ ] All are blocked (tests green)
- [ ] Commit with the `Task: PH06-T2` trailer

**Notes:**

### T3 — Integration tests
- **Assignee:** -
- **Status:** todo
- **Branch:** `test/PH06-T3-integration`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `/api/chat` flow (RAG)
- [ ] Function calling
- [ ] `/api/voice/chat`
- [ ] Commit with the `Task: PH06-T3` trailer

**Notes:**

### T4 — RAG evaluation
- **Assignee:** -
- **Status:** todo
- **Branch:** `test/PH06-T4-rag-eval`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `tests/eval/` using Ragas/TruLens
- [ ] Measure faithfulness, answer relevancy, context precision
- [ ] Configurable pass threshold (e.g. faithfulness > 0.85)
- [ ] Measure the hallucination rate
- [ ] Commit with the `Task: PH06-T4` trailer

**Notes:**

### T5 — Circuit Breaker
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH06-T5-circuit-breaker`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/core/resilience.py`: pybreaker around Azure OpenAI
- [ ] Open the circuit → standard fallback message (no 500)
- [ ] Commit with the `Task: PH06-T5` trailer

**Notes:**

### T6 — Retry
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH06-T6-retry`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] tenacity for transient errors (timeout/429)
- [ ] Backoff
- [ ] Commit with the `Task: PH06-T6` trailer

**Notes:**

### T7 — Fallback
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH06-T7-fallback`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] STT/TTS/LLM error → standard text response
- [ ] No crash, no exposure of internal error details
- [ ] Commit with the `Task: PH06-T7` trailer

**Notes:**

### T8 — CI
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH06-T8-ci`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] CI runs unit + security + integration
- [ ] Eval runs on a schedule/manually (token-costly)
- [ ] Commit with the `Task: PH06-T8` trailer

**Notes:**
