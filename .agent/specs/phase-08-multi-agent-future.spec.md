---
phase: "08"
slug: multi-agent-future
title: "Multi-Agent & Future Enhancements"
status: todo
depends_on: ["07"]
source_prompt: "prompts/phase-08-multi-agent-future/prompt.md"
---

# Phase 08 — Multi-Agent & Future Enhancements (SPEC)

## Context
The MVP is production-ready (Phases 0–7). Upgrade to a Multi-Agent architecture + extended use cases (ODC English Trainer).

## Objective
Replace the single orchestrating LLM with Multi-Agent (LangGraph/AutoGen) to improve accuracy; add an "ODC Communication" module (English Trainer).

## Scope
- **In:** multi-agent orchestrator, specialized sub-agents, ODC English Trainer.
- **Out:** rewriting already-stable layers (reuse existing tools/RAG).

## Deliverables
- LangGraph multi-agent orchestrator + sub-agents.
- Accuracy comparison report.
- ODC English Trainer module (voice-based).

## Acceptance Criteria
- [ ] Multi-agent correctly handles mixed queries (both doc and SQL/logs).
- [ ] Eval shows accuracy ≥ single-agent.
- [ ] Citations are still preserved through the orchestrator.
- [ ] The English Trainer conducts a voice conversation + gives error-correction feedback.
- [ ] A feature flag exists, with no impact on the MVP flow when disabled.

## Guardrails
- Reuse tested tools/RAG/voice, no duplicated logic.
- Keep the security guardrails (tool-level RBAC, SELECT only, Zero Data Leak).
- Multi-agent must not increase latency beyond the SLA.

## Links
- Tasks: `.agent/tasks/phase-08-multi-agent-future.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
