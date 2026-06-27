# Rule 04 — Security Guardrails (MANDATORY, must not be skipped)

> These are hard safety constraints. Any task that violates them will be rejected from merge.

## Secrets
- Do not hardcode secrets/tokens/passwords in code or commits.
- Only commit `.env.example`; real secrets via local env or Azure Key Vault (Phase 7).
- Do not log secrets/tokens/PII.

## RBAC & Tools
- RBAC is checked at the **tool layer** before `run()`; do not trust the LLM to decide permissions.
- Each tool has a `validate()` that runs before `run()`.
- Audit log every tool call: user, tool, params, result summary, latency.

## SQL Tool
- **`SELECT` only.** Block `DROP/DELETE/UPDATE/INSERT/ALTER`, block multi-statements (`;`), block comment injection.
- Run via a dedicated **read-only** connection/role for the tool.
- Security tests for SQL are a **must-have** (Phase 6).

## Network & Compliance (Phase 7)
- Azure OpenAI is accessed **only** via Private Endpoint/Private Link within the VNet, not public.
- Every infrastructure change goes through IaC (Terraform), no manual clicking in the portal.

## RAG / Documents
- Immutable store: version + `content_hash`; never edited in place.
- Citations are mandatory; do not fabricate when context is missing (answer safely).
- OCR/vision attaches confidence; flag low-confidence sources as risky.

## JIRA / Write actions (Phase 9)
- **Human-in-the-loop is mandatory** before writing to JIRA.
- **Idempotent + dry-run** to avoid duplicates/spam.
- JIRA token in Key Vault; every write action is audit-logged.

## Fallback
- LLM/STT/TTS error → standard fallback message, no crash, no exposure of internal error details.
