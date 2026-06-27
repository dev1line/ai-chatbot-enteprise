# Phase 1 — Backend Core & Architecture

## Context
Tiếp nối Phase 0 (scaffold đã có). Giờ xây nền backend: data layer, auth, RBAC, Repository Pattern — nền tảng cho RAG/tools/voice.

## Objective
Triển khai FastAPI app có cấu trúc rõ ràng: Prisma + PostgreSQL, auth JWT, RBAC, Repository Pattern, error handling & logging chuẩn.

## Scope
**In:** schema Prisma, migrations, repositories, auth/JWT, RBAC middleware, base chat endpoint (echo/mock LLM), logging, exception handlers.
**Out:** RAG retrieval, function calling thật, voice (phase sau). LLM tạm mock.

## Tasks
1. **Prisma schema** (`backend/prisma/schema.prisma`): models `User`, `Role`, `Conversation`, `Message`, `Document` (metadata). Quan hệ + enum role (`ADMIN`, `ENGINEER`, `VIEWER`).
2. Chạy migration + generate Prisma client.
3. **Repository Pattern** (`app/repositories/`): `UserRepository`, `ConversationRepository`, `MessageRepository` — cô lập mọi truy vấn DB, không gọi Prisma trực tiếp ở router.
4. **Auth** (`app/core/security.py`): JWT issue/verify, password hashing, dependency `get_current_user`.
5. **RBAC** (`app/core/rbac.py`): decorator/dependency `require_role(...)`; thiết kế để **tool/action sau này** kiểm tra scope user.
6. **Schemas** (`app/schemas/`): Pydantic request/response cho chat & auth.
7. **Chat endpoint** (`app/api/chat.py`): `POST /api/chat` nhận message, lưu Conversation/Message, trả mock response (placeholder cho orchestrator phase sau).
8. **Cross-cutting**: structured logging (request id, user id, latency), global exception handlers, CORS.

## Deliverables
- Prisma schema + migration chạy được.
- Repositories + auth + RBAC + chat endpoint (mock).
- Unit test cho repository & auth.

## Acceptance Criteria
- [ ] Đăng ký/đăng nhập trả JWT hợp lệ.
- [ ] `POST /api/chat` yêu cầu auth, lưu message, trả mock answer.
- [ ] RBAC chặn user thiếu quyền (403).
- [ ] Router KHÔNG gọi Prisma trực tiếp (chỉ qua repository).
- [ ] `pytest` cho repo/auth pass.

## Guardrails
- Tuyệt đối không gọi DB trực tiếp ngoài repository layer.
- RBAC phải mở rộng được cho tầng tool (Phase 3).
- Mọi secret qua env / Key Vault.
- Log không chứa dữ liệu nhạy cảm (password, token, PII).
