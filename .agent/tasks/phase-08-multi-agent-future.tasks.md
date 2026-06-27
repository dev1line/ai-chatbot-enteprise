---
phase: "08"
slug: multi-agent-future
spec: ".agent/specs/phase-08-multi-agent-future.spec.md"
---

# Phase 08 — Multi-Agent & Future Enhancements (TASKS)

> Rules: reuse tested tools/RAG/voice; keep the security guardrails.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Multi-Agent orchestration | - | todo | - |
| T2 | Routing & merging | - | todo | - |
| T3 | Evaluation multi vs single | - | todo | - |
| T4 | ODC English Trainer | - | todo | - |
| T5 | Feature flag | - | todo | - |

---

### T1 — Multi-Agent orchestration
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH08-T1-langgraph`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/orchestration/graph.py` (LangGraph)
- [ ] Main Agent (Orchestrator): delegate work, aggregate
- [ ] SQL Sub-Agent (reuse `sql_tool` from Phase 3)
- [ ] Docs Sub-Agent (reuse the Phase 2 retriever)
- [ ] Logs/Ops Sub-Agent (use `api_tool`)
- [ ] Commit with the `Task: PH08-T1` trailer

**Notes:**

### T2 — Routing & merging
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH08-T2-routing-merge`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] The orchestrator decides which sub-agent(s) to call
- [ ] Merge the results
- [ ] Ensure citations are still preserved
- [ ] Commit with the `Task: PH08-T2` trailer

**Notes:**

### T3 — Evaluation multi vs single
- **Assignee:** -
- **Status:** todo
- **Branch:** `test/PH08-T3-eval-compare`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Compare multi-agent vs single-agent accuracy via the Phase 6 eval harness
- [ ] Demonstrate improvement (≥ single-agent)
- [ ] Report the results
- [ ] Commit with the `Task: PH08-T3` trailer

**Notes:**

### T4 — ODC English Trainer
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH08-T4-english-trainer`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/features/english_trainer.py`
- [ ] Leverage the voice pipeline (Phase 4): English conversation
- [ ] Detect & correct grammar/pronunciation errors; suggest industry-specific phrasing
- [ ] Prompt engineering for a "foreign customer/colleague" persona
- [ ] Commit with the `Task: PH08-T4` trailer

**Notes:**

### T5 — Feature flag
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH08-T5-feature-flag`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Enable/disable multi-agent & english trainer via config
- [ ] Disabling does not affect the MVP flow
- [ ] Commit with the `Task: PH08-T5` trailer

**Notes:**
