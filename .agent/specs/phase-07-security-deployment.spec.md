---
phase: "07"
slug: security-deployment
title: "Security & Deployment"
status: todo
depends_on: ["06"]
source_prompt: "prompts/phase-07-security-deployment/prompt.md"
---

# Phase 07 — Security & Deployment (SPEC)

## Context
The system is feature-complete + tested and runs stably locally via Docker. This is the infrastructure deployment phase — only done AFTER development is finished. Security hardening (Zero Data Leak) + Azure deployment.
> Switch environments by changing the `APP_ENV=staging|prod` flag + `SECRETS_PROVIDER=azure_key_vault`, do NOT change logic.

## Objective
Ensure Zero Data Leak (Private Link/VNet), secret management, observability, and a deployment pipeline — upgraded from the local-docker version by changing flags/providers.

## Scope
- **In:** Azure Private Link/VNet, Key Vault, IaC (Terraform), observability, deployment, hardening.
- **Out:** adding new features.

## Deliverables
- Terraform infra (VNet + Private Link + Key Vault + DB).
- Observability (logs/metrics/traces) + alerts.
- CD pipeline + runbook.

## Acceptance Criteria
- [ ] Azure OpenAI is accessed only via a private endpoint (not public).
- [ ] No secret resides in code/repo; all are in Key Vault.
- [ ] Latency & time-to-resolution metrics are shown on a dashboard.
- [ ] The SQL tool uses a read-only DB role.
- [ ] Deploying staging/prod runs migrations automatically, with rollback.

## Guardrails
- Only deploy after development is finished (Phases 0–6 stable on local-docker).
- Switch environments via flags/providers, do NOT rewrite logic.
- Zero Data Leak: no public endpoint for the LLM/internal data.
- Least privilege at every layer; every infrastructure change via IaC.

## Links
- Tasks: `.agent/tasks/phase-07-security-deployment.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
