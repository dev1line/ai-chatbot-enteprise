# PROGRESS — Overall project progress table

> Update whenever a task's `Status` changes. Count: `done / total tasks` per phase.
> See per-task details in `.agent/tasks/phase-*.tasks.md`.

## Overview by phase

| Phase | Title | Tasks | Done | Status | Primary owner |
|-------|---------|:-----:|:----:|--------|-----------------|
| 00 | Foundation & Project Setup | 9 | 0 | todo | - |
| 01 | Backend Core & Architecture | 8 | 0 | todo | - |
| 02 | Multimodal RAG | 9 | 0 | todo | - |
| 03 | Actionable RAG (Function Calling) | 7 | 0 | todo | - |
| 04 | Voice Pipeline | 6 | 0 | todo | - |
| 05 | Frontend / UI Quality | 7 | 0 | todo | - |
| 06 | Testing & Robustness | 8 | 0 | todo | - |
| 07 | Security & Deployment | 9 | 0 | todo | - |
| 08 | Multi-Agent & Future | 5 | 0 | todo | - |
| 09 | Requirement & JIRA Automation | 8 | 0 | todo | - |
| **Total** | | **76** | **0** | | |

Valid statuses: `todo | in_progress | blocked | review | done`.

## Recent activity (update manually on merge)

| Date | Phase/Task | Assignee | Action | Commit/PR |
|------|-----------|----------|-----------|-----------|
| - | - | - | - | - |

## How to update this table
1. When a task moves to `done`, increment the **Done** column of the corresponding phase.
2. When all tasks are done & the spec's Acceptance Criteria are met → change the phase **Status** → `done` (and in `.agent/config.yaml`).
3. Add one row to "Recent activity" including the assignee + commit/PR.

## Trace "who did what" via git
```bash
git shortlog -sne                                    # totals per person
git log --grep="Task: PH<NN>-T<n>" --pretty="%h %an %s"
git log --author="<email>" --oneline
```
