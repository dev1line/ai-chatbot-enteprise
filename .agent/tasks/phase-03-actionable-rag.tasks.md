---
phase: "03"
slug: actionable-rag
spec: ".agent/specs/phase-03-actionable-rag.spec.md"
---

# Phase 03 — Actionable RAG (TASKS)

> Rules: `.agent/rules/04-security-guardrails.md` (SQL SELECT only, tool-level RBAC) is MANDATORY.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Tool framework | - | todo | - |
| T2 | Text-to-SQL tool | - | todo | - |
| T3 | Internal API tool | - | todo | - |
| T4 | Orchestrator routing | - | todo | - |
| T5 | Tool-level RBAC | - | todo | - |
| T6 | Audit log | - | todo | - |
| T7 | Integrate into /api/chat | - | todo | - |

---

### T1 — Tool framework
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T1-tool-base`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/tools/base.py`: interface with `name`, `schema`, `validate()`, `run()`, `required_role`
- [ ] Commit with the `Task: PH03-T1` trailer

**Notes:**

### T2 — Text-to-SQL tool
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T2-sql-tool`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Provide the DB schema to the LLM (schema-aware)
- [ ] Validator: only allow `SELECT`
- [ ] Block `DROP/DELETE/UPDATE/INSERT/ALTER`
- [ ] Block multi-statements (`;`) + comment injection
- [ ] Run via a limited read-only connection/role
- [ ] Commit with the `Task: PH03-T2` trailer

**Notes:**

### T3 — Internal API tool
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T3-api-tool`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/tools/api_tool.py`: endpoint whitelist (container/server status, KMS, WAF)
- [ ] Timeout
- [ ] RBAC checked before calling
- [ ] Commit with the `Task: PH03-T3` trailer

**Notes:**

### T4 — Orchestrator routing
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T4-agent-routing`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/orchestration/agent.py`: expose tool schemas to Azure OpenAI Function Calling
- [ ] The LLM chooses RAG vs tool
- [ ] Tool-call loop → result → summarize
- [ ] Document questions still go through RAG (no unnecessary tool calls)
- [ ] Commit with the `Task: PH03-T4` trailer

**Notes:**

### T5 — Tool-level RBAC
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T5-rbac-tool`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Before `run()`: check that `current_user` has the `required_role`
- [ ] Prevent the LLM "hallucinating" permissions
- [ ] User lacking permission → blocked
- [ ] Commit with the `Task: PH03-T5` trailer

**Notes:**

### T6 — Audit log
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T6-audit-log`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Log every tool call: user, tool, params, result summary, latency
- [ ] Do not log sensitive information
- [ ] Commit with the `Task: PH03-T6` trailer

**Notes:**

### T7 — Integrate into /api/chat
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH03-T7-chat-actions`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Distinguish RAG answers vs actions (with data)
- [ ] Test: valid SQL runs; destructive SQL is blocked; RBAC blocks users lacking permission
- [ ] Commit with the `Task: PH03-T7` trailer

**Notes:**
