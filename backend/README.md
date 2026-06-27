# Backend — AI Chatbot Enterprise

FastAPI + Prisma (PostgreSQL). **LOCAL-FIRST**: runs via Docker, and defaults to `LLM_PROVIDER=mock` so Azure is not required.

## Quick start (recommended: Docker from root)

```bash
# from the project root directory
make dev-up        # start postgres + qdrant + backend + frontend
```

Backend: http://localhost:8000 · Docs: http://localhost:8000/docs · Health: http://localhost:8000/health

## Run locally (without Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
prisma generate --schema=prisma/schema.prisma
# requires a running Postgres + DATABASE_URL
prisma db push --schema=prisma/schema.prisma
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q          # health/security/rbac tests that do not require a DB
```

## Environment flags

- `APP_ENV`: `local|docker|staging|prod`
- `LLM_PROVIDER`: `mock` (local) | `azure_openai` (Phase 2/7)
- `VECTOR_DB_PROVIDER`: `memory|qdrant|milvus|pinecone`

## Structure

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
