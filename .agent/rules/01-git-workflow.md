# Rule 01 — Git Workflow & Assignee Tracing

> Goal: always know **which git account did which task**, automatically and verifiably.

## 1. Git identity (mandatory)
- Each person/agent must configure the correct `user.name` and `user.email` (see `progress/assignees.yaml`).

```bash
git config user.name "Stephen Sang"
git config user.email "nguyentuanquangsang1999@gmail.com"
```

- This identity = the value of the `Assignee` field in `.tasks.md` files (use the short `id` from assignees.yaml).

## 2. Branch convention
```
<type>/PH<NN>-T<n>-<slug>
```
- `type`: `feat | fix | chore | docs | test | refactor | infra`
- Examples: `feat/PH01-T3-repository-pattern`, `infra/PH07-T3-terraform-vnet`
- One branch = one task (or a tightly related group of sub-checklist items).

## 3. Conventional Commits + Task trailer (MANDATORY)
```
<type>(<scope>): <short description>

<optional commit body>

Task: PH<NN>-T<n>
```
Example:
```
feat(backend): add UserRepository and ConversationRepository

Move all DB queries into the repository layer; routers do not call Prisma directly.

Task: PH01-T3
```

- The `Task:` trailer is **mandatory** to link commit ↔ task ↔ assignee.
- Each commit should correspond to 1+ completed sub-checklist items.

## 4. Pull Request
- PR title: `[PH<NN>] <title>` (e.g. `[PH01] Backend core & RBAC`).
- The PR description must list the completed `Task:` items + reference the spec.
- A PR is only merged when the spec's **Acceptance Criteria** are fully ticked.

## 5. Status updates on commit
Whenever you push progress, update in the `.tasks.md` file:
- `Status`: `todo → in_progress → review → done` (or `blocked`).
- `Commits`: add the short hash.
- `PR`: link/PR number when opened.

## 6. Commands to trace "who did what"
```bash
git shortlog -sne                                   # summary per person
git log --grep="Task: PH02-T5" --pretty="%h %an %s" # commits by task
git log --author="nguyentuanquangsang1999" --oneline
git blame <path>                                    # who last edited which line
```

## 7. Safety
- Do NOT commit the real `.env` (only `.env.example`).
- Do NOT `push --force` to `main`.
- Do NOT modify another person's `git config`.
