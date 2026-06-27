# 03 — Multimodal Document Search Strategy over the Released/Immutable Corpus

> This is the **core purpose** of the system: accurate, complete search over the corpus of released (immutable) documents, including text, images, PDF, and Excel.

## 1. Immutable Document Corpus Principles

- **Released documents do not change**: each document has a `doc_id` + `version` + `released_at` + `content_hash` (checksum).
- Ingest only through a **controlled release process** (admin/CI), no in-place edits.
- When a new version is available → create a **new version**, keeping the old one intact (for audit/change-request comparison).
- Every citation traces back precisely to a specific version.

## 2. Formats & Handling (multimodal ingestion)

| Format | Extraction Method | Citation Metadata |
|---|---|---|
| **Text / Markdown** | Parse directly, chunk by heading | `doc_id, version, section` |
| **PDF (text)** | Layout-aware parser (e.g. `unstructured`, PyMuPDF), preserve reading order | `doc_id, version, page` |
| **PDF (scan/image)** | **OCR** (Tesseract) or a **Vision model** → text; attach confidence | `doc_id, version, page, bbox` |
| **Images** (PNG/JPG: diagrams, screenshots) | **Vision model** description + OCR of text in the image; store caption + image embedding | `doc_id, image_id, region/bbox` |
| **Excel / CSV** | Extract structured tables (pandas/openpyxl); convert each region/table into descriptive text + preserve values | `doc_id, sheet, cell_range` |
| **Word / PPT** (extension) | `unstructured` → text + embedded images | `doc_id, slide/section` |

## 3. Index & Retrieval Strategy

- **Hybrid search**: combine **dense** (semantic embeddings) + **sparse/keyword** (BM25) to capture both meaning and exact keywords (error codes, field names).
- **Multimodal embeddings**:
  - Text/tables → text embeddings (Azure ada-002).
  - Images → vision embeddings (CLIP-class) **and/or** describe the image with a vision model and then embed the descriptive text.
- **Metadata filtering**: filter by `doc_id, version, released_at, type, project` (e.g. "search only within release v2.1").
- **Reranking**: rerank top-k with a cross-encoder to improve precision before passing to the LLM.
- **Smart chunking**: by structure (heading, table, image region), preserving parent-child context.

## 4. Multimodal Citations (mandatory)

Every answer must include citations sufficient for the user to verify:
```json
{
  "answer": "...",
  "citations": [
    {"type": "pdf",   "doc_id": "ARCH-001", "version": "v2.1", "page": 12, "snippet": "..."},
    {"type": "image", "doc_id": "DIAG-009", "version": "v2.1", "bbox": [x,y,w,h], "caption": "Payment flow diagram"},
    {"type": "excel", "doc_id": "BENCH-Q2", "version": "v1.0", "sheet": "throughput", "cell_range": "B2:D10"}
  ]
}
```

## 5. Recommended Tools

- **Ingestion/parsing**: `unstructured`, `PyMuPDF`/`pdfplumber`, `openpyxl`/`pandas`.
- **OCR**: Tesseract / Azure AI Document Intelligence (compliance).
- **Vision**: Azure OpenAI vision / CLIP-class embeddings.
- **Vector DB**: Pinecone/Milvus (support metadata filtering + namespace by version).
- **Hybrid/rerank**: BM25 (Elastic/pg) + cross-encoder reranker.

## 6. Acceptance (search quality)

- Find content located inside **images/diagrams** and **Excel tables**, not just text.
- Filter by **version** accurately (immutable corpus).
- Citations point exactly to the page/sheet/cell/image region.
- Evaluate retrieval with metrics (recall@k, precision@k) on a multimodal test set.
