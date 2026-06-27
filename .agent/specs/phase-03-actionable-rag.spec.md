---
phase: "03"
slug: actionable-rag
title: "Actionable RAG (Function Calling)"
status: todo
depends_on: ["02"]
source_prompt: "prompts/phase-03-actionable-rag/prompt.md"
---

# Phase 03 — Actionable RAG (SPEC)

## Context
RAG already answers from documents. Add the ability to act: the LLM calls a Text-to-SQL tool (reports) and an internal API (Ops/Security), safely + with RBAC.

## Objective
Function Calling with LangChain/Azure OpenAI: a `text_to_sql` tool (SELECT only) and an `internal_api_call` tool, with validation + sandbox + tool-layer RBAC.

## Scope
- **In:** tool schema, safe text-to-SQL, internal API tool, tool routing in the orchestrator, tool-level RBAC.
- **Out:** voice (Phase 4), UI (Phase 5).

## Deliverables
- Tool base + sql_tool + api_tool + agent routing.
- Audit logging for tool calls.
- Tests: valid SQL runs; destructive SQL is blocked; RBAC blocks users lacking permission.

## Acceptance Criteria
- [ ] "Revenue this week by project?" → generates the correct SELECT → returns the figures.
- [ ] Commands containing DROP/DELETE/UPDATE/INSERT are safely rejected.
- [ ] The internal API tool only calls whitelisted endpoints.
- [ ] A user lacking permission calling a tool → blocked (audit recorded).
- [ ] Document questions still go through the RAG flow (no unnecessary tool calls).

## Guardrails
- SELECT only for SQL; a dedicated read-only DB role for the tool.
- Every tool has `validate()` before `run()`.
- RBAC is mandatory at the tool layer; do not trust the LLM to decide.
- Full audit log, without exposing sensitive information.

## Links
- Tasks: `.agent/tasks/phase-03-actionable-rag.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
