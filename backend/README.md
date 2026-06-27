# Backend — AI Chatbot Enterprise

FastAPI + Prisma (PostgreSQL). **LOCAL-FIRST**: chạy qua Docker, mặc định `LLM_PROVIDER=mock` nên không cần Azure.

## Chạy nhanh (khuyến nghị: Docker từ root)

```bash
# tại thư mục gốc dự án
make dev-up        # khởi động postgres + qdrant + backend + frontend
```

Backend: http://localhost:8000 · Docs: http://localhost:8000/docs · Health: http://localhost:8000/health

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

## Test

```bash
pytest -q          # test health/security/rbac không cần DB
```

## Flag môi trường

- `APP_ENV`: `local|docker|staging|prod`
- `LLM_PROVIDER`: `mock` (local) | `azure_openai` (Phase 2/7)
- `VECTOR_DB_PROVIDER`: `memory|qdrant|milvus|pinecone`

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
