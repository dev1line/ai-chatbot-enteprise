# Backend — AI Chatbot Enterprise

FastAPI + Prisma (PostgreSQL). **LOCAL-FIRST**: chạy qua Docker, mặc định `LLM_PROVIDER=mock` nên không cần Azure.

## Chạy nhanh (khuyến nghị: Docker từ root)

```bash
# tại thư mục gốc dự án
make dev-up        # khởi động postgres + qdrant + backend + frontend
```

Backend: http://localhost:8000 · Docs: http://localhost:8000/docs · Health: http://localhost:8000/health · Chatbox: http://localhost:8000/chatbox

Chatbox hiện chạy theo chế độ không cần đăng nhập ứng dụng:
- UI gọi `POST /api/public/chat/completions`
- Backend dùng trực tiếp `OPENAI_API_KEY` từ ENV để gọi Azure/OpenAI

## Chạy local (không Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
prisma generate --schema=prisma/schema.prisma
# cần 1 Postgres đang chạy + DATABASE_URL
prisma db push --schema=prisma/schema.prisma
uvicorn app.main:app --reload
```

## ENV

- File ENV chạy backend đặt tại `backend/.env`.
- Không dùng trực tiếp file trong `.github/initial_document` để chạy runtime.
- `app/core/config.py` đã ưu tiên đọc theo thứ tự: `backend/.env` -> `.env`.

Chạy server từ root:

```bash
python -m uvicorn app.main:app --app-dir backend --reload
```

Chạy server từ thư mục backend:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## Test

```bash
pytest -q          # test health/security/rbac không cần DB
```

## API chat v1 (session-based)

- `POST /api/v1/chat/sessions` tạo session mới
- `GET /api/v1/chat/sessions` liệt kê session của user hiện tại
- `GET /api/v1/chat/sessions/{session_id}/messages?page=1&page_size=20`
- `POST /api/v1/chat/completions`

Payload completions:

```json
{
  "session_id": "your-session-id",
  "content": "Hello"
}
```

Lưu ý: API v1 dùng JWT bearer token hiện có (`/api/auth/register`, `/api/auth/login`).

## API public chat (không cần login)

- `POST /api/public/chat/completions`

Payload:

```json
{
  "message": "Hello",
  "history": [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello"}
  ]
}
```

## Flag môi trường

- `APP_ENV`: `local|docker|staging|prod`
- `LLM_PROVIDER`: `mock` (local) | `azure_openai` (Phase 2/7)
- `VECTOR_DB_PROVIDER`: `memory|qdrant|milvus|pinecone`

Chat completion/OpenAI config:

- `OPENAI_API_KEY`
- `MODEL_NAME` (Azure deployment name, ví dụ `gpt-5-mini`)
- `MAX_CONTEXT_TOKENS` (mặc định `2048`)
- `COMPLETION_TOKEN_RESERVE` (mặc định `256`)
- `DEFAULT_PAGE_SIZE` (mặc định `20`)
- `OPENAI_BASE_URL` (ví dụ `https://<resource>.openai.azure.com/openai/v1`)
- `OPENAI_API_VERSION` (mặc định `2024-02-01`)
- `OPENAI_VERIFY_SSL` (`true|false`)

Azure Entra ID mode (theo mẫu Azure, không cần `OPENAI_API_KEY`):

- `OPENAI_USE_ENTRA_ID=true`
- `OPENAI_ENTRA_SCOPE=https://ai.azure.com/.default`
- `OPENAI_BASE_URL=https://<resource>.services.ai.azure.com/openai/v1`
- `MODEL_NAME=<deployment-name>`

Khi bật Entra ID mode, backend dùng `DefaultAzureCredential()` + bearer token provider để gọi Azure OpenAI.

Khuyến nghị môi trường corporate proxy:

- `NO_PROXY=localhost,127.0.0.1`

Mapping lỗi OpenAI:

- Lỗi kết nối OpenAI -> `503`
- Lỗi xác thực OpenAI -> `401`
- Lỗi OpenAI khác -> `502`

## Cấu trúc

```
app/
  api/            routers: health, auth, chat
  core/           config, logging, db, security, deps, rbac
  orchestration/  llm provider abstraction (mock/azure)
  repositories/   Repository Pattern (Prisma)
  schemas/        Pydantic models
prisma/           schema.prisma
tests/            pytest
```
