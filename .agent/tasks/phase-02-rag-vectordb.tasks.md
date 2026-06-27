---
phase: "02"
slug: rag-vectordb
spec: ".agent/specs/phase-02-rag-vectordb.spec.md"
---

# Phase 02 — Multimodal RAG (TASKS)

> Rules: `.agent/rules/03-task-management.md` + `.agent/rules/04-security-guardrails.md`.

## Overview table
| Task | Description | Assignee | Status | PR |
|------|-------|----------|--------|----|
| T1 | Immutable corpus model | - | todo | - |
| T2 | Multimodal ingestion (loaders) | - | todo | - |
| T3 | Embeddings | - | todo | - |
| T4 | Vector store (metadata filter) | - | todo | - |
| T5 | Hybrid search + rerank | - | todo | - |
| T6 | Ingestion endpoint (ADMIN) | - | todo | - |
| T7 | RAG chain | - | todo | - |
| T8 | Multimodal citations | - | todo | - |
| T9 | Integrate RAG into /api/chat | - | todo | - |

---

### T1 — Immutable corpus model
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T1-immutable-model`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Extend `Document` with `version`, `released_at`, `content_hash`, `type`
- [ ] Ingest only via the release process (a new version = a new release)
- [ ] No in-place editing (immutable)
- [ ] Commit with the `Task: PH02-T1` trailer

**Notes:**

### T2 — Multimodal ingestion (loaders)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T2-loaders`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `text_loader` (MD/TXT)
- [ ] `pdf_loader` (layout-aware, PyMuPDF/unstructured)
- [ ] `pdf_scan_loader` + OCR (Tesseract/Azure DI) with confidence
- [ ] `image_loader`: vision model describes the image + OCR + caption (optional image embedding)
- [ ] `excel_loader`: extract tables (openpyxl/pandas), keep `sheet` + `cell_range`
- [ ] Each chunk carries citation metadata
- [ ] Commit with the `Task: PH02-T2` trailer

**Notes:**

### T3 — Embeddings
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T3-embeddings`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/rag/embeddings.py`: Azure `text-embedding-ada-002` for text/tables/captions
- [ ] With retry (tenacity)
- [ ] (Optional) vision embeddings for images
- [ ] Commit with the `Task: PH02-T3` trailer

**Notes:**

### T4 — Vector store (metadata filter)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T4-vector-store`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/rag/vector_store.py` abstraction (pinecone/milvus)
- [ ] Metadata filter (`doc_id, version, type, project`)
- [ ] Namespace by version
- [ ] Switching `VECTOR_DB_PROVIDER` requires no changes to the chain code
- [ ] Commit with the `Task: PH02-T4` trailer

**Notes:**

### T5 — Hybrid search + rerank
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T5-hybrid-rerank`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/rag/retriever.py`: combine dense + sparse/BM25
- [ ] Rerank top-k with a cross-encoder
- [ ] Out-of-scope questions → no fabrication
- [ ] Commit with the `Task: PH02-T5` trailer

**Notes:**

### T6 — Ingestion endpoint (ADMIN)
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T6-ingest-endpoint`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `POST /api/admin/ingest` (RBAC ADMIN)
- [ ] Load multiple formats → Vector DB
- [ ] Store metadata + version/hash in Postgres
- [ ] Commit with the `Task: PH02-T6` trailer

**Notes:**

### T7 — RAG chain
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T7-rag-chain`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] `app/orchestration/rag_chain.py`: embed query → filter version → retrieve + rerank
- [ ] Prompt context + question → Azure OpenAI → answer
- [ ] Commit with the `Task: PH02-T7` trailer

**Notes:**

### T8 — Multimodal citations
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T8-citations`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Return `answer` + `citations[]` with `type` (text/pdf/image/excel)
- [ ] Source coordinates (page/bbox/sheet/cell_range)
- [ ] Missing context → answer safely (no fabrication)
- [ ] Commit with the `Task: PH02-T8` trailer

**Notes:**

### T9 — Integrate RAG into /api/chat
- **Assignee:** -
- **Status:** todo
- **Branch:** `feat/PH02-T9-chat-integration`
- **Commits:** -
- **PR:** -

**Sub-checklist:**
- [ ] Replace the Phase 1 mock with the RAG chain
- [ ] Support version filtering in the request
- [ ] Test with a sample document set (PDF, images, Excel)
- [ ] Commit with the `Task: PH02-T9` trailer

**Notes:**
