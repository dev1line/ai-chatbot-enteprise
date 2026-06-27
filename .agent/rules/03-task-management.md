# Rule 03 — Spec, Task & Progress Management

## Concepts
- **Spec** (`specs/*.spec.md`): describes **WHAT/WHY** — objective, scope, deliverables, acceptance, guardrails of a phase.
- **Task** (`tasks/*.tasks.md`): describes **HOW/WHO** — the work list, where each task has a **sub-checklist**,
  **Assignee** (git), **Status**, **Branch**, **Commits**, **PR**.
- **Progress** (`progress/PROGRESS.md`): the overall project progress summary table.

## Lifecycle of a task
```
todo → in_progress → review → done
              ↘ blocked ↗
```

## Rules when working on a task
1. **Claim**: fill in `Assignee` = your id (in `assignees.yaml`), change `Status` → `in_progress`.
2. Create a branch per `rules/01-git-workflow.md`.
3. Follow the **sub-checklist**; tick `[x]` as soon as each item is done (do not tick ahead of time).
4. Commit with the `Task: PH<NN>-T<n>` trailer; add the hash to the `Commits` field.
5. When the whole checklist is done + the related acceptance is met → `Status` → `review` → (after review) `done`.
6. Update `progress/PROGRESS.md` (count tasks done / total).
7. If blocked: `Status` → `blocked` and note the reason in the task's `Notes` section.

## Editing rules
- Do not delete old tasks; if cancelled → `Status: cancelled` + reason.
- New tasks must have a consecutive id `T<n+1>` and a complete checklist.
- When the spec's acceptance criteria are fully met → mark the phase `done` in `config.yaml` + `PROGRESS.md`.

## Invariants to check on every PR
- Every ticked checklist item must have a corresponding commit (traceable via the `Task:` trailer).
- A task's `Assignee` matches the commit's `author` (git).
- No `done` task whose acceptance criteria are not yet met.
