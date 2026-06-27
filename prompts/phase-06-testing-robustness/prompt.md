# Phase 6 — Testing & Robustness

## Context
Hệ thống đã đủ chức năng (Phase 0–5). Giờ đảm bảo **chất lượng & độ bền**: test chặt cho function calling, đánh giá RAG (Ragas/TruLens), và xử lý ngoại lệ (Circuit Breaker + Fallback).

## Objective
Bộ test toàn diện + đo lường chất lượng LLM + cơ chế chịu lỗi cho Azure/STT/TTS.

## Scope
**In:** unit/integration test, security test cho SQL tool, RAG eval (Ragas/TruLens), Circuit Breaker, Retry, Fallback.
**Out:** triển khai hạ tầng (Phase 7).

## Tasks
1. **Unit tests** (PyTest): repositories, auth/RBAC, tool validators (đặc biệt SQL).
2. **Security tests cho SQL tool**: bộ ca tấn công (DROP/DELETE/UPDATE/INSERT/`;`/comment injection) → **đều bị chặn**. Đây là test bắt buộc.
3. **Integration tests**: luồng `/api/chat` (RAG), function calling, `/api/voice/chat`.
4. **RAG evaluation** (`tests/eval/`): dùng **Ragas/TruLens** đo faithfulness, answer relevancy, context precision; ngưỡng pass cấu hình được (vd faithfulness > 0.85). Đo tỷ lệ hallucination.
5. **Circuit Breaker** (`app/core/resilience.py`): pybreaker quanh Azure OpenAI; khi mở mạch → fallback message chuẩn.
6. **Retry**: tenacity cho lỗi tạm thời (timeout/429) với backoff.
7. **Fallback**: STT/TTS/LLM lỗi → phản hồi văn bản tiêu chuẩn, không crash.
8. **CI**: chạy unit + security + integration; eval chạy theo schedule/manual (vì tốn token).

## Deliverables
- Test suite (unit/integration/security).
- Eval harness Ragas/TruLens + báo cáo ngưỡng.
- Module resilience (circuit breaker + retry + fallback).

## Acceptance Criteria
- [ ] Mọi ca SQL phá hoại bị chặn (test xanh).
- [ ] Eval RAG đạt ngưỡng cấu hình; báo cáo metric.
- [ ] Khi Azure timeout → Circuit Breaker mở → fallback, không 500.
- [ ] Retry hoạt động cho lỗi tạm thời.
- [ ] CI chạy test pass.

## Guardrails
- Security test cho SQL là **must-have**, không bỏ qua.
- Eval phải đo được hallucination, không chỉ "chạy được".
- Fallback message không lộ chi tiết lỗi nội bộ ra client.
