---
phase: "02"
slug: rag-vectordb
title: "Multimodal RAG on a Released/Immutable corpus"
status: todo
depends_on: ["01"]
source_prompt: "prompts/phase-02-rag-vectordb/prompt.md"
---

# Phase 02 — Multimodal RAG (SPEC)

## Context
The backend core already has auth/RBAC/repositories + mock chat. Build the core purpose: multimodal search over a released/immutable document corpus — text, PDF, images, Excel — answering with citations.
> Reference: `docs/03-document-search-strategy.md`.

## Objective
A multimodal RAG flow: ingestion → embeddings → Vector DB (version + metadata) → hybrid retrieve + rerank → answers with multimodal citations. Immutable corpus (versioned, hash).

## Scope
- **In:** immutable doc model (version/hash), multimodal ingestion (PDF text+scan/OCR, images+vision, Excel), embeddings, vector store with metadata filtering, hybrid search + rerank, RAG chain, multimodal citations.
- **Out:** function calling/SQL (Phase 3), voice (Phase 4).

## Deliverables
- Multimodal loaders + OCR + vision + excel.
- Vector store with metadata/version filtering, hybrid retriever + rerank.
- Ingest endpoint (ADMIN, versioned) + chat using RAG.
- Tests with a sample document set of PDF/images/Excel.

## Acceptance Criteria
- [ ] Ingest PDF, images, Excel → create vectors + version/hash metadata.
- [ ] Ask about content in an image/diagram → answer + citation (bbox/caption).
- [ ] Ask about figures in Excel → answer + citation (sheet/cell_range).
- [ ] Filter by version accurately.
- [ ] Hybrid search + rerank works; out-of-scope questions → no fabrication.
- [ ] Switching `VECTOR_DB_PROVIDER` requires no changes to the chain code.

## Guardrails
- Immutable store: version + `content_hash` mandatory.
- Citations mandatory, accurate to page/sheet/cell/image region.
- OCR/vision attaches confidence.
- Embeddings/LLM/OCR prefer Azure, with retry.
- Do not log sensitive document content at info level.

## Links
- Tasks: `.agent/tasks/phase-02-rag-vectordb.tasks.md`
- Rules: `.agent/rules/00-global.md`, `.agent/rules/04-security-guardrails.md`
