# Phase 0 — Foundation & Project Setup

## Context
Đây là phase đầu tiên. Workspace có thể trống. Mục tiêu: dựng khung repo, môi trường, và công cụ để các phase sau build lên.

## Objective
Tạo monorepo `backend/` + `frontend/` + `infra/`, cấu hình môi trường, Docker, và CI cơ bản. Chưa cần logic nghiệp vụ.

> **Nguyên tắc bắt buộc — LOCAL-FIRST / DOCKER-FIRST:** Toàn bộ dev & test chức năng (Phase 0–6) phải **chạy được local qua Docker Compose**, KHÔNG phụ thuộc hạ tầng Azure. Hạ tầng Azure (Phase 7) chỉ triển khai **sau** khi dev xong chức năng. Phải có **flag ENV** (`APP_ENV`) + provider swappable để phân biệt local vs azure. Xem `docs/02-tech-stack.md` mục "LOCAL-FIRST".

## Scope
**In:** scaffold thư mục, dependency manifests, `.env.example` có flag môi trường, **Docker Compose chạy full stack local** (Postgres + Vector DB container + backend + frontend), Makefile/script phân biệt mode, pre-commit, CI lint/test skeleton.
**Out:** RAG, function calling, voice, UI logic (phase sau); hạ tầng Azure/IaC (Phase 7 — làm sau khi dev xong).

## Tasks
1. Tạo cấu trúc thư mục:
   ```
   backend/app/{api,core,orchestration,rag,tools,voice,repositories,schemas}
   backend/{prisma,tests}
   frontend/src/{components,hooks,api}
   infra/
   ```
2. **Backend deps** (`backend/pyproject.toml`): fastapi, uvicorn, pydantic-settings, prisma, langchain, openai (azure), tenacity, pybreaker, python-multipart, pytest.
3. **Frontend**: khởi tạo Vite + React + TypeScript (`frontend/package.json`).
4. **Config + flag môi trường**: `backend/app/core/config.py` dùng `pydantic-settings` đọc env, expose `APP_ENV` (`local|docker|staging|prod`) và các provider (`LLM_PROVIDER`, `VECTOR_DB_PROVIDER`, `OCR_PROVIDER`, `STT_PROVIDER`, `TTS_PROVIDER`, `SECRETS_PROVIDER`). Tạo `.env.example` đầy đủ biến + comment rõ "Azure chỉ bật ở staging/prod" (xem `docs/02-tech-stack.md`).
5. **Docker Compose (local-first)** (`docker-compose.yml` ở root): services `postgres` (+ volume), **vector DB local** (Milvus hoặc Qdrant container), `backend`, `frontend`. Đảm bảo `docker compose up` chạy full stack ở máy dev mà KHÔNG cần Azure.
6. **Makefile / scripts** phân biệt mode: `make dev-up` / `make dev-down` (local docker), `make logs`, `make test`. Đặt placeholder `make infra-*` (Phase 7) nhưng chưa triển khai.
7. **Health check**: endpoint `GET /health` trả `{"status":"ok","app_env":"<APP_ENV>"}` trong `backend/app/api`.
8. **Quality**: `.pre-commit-config.yaml` (ruff + black), `.gitignore`, GitHub Actions CI chạy lint + `pytest` (trong container/local, không cần Azure).
9. **README** mỗi sub-project (backend/frontend) với lệnh chạy local qua Docker + giải thích flag `APP_ENV`.

## Deliverables
- Cây thư mục đầy đủ + manifests.
- `docker-compose.yml` chạy full stack local (Postgres + Vector DB + backend + frontend).
- Makefile với `dev-up/dev-down/test` + placeholder `infra-*`.
- `.env.example` có flag `APP_ENV` + provider.
- CI workflow file.

## Acceptance Criteria
- [ ] `make dev-up` (docker compose) khởi động full stack local **không cần Azure**.
- [ ] `GET /health` trả 200 kèm `app_env`.
- [ ] Vector DB container (Milvus/Qdrant) chạy & kết nối được.
- [ ] `pytest` chạy local/trong container (ít nhất 1 test health pass).
- [ ] Frontend mở được trang trống.
- [ ] Đổi provider qua ENV không phải sửa code (abstraction sẵn sàng cho phase sau).
- [ ] Không có secret hardcode; mọi config qua env.

## Guardrails
- **LOCAL-FIRST**: phải chạy được hoàn toàn local qua Docker, không phụ thuộc Azure ở giai đoạn dev.
- Flag `APP_ENV` + provider swappable là bắt buộc.
- KHÔNG commit `.env` thật, chỉ `.env.example`.
- Pin version dependency rõ ràng.
- Cấu trúc tuân theo `docs/01-architecture.md` mục 3.
