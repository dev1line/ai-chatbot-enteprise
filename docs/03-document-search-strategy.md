# 03 — Chiến lược tìm kiếm tài liệu Multimodal trên kho Released/Immutable

> Đây là **mục đích cốt lõi** của hệ thống: tìm kiếm chính xác, đầy đủ trên kho tài liệu đã release (bất biến), bao gồm text, hình ảnh, PDF, Excel.

## 1. Nguyên tắc kho tài liệu Immutable

- Tài liệu **đã release thì không thay đổi**: mỗi tài liệu có `doc_id` + `version` + `released_at` + `content_hash` (checksum).
- Chỉ nạp (ingest) qua **quy trình release có kiểm soát** (admin/CI), không sửa tại chỗ.
- Khi có bản mới → tạo **version mới**, giữ nguyên bản cũ (audit/so sánh change request).
- Mọi citation truy ngược chính xác tới version cụ thể.

## 2. Loại định dạng & cách xử lý (ingestion multimodal)

| Định dạng | Cách trích xuất | Metadata trích dẫn |
|---|---|---|
| **Text / Markdown** | Parse trực tiếp, chunk theo heading | `doc_id, version, section` |
| **PDF (text)** | Parser layout-aware (vd `unstructured`, PyMuPDF), giữ thứ tự đọc | `doc_id, version, page` |
| **PDF (scan/ảnh)** | **OCR** (Tesseract) hoặc **Vision model** → text; gắn confidence | `doc_id, version, page, bbox` |
| **Hình ảnh** (PNG/JPG: diagram, screenshot) | **Vision model** mô tả + OCR text trong ảnh; lưu caption + embedding ảnh | `doc_id, image_id, region/bbox` |
| **Excel / CSV** | Trích xuất bảng có cấu trúc (pandas/openpyxl); chuyển mỗi vùng/bảng thành text mô tả + giữ giá trị | `doc_id, sheet, cell_range` |
| **Word / PPT** (mở rộng) | `unstructured` → text + ảnh nhúng | `doc_id, slide/section` |

## 3. Chiến lược index & retrieval

- **Hybrid search**: kết hợp **dense** (embeddings ngữ nghĩa) + **sparse/keyword** (BM25) để bắt cả ý nghĩa lẫn từ khoá chính xác (mã lỗi, tên field).
- **Multimodal embeddings**:
  - Text/bảng → text embeddings (Azure ada-002).
  - Hình ảnh → vision embeddings (CLIP-class) **và/hoặc** mô tả ảnh bằng vision model rồi embed text mô tả.
- **Metadata filtering**: lọc theo `doc_id, version, released_at, type, project` (vd "chỉ tìm trong release v2.1").
- **Reranking**: rerank top-k bằng cross-encoder để tăng precision trước khi đưa vào LLM.
- **Chunking thông minh**: theo cấu trúc (heading, bảng, vùng ảnh), giữ context cha-con.

## 4. Citation đa phương thức (bắt buộc)

Mỗi câu trả lời phải kèm trích dẫn đủ để người dùng kiểm chứng:
```json
{
  "answer": "...",
  "citations": [
    {"type": "pdf",   "doc_id": "ARCH-001", "version": "v2.1", "page": 12, "snippet": "..."},
    {"type": "image", "doc_id": "DIAG-009", "version": "v2.1", "bbox": [x,y,w,h], "caption": "Sơ đồ luồng thanh toán"},
    {"type": "excel", "doc_id": "BENCH-Q2", "version": "v1.0", "sheet": "throughput", "cell_range": "B2:D10"}
  ]
}
```

## 5. Công cụ đề xuất

- **Ingestion/parsing**: `unstructured`, `PyMuPDF`/`pdfplumber`, `openpyxl`/`pandas`.
- **OCR**: Tesseract / Azure AI Document Intelligence (compliance).
- **Vision**: Azure OpenAI vision / CLIP-class embeddings.
- **Vector DB**: Pinecone/Milvus (hỗ trợ metadata filter + namespace theo version).
- **Hybrid/rerank**: BM25 (Elastic/pg) + cross-encoder reranker.

## 6. Acceptance (chất lượng tìm kiếm)

- Tìm được nội dung nằm trong **ảnh/diagram** và **bảng Excel**, không chỉ text.
- Lọc theo **version** chính xác (immutable corpus).
- Citation chỉ đúng tới page/sheet/cell/vùng ảnh.
- Đánh giá retrieval bằng metric (recall@k, precision@k) trên bộ test đa phương thức.
