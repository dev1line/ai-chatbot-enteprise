# Enterprise AI Chatbot — "Actionable RAG" Platform

Trợ lý AI nội bộ cho doanh nghiệp (đặc biệt mô hình **ODC** — Offshore Development Center) giúp tra cứu tài liệu nghiệp vụ, policy bảo mật và **thực thi hành động** (gọi API, query SQL) qua cả **văn bản** lẫn **giọng nói** — với cam kết **Zero Data Leak**.

> Điểm đột phá: không chỉ "đọc tài liệu rồi trả lời" (RAG truyền thống) mà **Actionable RAG** — chatbot có khả năng hành động (call function / truy vấn DB) một cách an toàn và có kiểm soát quyền (RBAC).

> **Mục đích cốt lõi**: tìm kiếm **đa phương thức (multimodal)** trên kho tài liệu đã **released/bất biến** — gồm **hình ảnh, PDF, Excel** — để tra cứu đầy đủ & chính xác hơn.
>
> **Tầm nhìn xa**: AI Agent tự động **phân tích tài liệu requirement khách hàng** và **tạo task trên JIRA**, hỗ trợ **BA** và quản lý **Change Request**.

---

## 1. Mục tiêu (theo STAR)

| | Nội dung |
|---|---|
| **Situation** | Doanh nghiệp/ODC đối mặt khối lượng lớn tài liệu nghiệp vụ + policy bảo mật phức tạp. Kỹ sư tốn nhiều thời gian tra cứu thủ công → chậm xử lý sự cố & vận hành. |
| **Task** | Xây trợ lý AI nội bộ hỗ trợ tra cứu + thực thi hành động qua text/voice, tích hợp hệ thống nội bộ, đảm bảo bảo mật tuyệt đối (Zero Data Leak). |
| **Action** | Backend Python (FastAPI), Azure OpenAI làm "não bộ" tuân thủ compliance, luồng RAG + Vector DB, Function Calling cho DB/báo cáo, STT & TTS bằng mã nguồn mở. |
| **Result** | Giảm ~80% thời gian tra cứu. Hỗ trợ hands-free. Truy vấn real-time bằng ngôn ngữ tự nhiên, chính xác & an toàn. |

## 2. Tính năng cốt lõi

- **Multimodal Search trên kho Released/Immutable**: tìm kiếm đầy đủ trên text, **PDF, hình ảnh (diagram/screenshot), Excel**; kho tài liệu released bất biến (versioned + hash), citation đúng tới page/sheet/cell/vùng ảnh.
- **Actionable RAG**: trả lời từ tài liệu + gọi API / sinh & chạy SQL có kiểm soát.
- **Voice Pipeline**: Hold-to-Talk → Whisper (STT) → LLM → HuggingFace (TTS), hỗ trợ streaming.
- **Citations bắt buộc**: mọi câu trả lời RAG phải hiển thị "Trích dẫn" (trang/tài liệu nguồn) để tăng độ tin cậy.
- **RBAC**: phân quyền người dùng, "ảo giác quyền hạn" bị chặn ở tầng tool.
- **Robustness**: Circuit Breaker + Retry + Fallback khi Azure timeout.
- **Compliance**: Azure OpenAI trong private VNet (Azure Private Link), không train trên dữ liệu doanh nghiệp.

## 3. Use Cases

1. **Multimodal Document Search (cốt lõi)**: tra cứu nội dung nằm trong ảnh/diagram, PDF, bảng Excel của tài liệu đã release; trả lời + trích dẫn nguồn chính xác.
2. **Ops/Security Bot**: tra cứu policy an toàn (WAF/KMS), check trạng thái container/server qua API.
3. **Báo cáo thông minh (Text-to-SQL)**: "Doanh thu tuần này theo dự án là bao nhiêu?" → bot sinh SQL, query DB, đọc kết quả bằng giọng nói.
4. **BA / Requirement Automation (tầm nhìn)**: phân tích tài liệu requirement khách hàng → đề xuất backlog → BA duyệt → tạo task JIRA; quản lý change request dựa trên kho immutable.

## 4. Kiến trúc & Tech Stack (tóm tắt)

```
[ React/Vue UI ] --(text/audio)--> [ FastAPI Gateway ]
        |                                  |
   Web Audio API                     Auth + RBAC
        |                                  |
   Whisper STT  <-----------------> [ Orchestrator (LangChain) ]
                                          /    |    \
                            [ RAG Retriever ] [ Function Calling ] [ Azure OpenAI ]
                                    |               |        \
                            [ Vector DB ]   [ SQL / Internal APIs ]  embeddings(ada-002)
                            (Pinecone/Milvus)        |
                                              [ PostgreSQL via Prisma ]
        |
   HuggingFace TTS  <--- (audio response stream) ---
```

