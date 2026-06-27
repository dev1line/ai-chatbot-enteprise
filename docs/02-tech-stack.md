# 02 — Tech Stack & Lý do lựa chọn

| Layer | Công nghệ | Lý do |
|---|---|---|
| Language | Python 3.11+ | Hệ sinh thái AI/ML mạnh nhất |
| Web framework | FastAPI | Async, type-safe (Pydantic), streaming, docs tự động |
| ORM | Prisma (prisma-client-py) | Type-safe, migration tốt, tách session logic |
| Database | PostgreSQL | Quan hệ vững, JSONB, đủ cho báo cáo Text-to-SQL |
| Orchestration | LangChain | Điều phối RAG + tool calling, nhiều integration |
| Embeddings | Azure OpenAI text-embedding-ada-002 | Chất lượng cao, cùng hệ Azure (compliance) |
| Doc parsing (multimodal) | unstructured, PyMuPDF/pdfplumber, openpyxl/pandas | Trích xuất PDF/Excel/Word có cấu trúc, layout-aware |
| OCR | Tesseract / Azure AI Document Intelligence | Đọc PDF scan & text trong ảnh (compliance khi dùng Azure) |
| Vision | Azure OpenAI vision / CLIP-class embeddings | Mô tả & tìm kiếm trên hình ảnh, diagram |
| Hybrid search | BM25 (Postgres/Elastic) + dense embeddings + cross-encoder rerank | Bắt cả từ khoá chính xác lẫn ngữ nghĩa, tăng precision |
| Vector DB | Pinecone (managed) / Milvus (self-host) | Metadata filter + namespace theo version (immutable corpus) |
| LLM | Azure OpenAI (GPT-4 class) | Private VNet, enterprise compliance, no-train |
| STT | Whisper | Mã nguồn mở, đa ngôn ngữ, chính xác |
| TTS | Hugging Face TTS | Mã nguồn mở, tối ưu chi phí, tự host |
| Frontend | React (hoặc Vue) + TypeScript | Hệ sinh thái lớn, dễ tuyển dụng |
| Audio | Web Audio API / MediaRecorder | Ghi âm Hold-to-Talk trên trình duyệt |
| Testing | PyTest | Chuẩn de-facto cho Python |
| LLM Eval | Ragas / TruLens | Đo faithfulness, answer relevancy, hallucination |
| Resilience | Circuit Breaker (pybreaker), Retry (tenacity) | Chịu lỗi khi Azure timeout |
| Security | Azure Private Link, VNet, Key Vault | Zero Data Leak, secret management |
| Future | LangGraph / AutoGen | Multi-agent orchestration |
| Issue tracking | JIRA REST API v3 (Atlassian) | Tự động hoá tạo/cập nhật task cho BA, quản lý change request |

## Quy ước môi trường

- Secrets qua **Azure Key Vault** / biến môi trường, KHÔNG hardcode.
- `.env.example` mô tả mọi biến cần thiết.
- Tách config theo môi trường: `dev`, `staging`, `prod`.

## Nguyên tắc triển khai: LOCAL-FIRST / DOCKER-FIRST

> Quan trọng: **Phải chạy được local (qua Docker) trước**. Toàn bộ development & test chức năng (Phase 0–6) chạy trên **Docker Compose** ở máy dev. **Hạ tầng Azure (Phase 7) chỉ triển khai SAU khi dev xong chức năng.**

- Phải có **flag môi trường** trong ENV để phân biệt chế độ chạy:
  - `APP_ENV=local | docker | staging | prod`
  - Provider **swappable qua ENV** để local không phụ thuộc Azure bắt buộc.
- Local mode dùng **alternatives chạy được offline/trong Docker** (Postgres container, Milvus/Qdrant container, Tesseract OCR, Whisper local, HF TTS local). Azure chỉ bật khi `APP_ENV` ở `staging/prod` hoặc cấu hình rõ ràng.
- Mọi script/Makefile target tách biệt: `make dev-up` (local docker) vs `make infra-*` (Azure — chạy sau).

### Provider abstraction (chọn qua ENV)

| Biến | Local/Docker | Azure (sau) |
|---|---|---|
| `LLM_PROVIDER` | `azure_openai` (có thể trỏ key dev) hoặc mock | `azure_openai` (private VNet) |
| `EMBEDDING_PROVIDER` | `azure_openai` / local | `azure_openai` |
| `VECTOR_DB_PROVIDER` | `milvus` / `qdrant` (container) | `pinecone` / `milvus` |
| `OCR_PROVIDER` | `tesseract` (local) | `azure_doc_intelligence` |
| `STT_PROVIDER` | `whisper_local` | `whisper_local` / azure |
| `TTS_PROVIDER` | `hf_local` | `hf_local` |
| `SECRETS_PROVIDER` | `env` (.env) | `azure_key_vault` |

## Biến môi trường chính (ví dụ)

```
# --- Run mode / flags ---
APP_ENV=local                 # local | docker | staging | prod
SECRETS_PROVIDER=env          # env | azure_key_vault
LLM_PROVIDER=azure_openai     # azure_openai | mock
EMBEDDING_PROVIDER=azure_openai
VECTOR_DB_PROVIDER=milvus     # milvus | qdrant | pinecone
OCR_PROVIDER=tesseract        # tesseract | azure_doc_intelligence
STT_PROVIDER=whisper_local
TTS_PROVIDER=hf_local

# --- Azure (chỉ bật ở staging/prod hoặc khi cấu hình) ---
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT_CHAT=
AZURE_OPENAI_DEPLOYMENT_EMBED=

# --- Vector DB ---
PINECONE_API_KEY=
MILVUS_URI=http://milvus:19530

# --- Core ---
DATABASE_URL=postgresql://app:app@postgres:5432/app
WHISPER_MODEL=base
TTS_MODEL=...
JWT_SECRET=
JIRA_BASE_URL=
JIRA_API_TOKEN=
```
