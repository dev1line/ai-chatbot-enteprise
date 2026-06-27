---
phase: "06"
slug: testing-robustness
title: "Testing & Robustness"
status: todo
depends_on: ["05"]
source_prompt: "prompts/phase-06-testing-robustness/prompt.md"
---

# Phase 06 — Testing & Robustness (SPEC)

## Context
The system is feature-complete (Phases 0–5). Ensure quality & durability: test function calling, evaluate RAG, handle exceptions.

## Objective
A comprehensive test suite + LLM quality measurement (Ragas/TruLens) + fault-tolerance mechanisms (Circuit Breaker + Retry + Fallback).

## Scope
- **In:** unit/integration tests, SQL tool security tests, RAG eval, Circuit Breaker, Retry, Fallback.
- **Out:** infrastructure deployment (Phase 7).

## Deliverables
- Test suite (unit/integration/security).
- Ragas/TruLens eval harness + threshold report.
- Resilience module (circuit breaker + retry + fallback).

## Acceptance Criteria
- [ ] Every destructive SQL case is blocked (tests green).
- [ ] RAG eval meets the configured thresholds; metrics reported.
- [ ] Azure timeout → Circuit Breaker opens → fallback, no 500.
- [ ] Retry works for transient errors.
- [ ] CI runs the tests and passes.

## Guardrails
- SQL security tests are a must-have.
- Eval must measure hallucination, not just "it runs".
- The fallback message does not expose internal error details.

## Links
- Tasks: `.agent/tasks/phase-06-testing-robustness.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
