# Rule 00 — Core principles (MANDATORY)

> Every agent/human working on this repo MUST read and follow these before coding.

## 1. Zero Data Leak
- Never send enterprise data to unapproved public services.
- Prefer Azure-hosted services for LLM/Embeddings/OCR (compliance, no-train).
- Do not log sensitive data at `info` level (PII, document content, secrets, tokens, passwords).

## 2. LOCAL-FIRST / DOCKER-FIRST
- Phases 0–6: all dev & test must run **locally via Docker Compose**, with NO dependency on Azure.
- Azure infrastructure is only deployed in **Phase 7**, after functionality is stable locally.
- Switch environments only by changing a **flag/provider** (`APP_ENV`, `LLM_PROVIDER`, `SECRETS_PROVIDER`, …),
  do NOT rewrite business logic.

## 3. Provider swappable
- Every provider (LLM, Vector DB, OCR, STT, TTS, Secrets) must sit behind an abstraction.
- Switching providers via ENV must not require changing business code.

## 4. Layered security
- RBAC is mandatory at the tool layer (to prevent the LLM "hallucinating" permissions).
- The SQL tool is **SELECT-only**, using a read-only DB role.
- Least privilege at every layer (DB, network, identity).

## 5. Documentation & source citations
- Every RAG answer must include accurate **citations** (page/sheet/cell/bbox).
- The document store is **immutable**: versioned + `content_hash`, never edited in place.

## 6. Quality
- No hardcoded secrets; all config via env / Key Vault.
- Pin dependency versions.
- Add tests for what you add; do not break existing tests.
- Follow the structure in `docs/01-architecture.md`.

## 7. Specification source references
- `prompts/phase-*/prompt.md` is the origin; `.agent/specs/*` is the normalized version used to track progress.
- When the prompt and spec diverge → update the spec and note the reason in the PR.
