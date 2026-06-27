# `.agent/` — Progress & rules management system for the AI Agent / Team

This directory is the **source of truth** for managing how the AI coding agent and humans
work together on the **Enterprise AI Chatbot ("Actionable RAG")** project.

It answers 4 questions:

1. **Which rules to follow?** → `rules/`
2. **What to build (specifications)?** → `specs/`
3. **How far along, and who is doing what (progress + assignee/git)?** → `tasks/` + `progress/`
4. **Shared configuration?** → `config.yaml`

---

## Structure

```
.agent/
├── README.md                ← you are reading this
├── config.yaml              ← shared configuration (phase, branch, git identity)
├── rules/                   ← mandatory rules & instructions
│   ├── 00-global.md         ← core principles (Zero Data Leak, local-first…)
│   ├── 01-git-workflow.md   ← branch / commit / PR / assignee mapping via git
│   ├── 02-coding-standards.md
│   ├── 03-task-management.md ← how to use spec + task + update progress
│   └── 04-security-guardrails.md
├── specs/                   ← per-phase specifications (WHAT & WHY)  *.spec.md
│   ├── SPEC-template.md
│   └── phase-00..09 *.spec.md
├── tasks/                   ← execution checklist + assignee/git (HOW & WHO) *.tasks.md
│   ├── TASK-template.md
│   └── phase-00..09 *.tasks.md
└── progress/
    ├── PROGRESS.md          ← overall project progress table
    └── assignees.yaml       ← assignee list + git identity
```

> `.spec` = specification. `.tasks` = work list with a checklist + owner.
> File naming convention: `phase-<NN>-<slug>.spec.md` and `phase-<NN>-<slug>.tasks.md`.

---

## Standard workflow (every agent/human MUST follow)

1. Read `rules/` before coding (especially `00-global.md` + `04-security-guardrails.md`).
2. Open `specs/phase-<NN>-*.spec.md` to understand the scope & acceptance criteria.
3. Open `tasks/phase-<NN>-*.tasks.md`:
   - **Claim** a task: fill in `Assignee` (git name) + change `Status` → `in_progress`.
   - Create a branch per `rules/01-git-workflow.md`.
4. Follow the task's **sub-checklist**; tick `[x]` as each item is completed.
5. Commit following Conventional Commits, including the `Task:` trailer to link the task.
6. When finished: change `Status` → `done`, fill in `Commits` + `PR`, and update `progress/PROGRESS.md`.
7. Only move to the next phase once the spec's **Acceptance Criteria** are met.

---

## Who did what? (git account / assigner)

- Each task has an **`Assignee`** field (an identity in `progress/assignees.yaml`).
- Each commit must link to a task via the `Task: PH<NN>-T<n>` trailer.
- To see who did what:

```bash
# History per person
git shortlog -sne

# Commits for a specific task
git log --grep="Task: PH01-T3" --pretty="%h %an <%ae> %s"

# Who last modified a file
git blame <path>
```
