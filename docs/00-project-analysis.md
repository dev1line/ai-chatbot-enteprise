# 00 — Phân tích dự án (Project Analysis)

## 1. Bối cảnh & vấn đề

Doanh nghiệp (đặc biệt mô hình **ODC**) có:
- Khối lượng lớn tài liệu nghiệp vụ, runbook, policy bảo mật thay đổi liên tục.
- Kỹ sư tốn nhiều thời gian tra cứu thủ công → chậm phản ứng sự cố, giảm năng suất vận hành.
- Yêu cầu bảo mật cao: **Zero Data Leak** — không để dữ liệu nội bộ rò rỉ ra dịch vụ public.

## 2. Phân tích theo STAR

### Situation
Tra cứu thủ công chậm, kiến thức phân mảnh trong nhiều hệ thống (wiki, PDF, DB, monitoring).

### Task
Trợ lý AI nội bộ:
- Tra cứu tài liệu (RAG) + **thực thi hành động** (gọi API, query DB).
- Hỗ trợ cả **text** và **voice**.
- Bảo mật tuyệt đối.

### Action (đề xuất kỹ thuật)
- Backend Python + FastAPI, tách tầng rõ ràng (Repository Pattern).
- Azure OpenAI làm LLM (compliance-friendly, private VNet).
- RAG: nạp tài liệu → Vector DB; LangChain điều phối luồng.
- Function Calling: cho LLM truy cập DB báo cáo / internal API có kiểm soát.
- STT/TTS bằng mã nguồn mở (Whisper, HuggingFace) để tối ưu chi phí.

### Result (KPI mục tiêu)
| Metric | Mục tiêu |
|---|---|
| Thời gian tra cứu | Giảm ~80% |
| Time-to-resolution sự cố | Giảm rõ rệt |
| API latency (P95) | < 2s (text), streaming cho voice |
| RAG faithfulness (Ragas) | > 0.85 |
| Tỷ lệ "ảo giác" (hallucination) | Đo & giảm tối thiểu |

## 3. Điểm đột phá — "Actionable RAG"

RAG truyền thống chỉ **đọc** tài liệu. Dự án này thêm khả năng **hành động**:
- Sinh & thực thi SQL (Text-to-SQL) có sandbox + chỉ `SELECT`.
- Gọi internal API (check container/server, KMS, WAF…).
- Mô hình lai (Hybrid): Azure OpenAI cho reasoning, HuggingFace cho TTS để tiết kiệm.

## 3b. Mục đích chính (cập nhật) — Tìm kiếm tài liệu Released đa phương thức

Trọng tâm cốt lõi của hệ thống là **tìm kiếm chính xác trên kho tài liệu đã RELEASED / BẤT BIẾN** (immutable, versioned):
- Tài liệu đã release **không thay đổi** → đảm bảo nguồn tra cứu ổn định, có version, có thể audit.
- **Đa phương thức (Multimodal)**: index & tìm kiếm đầy đủ trên **hình ảnh** (sơ đồ, screenshot, diagram), **PDF** (kể cả scan), **Excel/CSV** (bảng số liệu), không chỉ text/markdown.
- Mục tiêu: tra cứu "đầy đủ hơn" — câu trả lời tổng hợp được từ nhiều loại định dạng + trích dẫn đúng nguồn (file, trang, sheet/cell, vùng ảnh).

> Đây là nền tảng cho mọi tính năng phía trên: chất lượng tìm kiếm multimodal quyết định chất lượng trả lời và độ tin cậy.

## 3c. Tầm nhìn xa — AI Agent tự động hoá phân tích Requirement & JIRA

Hướng phát triển dài hạn: hệ thống **AI Agent** hỗ trợ **BA (Business Analyst)** và **quản lý Change Request**:
- Tự động **phân tích tài liệu requirement** của khách hàng (SRS, BRD, email, spec, file đính kèm đa định dạng).
- Bóc tách thành **user stories / tasks / sub-tasks**, ước lượng, gắn acceptance criteria.
- **Tạo & cập nhật task trên JIRA** tự động (qua Atlassian/JIRA API) với human-in-the-loop xác nhận.
- Phát hiện & quản lý **Change Request**: so sánh requirement mới vs đã release (dùng kho immutable ở mục 3b), highlight thay đổi, đánh giá impact, đề xuất cập nhật backlog.

## 4. Use Cases chi tiết

1. **Multimodal Document Search (cốt lõi)**
   - "Sơ đồ kiến trúc module thanh toán bản release v2.1 nằm ở đâu?" → tìm trong hình ảnh/PDF → trả lời + trích dẫn (file, trang, vùng ảnh).
   - "Số liệu throughput trong file benchmark Q2.xlsx là bao nhiêu?" → đọc bảng Excel → trả lời + trích dẫn (sheet, cell range).
2. **Ops/Security Bot**
   - "Trạng thái container payment-service hiện tại?" → gọi API → trả lời.
   - "Policy về KMS key rotation là gì?" → RAG + citation.
3. **Text-to-SQL Report Bot**
   - "Doanh thu tuần này theo từng dự án?" → sinh SQL → query PostgreSQL → đọc kết quả (voice).
4. **BA / Requirement Automation (tầm nhìn)**
   - Upload tài liệu requirement khách hàng → agent phân tích → đề xuất danh sách task → BA duyệt → tạo trên JIRA.
   - "So với bản release trước, requirement này thay đổi gì?" → so sánh với kho immutable → liệt kê change request + impact.

## 5. Rủi ro & Giải pháp

| Rủi ro | Giải pháp |
|---|---|
| Data leak qua public LLM | Azure OpenAI private VNet + Private Link, no-train policy |
| SQL injection / lệnh phá hoại (DROP/DELETE) | Whitelist `SELECT`, parameterized, schema-aware validation, unit test chặt |
| Hallucination | Citations bắt buộc, Ragas/TruLens đánh giá, guardrails |
| Azure timeout / downtime | Circuit Breaker + Retry + Fallback message chuẩn |
| Quyền hạn ("ảo giác quyền") | RBAC ở tầng tool, mọi action kiểm tra scope user |
| Latency voice | Streaming response, index Vector DB tối ưu |
| Tài liệu released bị sửa/lệch version | Kho immutable + checksum/hash + versioning; chỉ ingest qua quy trình release |
| OCR/hình ảnh kém chất lượng (scan mờ) | Vision model + OCR fallback, gắn confidence score, đánh dấu nguồn rủi ro |
| Bảng Excel phức tạp (merge cell, công thức) | Trích xuất có cấu trúc + giữ tham chiếu sheet/cell, ưu tiên giá trị đã tính |
| Agent tạo task JIRA sai/thừa | Human-in-the-loop bắt buộc duyệt trước khi ghi; dry-run + audit |

## 6. Phạm vi & Định hướng mở rộng

- **Core/MVP**: Phase 0–5 (RAG **multimodal trên kho released**, Function Calling, Voice, UI).
- **Hardening**: Phase 6–7 (Testing, Security, Deploy).
- **Future**:
  - Phase 8 — Multi-Agent (LangGraph: SQL agent / Doc agent / Log agent), ODC English Trainer.
  - Phase 9 — AI Agent phân tích requirement khách hàng + tự động hoá JIRA + quản lý Change Request (hỗ trợ BA).

## 7. Tài liệu liên quan

- [`03-document-search-strategy.md`](03-document-search-strategy.md) — Chiến lược tìm kiếm multimodal trên kho immutable.
- [`04-jira-automation-vision.md`](04-jira-automation-vision.md) — Tầm nhìn AI Agent requirement + JIRA.
