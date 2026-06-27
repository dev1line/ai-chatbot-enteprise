# Phase 2 — Multimodal RAG trên kho tài liệu Released/Immutable

## Context
Backend core (Phase 1) đã có auth/RBAC/repositories và chat endpoint mock. Giờ xây **mục đích cốt lõi** của hệ thống: tìm kiếm **đa phương thức (multimodal)** trên **kho tài liệu đã released/bất biến** — text, PDF, hình ảnh, Excel — và trả lời kèm **citations** chính xác.

> Tham khảo bắt buộc: `docs/03-document-search-strategy.md`.

## Objective
Xây luồng RAG multimodal: ingestion text/PDF/ảnh/Excel → embeddings → Vector DB (có version & metadata) → hybrid retrieve + rerank → trả lời kèm citation đa phương thức. Đảm bảo kho **immutable** (versioned, hash).

## Scope
**In:** immutable doc model (version/hash), ingestion multimodal (PDF text+scan/OCR, hình ảnh+vision, Excel/CSV bảng), embeddings, vector store có metadata filter, hybrid search + rerank, RAG chain, citations đa phương thức.
**Out:** function calling/SQL (Phase 3), voice (Phase 4).

## Tasks
1. **Immutable corpus model**: mở rộng `Document` (Phase 1) với `version`, `released_at`, `content_hash`, `type`. Ingest chỉ qua quy trình release; bản mới = version mới (không sửa tại chỗ).
2. **Ingestion multimodal** (`app/rag/ingestion/`):
   - `text_loader` (MD/TXT), `pdf_loader` (layout-aware, vd PyMuPDF/`unstructured`).
   - `pdf_scan_loader` + **OCR** (Tesseract / Azure Document Intelligence) cho PDF scan, gắn confidence.
   - `image_loader`: **vision model** mô tả ảnh + OCR text trong ảnh; lưu caption + (tuỳ chọn) image embedding (CLIP-class).
   - `excel_loader`: trích bảng có cấu trúc (`openpyxl`/`pandas`), giữ `sheet` + `cell_range`, chuyển vùng bảng thành text mô tả + giá trị.
   - Mỗi chunk gắn metadata trích dẫn (xem docs/03 mục 2).
3. **Embeddings** (`app/rag/embeddings.py`): Azure `text-embedding-ada-002` cho text/bảng/caption; có retry. (Tuỳ chọn) vision embeddings cho ảnh.
4. **Vector store** (`app/rag/vector_store.py`): abstraction `pinecone`/`milvus`; hỗ trợ **metadata filter** (`doc_id, version, type, project`) + namespace theo version.
5. **Hybrid search + rerank** (`app/rag/retriever.py`): kết hợp dense (embeddings) + sparse/BM25; rerank top-k bằng cross-encoder.
6. **Ingestion endpoint** (`POST /api/admin/ingest`, ADMIN): nạp tài liệu (đa định dạng) → Vector DB + lưu metadata + version/hash vào Postgres.
7. **RAG chain** (`app/orchestration/rag_chain.py`): embed query → (filter version nếu chỉ định) → hybrid retrieve + rerank → prompt context + question → Azure OpenAI → answer.
8. **Citations đa phương thức**: trả `answer` + `citations[]` với `type` (text/pdf/image/excel) và toạ độ nguồn (page/bbox/sheet/cell_range). Không đủ context → trả lời an toàn (không bịa).
9. Tích hợp RAG chain vào `POST /api/chat` (thay mock Phase 1). Hỗ trợ filter theo version trong request.

## Deliverables
- Loaders multimodal + OCR + vision + excel.
- Vector store có metadata/version filter, hybrid retriever + rerank.
- Endpoint ingest (ADMIN, versioned) + chat dùng RAG multimodal.
- Test với bộ tài liệu mẫu gồm PDF, ảnh, Excel.

## Acceptance Criteria
- [ ] Ingest tài liệu **PDF, ảnh, Excel** → tạo vectors + metadata version/hash.
- [ ] Hỏi nội dung nằm trong **ảnh/diagram** → trả lời + citation (bbox/caption).
- [ ] Hỏi số liệu trong **Excel** → trả lời + citation (sheet/cell_range).
- [ ] Lọc theo **version** chính xác (chỉ tìm trong release chỉ định).
- [ ] Hybrid search + rerank hoạt động; câu ngoài phạm vi → không bịa.
- [ ] Đổi `VECTOR_DB_PROVIDER` không phải sửa code chain.

## Guardrails
- Kho tài liệu **immutable**: không sửa tại chỗ; version + `content_hash` bắt buộc.
- Citations là **bắt buộc** và phải đúng tới page/sheet/cell/vùng ảnh.
- OCR/vision gắn confidence; đánh dấu nguồn rủi ro thấp.
- Embeddings/LLM/OCR ưu tiên dịch vụ trong Azure (compliance), có retry.
- Không log nội dung tài liệu nhạy cảm ở mức info.
