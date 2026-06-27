---
phase: "<NN>"
slug: "<slug>"
title: "<Phase title>"
status: todo            # todo | in_progress | review | done
depends_on: ["<NN-1>"] # phases this depends on
source_prompt: "prompts/phase-<NN>-<slug>/prompt.md"
---

# Phase <NN> — <Title> (SPEC)

## Context
<Position in the roadmap, dependency on the previous phase.>

## Objective
<Main objective of the phase.>

## Scope
- **In:** <what to do>
- **Out:** <what not to do>

## Deliverables
- <file/artifact to create>

## Acceptance Criteria
- [ ] <completion condition 1>
- [ ] <completion condition 2>

## Guardrails
- <technical / security constraint>

## Links
- Tasks: `.agent/tasks/phase-<NN>-<slug>.tasks.md`
- Applicable rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
