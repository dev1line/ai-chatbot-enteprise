---
phase: "07"
slug: security-deployment
spec: ".agent/specs/phase-07-security-deployment.spec.md"
---

# Phase 07 — Security & Deployment (TASKS)

> Rules: `.agent/rules/04-security-guardrails.md` — Zero Data Leak, IaC-only, least privilege.
> Only do this AFTER Phases 0–6 run stably on local-docker.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T0 | Prerequisite: confirm the stack is stable locally | - | todo | - |
| T1 | Network / Private Link | - | todo | - |
| T2 | Secrets → Key Vault | - | todo | - |
| T3 | IaC (Terraform) | - | todo | - |
| T4 | Vector DB compliance | - | todo | - |
| T5 | Observability | - | todo | - |
| T6 | Hardening | - | todo | - |
| T7 | Deploy pipeline | - | todo | - |
| T8 | Runbook | - | todo | - |

---

### T0 — Prerequisite: confirm the stack is stable locally
- **Assignee:** -
- **Status:** todo
- **Branch:** `chore/PH07-T0-preflight`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Confirm Phases 0–6 run stably locally via Docker
- [ ] Keep the ability to run locally intact (only add an infra layer + change flags)
- [ ] Commit with the `Task: PH07-T0` trailer

**Notes:**

### T1 — Network / Private Link
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T1-private-link`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Azure OpenAI via Private Endpoint/Private Link within the VNet
- [ ] Backend does not call public endpoints
- [ ] Document the no-train commitment (compliance)
- [ ] Commit with the `Task: PH07-T1` trailer

**Notes:**

### T2 — Secrets → Key Vault
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T2-key-vault`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Move all secrets to Azure Key Vault
- [ ] The app reads via managed identity
- [ ] Remove secrets from the prod env file
- [ ] Commit with the `Task: PH07-T2` trailer

**Notes:**

### T3 — IaC (Terraform)
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T3-terraform`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `infra/terraform/`: VNet, subnet, private endpoint
- [ ] Postgres, Key Vault
- [ ] Container apps/AKS
- [ ] No manual clicking in the portal
- [ ] Commit with the `Task: PH07-T3` trailer

**Notes:**

### T4 — Vector DB compliance
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T4-vectordb`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] If on-prem → self-host Milvus within the VNet
- [ ] If Pinecone → assess compliance/region
- [ ] Commit with the `Task: PH07-T4` trailer

**Notes:**

### T5 — Observability
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T5-observability`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Centralized structured logs
- [ ] Tracing (request → docs → tool calls → latency)
- [ ] Metrics (Time-to-resolution, API latency P95)
- [ ] Dashboard + alert
- [ ] Commit with the `Task: PH07-T5` trailer

**Notes:**

### T6 — Hardening
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T6-hardening`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] HTTPS/TLS + security headers
- [ ] Rate limiting + input validation
- [ ] Dependency scan
- [ ] Least-privilege DB role (read-only for the SQL tool)
- [ ] Commit with the `Task: PH07-T6` trailer

**Notes:**

### T7 — Deploy pipeline
- **Assignee:** -
- **Status:** todo
- **Branch:** `infra/PH07-T7-deploy`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Build image
- [ ] Automatic Prisma migration
- [ ] Blue/green or rolling
- [ ] `staging` & `prod` environments
- [ ] Commit with the `Task: PH07-T7` trailer

**Notes:**

### T8 — Runbook
- **Assignee:** -
- **Status:** todo
- **Branch:** `docs/PH07-T8-runbook`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Operations documentation
- [ ] Rollback procedure
- [ ] Commit with the `Task: PH07-T8` trailer

**Notes:**
