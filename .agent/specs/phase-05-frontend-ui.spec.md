---
phase: "05"
slug: frontend-ui
title: "Frontend / UI Quality"
status: todo
depends_on: ["04"]
source_prompt: "prompts/phase-05-frontend-ui/prompt.md"
---

# Phase 05 — Frontend / UI Quality (SPEC)

## Context
The backend is complete: RAG, Actionable RAG, Voice. Build a professional UI: Chat Console, Hold-to-Talk, mandatory Citations.

## Objective
A React + TypeScript SPA: modern chat, hands-free voice, transparent sources (citations).

## Scope
- **In:** Chat Console UI, Hold-to-Talk (Web Audio API), citations panel, streaming render, auth UI, typed API client.
- **Out:** changes to backend logic.

## Deliverables
- ChatConsole, HoldToTalk, Citations, Login, hooks, api client.
- UI fully connected to the backend (text + voice).

## Acceptance Criteria
- [ ] Send a text question → answer streams in gradually + citations are displayed.
- [ ] Press-and-hold to speak → receive an answer in audio.
- [ ] RAG answers always include citations; click to view the source.
- [ ] Handle 401/403 and network errors gracefully.

## Guardrails
- TypeScript strict; error handling with a fallback message.
- Citations must be displayed for RAG answers.
- Store the JWT securely; do not expose the token.

## Links
- Tasks: `.agent/tasks/phase-05-frontend-ui.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/02-coding-standards.md`