| Layer | Công nghệ |
|---|---|
| Backend | Python, **FastAPI**, Repository Pattern |
| ORM / DB | **Prisma ORM**, **PostgreSQL** |
| AI Orchestration | **LangChain** |
| Embeddings | Azure OpenAI **text-embedding-ada-002** |
| Vector DB | **Pinecone / Milvus** |
| LLM | **Azure OpenAI** (private VNet) |
| STT | **Whisper** (OpenAI SDK / open-source) |
| TTS | **Hugging Face** TTS |
| Frontend | **React / Vue**, Web Audio API |
| Testing | **PyTest**, **Ragas / TruLens** |
| Resilience | **Circuit Breaker**, Retry, Streaming |
| Security | **Azure Private Link**, VNet |
| Future | Multi-Agent (**LangGraph / AutoGen**) |

## 4b. Nguyên tắc triển khai: LOCAL-FIRST / DOCKER-FIRST

- Dev & test toàn bộ chức năng (**Phase 0–6**) chạy **local qua Docker Compose**, KHÔNG phụ thuộc Azure.
- **Hạ tầng Azure (Phase 7) triển khai SAU** khi dev xong chức năng.
- Phân biệt môi trường bằng **flag ENV** `APP_ENV` (`local|docker|staging|prod`) + provider swappable (`LLM_PROVIDER`, `VECTOR_DB_PROVIDER`, `OCR_PROVIDER`, `SECRETS_PROVIDER`...). Đổi môi trường = đổi flag, không sửa logic.
- Lệnh: `make dev-up` (chạy local), `make infra-*` (Azure — làm sau). Chi tiết: `docs/02-tech-stack.md` mục "LOCAL-FIRST".

## 5. Roadmap theo Phase

| Phase | Tên | Mục tiêu chính | Prompt |
|---|---|---|---|
| **0** | Foundation & Setup | Repo, env, Docker, CI cơ bản | [`prompts/phase-00-foundation`](prompts/phase-00-foundation/prompt.md) |
| **1** | Backend Core & Architecture | FastAPI, Prisma, PostgreSQL, RBAC, Repository Pattern | [`prompts/phase-01-backend-core`](prompts/phase-01-backend-core/prompt.md) |
| **2** | Multimodal RAG (Released/Immutable) | Ingestion text/PDF/ảnh/Excel → embeddings → Vector DB (versioned) → hybrid search + rerank + citations đa phương thức | [`prompts/phase-02-rag-vectordb`](prompts/phase-02-rag-vectordb/prompt.md) |
| **3** | Actionable RAG (Function Calling) | Text-to-SQL an toàn + gọi internal API qua tools | [`prompts/phase-03-actionable-rag`](prompts/phase-03-actionable-rag/prompt.md) |
| **4** | Voice Pipeline | Whisper STT + HuggingFace TTS + streaming | [`prompts/phase-04-voice-pipeline`](prompts/phase-04-voice-pipeline/prompt.md) |
| **5** | Frontend / UI | Chat Console, Hold-to-Talk, Citations | [`prompts/phase-05-frontend-ui`](prompts/phase-05-frontend-ui/prompt.md) |
| **6** | Testing & Robustness | PyTest, Ragas/TruLens, Circuit Breaker, Fallback | [`prompts/phase-06-testing-robustness`](prompts/phase-06-testing-robustness/prompt.md) |
| **7** | Security & Deployment | Azure Private Link, VNet, observability, deploy | [`prompts/phase-07-security-deployment`](prompts/phase-07-security-deployment/prompt.md) |
| **8** | Multi-Agent & Future | LangGraph orchestrator, ODC English Trainer | [`prompts/phase-08-multi-agent-future`](prompts/phase-08-multi-agent-future/prompt.md) |
| **9** | JIRA & Requirement Automation | AI Agent phân tích requirement → backlog → JIRA (BA support), Change Request | [`prompts/phase-09-jira-requirement-agent`](prompts/phase-09-jira-requirement-agent/prompt.md) |

## 6. Tài liệu

- [`docs/00-project-analysis.md`](docs/00-project-analysis.md) — Phân tích chi tiết theo STAR + rủi ro.
- [`docs/01-architecture.md`](docs/01-architecture.md) — Kiến trúc hệ thống & data flow.
- [`docs/02-tech-stack.md`](docs/02-tech-stack.md) — Tech stack & lý do lựa chọn.
- [`docs/03-document-search-strategy.md`](docs/03-document-search-strategy.md) — Chiến lược tìm kiếm multimodal trên kho immutable.
- [`docs/04-jira-automation-vision.md`](docs/04-jira-automation-vision.md) — Tầm nhìn AI Agent requirement + JIRA.

## 7. Cách dùng bộ prompt

Xem [`prompts/README.md`](prompts/README.md). Mỗi phase có 1 file `prompt.md` để đưa cho AI coding agent thực thi tuần tự (Phase 0 → 8).
