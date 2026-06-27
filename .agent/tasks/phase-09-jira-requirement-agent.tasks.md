---
phase: "09"
slug: jira-requirement-agent
spec: ".agent/specs/phase-09-jira-requirement-agent.spec.md"
---

# Phase 09 — Requirement Analysis & JIRA Automation (TASKS)

> Rules: human-in-the-loop mandatory, idempotent + dry-run, JIRA token in Key Vault.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Requirement ingestion | - | todo | - |
| T2 | Requirement Analyzer agent | - | todo | - |
| T3 | Work Breakdown agent | - | todo | - |
| T4 | Human-in-the-loop review | - | todo | - |
| T5 | JIRA Sync agent | - | todo | - |
| T6 | Change Request Manager | - | todo | - |
| T7 | RBAC + feature flag | - | todo | - |
| T8 | Orchestration (LangGraph) | - | todo | - |

---

### T1 — Requirement ingestion
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T1-ingestion`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Reuse the Phase 2 multimodal pipeline
- [ ] Read requirements (PDF/Word/Excel/images) → structured text
- [ ] Citation to the original passage
- [ ] Commit with the `Task: PH09-T1` trailer

**Notes:**

### T2 — Requirement Analyzer agent
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T2-analyzer`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/agents/requirement_analyzer.py`
- [ ] Extract requirements, constraints, acceptance criteria
- [ ] Detect ambiguity/gaps/contradictions → generate clarifying questions for the BA
- [ ] Commit with the `Task: PH09-T2` trailer

**Notes:**

### T3 — Work Breakdown agent
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T3-work-breakdown`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/agents/work_breakdown.py`
- [ ] Break down Epic → Story → Task → Sub-task
- [ ] Attach estimate, priority, labels, acceptance criteria
- [ ] Each item references (citation) the original requirement passage
- [ ] Commit with the `Task: PH09-T3` trailer

**Notes:**

### T4 — Human-in-the-loop review
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T4-review-api`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Endpoint returns the proposed backlog for the BA to review/adjust
- [ ] Only proceed to the sync step once approved
- [ ] Commit with the `Task: PH09-T4` trailer

**Notes:**

### T5 — JIRA Sync agent
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T5-jira-sync`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/integrations/jira/` JIRA REST API v3 (token/OAuth, secret in Key Vault)
- [ ] Idempotent: external key (requirement id) prevents duplicate creation
- [ ] Dry-run mode: print the list of operations before writing for real
- [ ] Configurable field mapping (project, issuetype, epic link, components, labels, custom fields)
- [ ] Audit log every write operation (approver, payload, result)
- [ ] Commit with the `Task: PH09-T5` trailer

**Notes:**

### T6 — Change Request Manager
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T6-change-request`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/agents/change_request.py`
- [ ] Semantic diff of new requirements vs the released version (version/hash from Phase 2)
- [ ] Output: added/modified/removed + impact
- [ ] Propose creating/updating a change request issue
- [ ] Commit with the `Task: PH09-T6` trailer

**Notes:**

### T7 — RBAC + feature flag
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T7-rbac-flag`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Only authorized roles may sync to JIRA
- [ ] Enable/disable the entire feature via config
- [ ] Disabling does not affect the MVP
- [ ] Commit with the `Task: PH09-T7` trailer

**Notes:**

### T8 — Orchestration (LangGraph)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH09-T8-orchestration`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Plug the agents into LangGraph (Phase 8)
- [ ] The Main Agent orchestrates, preserving citations throughout
- [ ] Test: analyze sample documents → backlog; dry-run JIRA; change request diff
- [ ] Commit with the `Task: PH09-T8` trailer

**Notes:**
