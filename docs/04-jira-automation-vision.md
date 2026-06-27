# 04 — Vision: AI Agent for Requirement Analysis & JIRA Automation

> Long-term direction: an AI Agent system that supports **BAs (Business Analysts)** in analyzing customer requirement documents, creating tasks in **JIRA**, and managing **Change Requests**.

## 1. Objectives

- Reduce the BA's manual effort in reading/breaking down requirements.
- Standardize backlog creation (epic → story → task → sub-task) in JIRA.
- Track & manage **change requests** based on the released (immutable) document corpus.
- Always keep a **human-in-the-loop**: the agent proposes, a reviewer approves before anything is written.

## 2. Business Flow (high-level)

```
[Customer requirement document]  (PDF/Word/Excel/image — multi-format)
        │  (uses the multimodal pipeline in docs/03)
        ▼
[Requirement Analyzer Agent]
   - Extract requirements, constraints, acceptance criteria
   - Detect ambiguity / missing information → ask the BA questions
        ▼
[Work Breakdown Agent]
   - Break down Epic → Story → Task → Sub-task
   - Attach estimate, priority, acceptance criteria, labels
        ▼
[BA Review (human-in-the-loop)]  ← MANDATORY review/edit
        ▼
[JIRA Sync Agent]
   - Create/update issues via the JIRA REST API
   - Map fields (project, issuetype, epic link, components)
        ▼
[Change Request Manager]
   - Compare new requirements vs. the released (immutable corpus)
   - List changes, assess impact, propose issue updates
```

## 3. Proposed Agents (extending Multi-Agent in Phase 8)

| Agent | Responsibility |
|---|---|
| **Requirement Analyzer** | Read multi-format documents, extract structured requirements, detect gaps/contradictions |
| **Work Breakdown** | Convert requirements → backlog (epic/story/task), estimate, acceptance criteria |
| **JIRA Sync** | Create/update issues via API, idempotent (avoid duplicates), dry-run first |
| **Change Request Manager** | Diff requirements vs. released docs, impact analysis, propose changes |

## 4. JIRA Integration

- **API**: JIRA Cloud REST API v3 (or Data Center) via token/OAuth.
- **Idempotency**: attach an external key (e.g. requirement id) to avoid creating duplicate issues.
- **Configurable field mapping**: project key, issue type, epic link, components, labels, custom fields.
- **Dry-run mode**: print the list of operations to be performed before writing for real.
- **Audit**: log every JIRA write operation (who approved, payload, result).

## 5. Change Request Management

- Leverage the **immutable** corpus (docs/03): each release has a version + hash.
- When a new requirement/document arrives → perform a **semantic diff** against the most recent released version.
- Output: a list of changes (added/modified/removed), impact (related module/issue), and proposals to create/update change-request issues.

## 6. Guardrails & Risks

- **Mandatory human-in-the-loop** before writing to JIRA (no uncontrolled auto-create).
- **Idempotent + dry-run** to avoid spamming/duplicating issues.
- **RBAC**: only authorized roles may sync to JIRA.
- **Security**: JIRA token in Key Vault; never log secrets; respect Zero Data Leak.
- **Source traceability**: every proposed task must reference the original requirement excerpt (citation).

## 7. Dependencies

- Requires **Phase 2 (multimodal)** to read multi-format requirement documents.
- Requires **Phase 8 (multi-agent)** as the orchestration framework.
- Detailed implementation: see `prompts/phase-09-jira-requirement-agent/prompt.md`.
