# Phase 3 — Actionable RAG (Function Calling)

## Context
RAG (Phase 2) đã trả lời từ tài liệu. Giờ thêm điểm đột phá: **khả năng hành động** — LLM gọi tool để **Text-to-SQL** (báo cáo) và **gọi internal API** (Ops/Security), an toàn và có RBAC.

## Objective
Triển khai Function Calling với LangChain/Azure OpenAI: tool `text_to_sql` (chỉ SELECT) và `internal_api_call`, có validation + sandbox + RBAC ở tầng tool.

## Scope
**In:** tool schema, text-to-SQL an toàn, internal API tool, tool routing trong orchestrator, RBAC tool-level.
**Out:** voice (Phase 4), UI (Phase 5).

## Tasks
1. **Tool framework** (`app/tools/base.py`): interface tool có `name`, `schema`, `validate()`, `run()`, và `required_role`.
2. **Text-to-SQL tool** (`app/tools/sql_tool.py`):
   - Cung cấp schema DB (tên bảng/cột) cho LLM (schema-aware).
   - LLM sinh SQL → **validator**: chỉ cho phép `SELECT`, chặn `DROP/DELETE/UPDATE/INSERT/ALTER`, chặn multi-statement.
   - Chạy qua read-only connection / role giới hạn → trả kết quả.
3. **Internal API tool** (`app/tools/api_tool.py`): whitelist endpoint (vd check container/server status, KMS, WAF), timeout, RBAC.
4. **Orchestrator routing** (`app/orchestration/agent.py`): expose tool schema cho Azure OpenAI Function Calling; LLM chọn RAG vs tool; vòng lặp tool-call → kết quả → tóm tắt.
5. **RBAC tool-level**: trước khi `run()`, kiểm tra `current_user` có `required_role` (chống "ảo giác quyền hạn").
6. **Audit log**: ghi mọi tool call (user, tool, params, kết quả tóm tắt, latency).
7. Tích hợp vào `/api/chat`: phân biệt câu trả lời RAG vs câu trả lời từ action (kèm dữ liệu).

## Deliverables
- Tool base + sql_tool + api_tool + agent routing.
- Audit logging cho tool calls.
- Test: SQL hợp lệ chạy được; SQL phá hoại bị chặn; RBAC chặn user thiếu quyền.

## Acceptance Criteria
- [ ] "Doanh thu tuần này theo dự án?" → sinh SELECT đúng → trả số liệu.
- [ ] Lệnh chứa DROP/DELETE/UPDATE/INSERT bị từ chối an toàn.
- [ ] Internal API tool chỉ gọi endpoint trong whitelist.
- [ ] User thiếu quyền gọi tool → bị chặn (audit ghi nhận).
- [ ] Câu hỏi tài liệu vẫn đi luồng RAG (không gọi tool thừa).

## Guardrails
- **Chỉ SELECT** cho SQL; ưu tiên DB role read-only riêng cho tool.
- Mọi tool có `validate()` trước `run()`.
- RBAC bắt buộc ở tầng tool, không tin tưởng LLM tự ý.
- Audit log đầy đủ, không log secret.
