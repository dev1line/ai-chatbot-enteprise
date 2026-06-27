# Phase 9 — AI Agent phân tích Requirement & tự động hoá JIRA (BA Support)

## Context
Hệ thống đã có RAG multimodal (Phase 2) + multi-agent orchestration (Phase 8). Phase này hiện thực **tầm nhìn dài hạn**: AI Agent hỗ trợ **BA** phân tích tài liệu requirement khách hàng, tạo task trên **JIRA**, và quản lý **Change Request**.

> Tham khảo bắt buộc: `docs/04-jira-automation-vision.md` và `docs/03-document-search-strategy.md`.

## Objective
Triển khai pipeline agent: đọc tài liệu requirement (đa định dạng) → trích xuất requirement có cấu trúc → bóc tách backlog → **BA duyệt (human-in-the-loop)** → sync JIRA → quản lý change request dựa trên kho immutable.

## Scope
**In:** Requirement Analyzer agent, Work Breakdown agent, JIRA Sync agent (idempotent, dry-run), Change Request Manager, human-in-the-loop review API/UI hook.
**Out:** thay đổi luồng RAG cốt lõi; tự ý ghi JIRA không qua duyệt.

## Tasks
1. **Requirement ingestion**: tái dùng pipeline multimodal Phase 2 để đọc requirement (PDF/Word/Excel/ảnh) → text có cấu trúc + citation tới đoạn gốc.
2. **Requirement Analyzer agent** (`app/agents/requirement_analyzer.py`):
   - Trích xuất requirement, ràng buộc, acceptance criteria.
   - Phát hiện mơ hồ/thiếu/mâu thuẫn → sinh câu hỏi làm rõ cho BA.
3. **Work Breakdown agent** (`app/agents/work_breakdown.py`):
   - Bóc tách Epic → Story → Task → Sub-task; gắn estimate, priority, labels, acceptance criteria.
   - Mỗi item dẫn chiếu (citation) đoạn requirement gốc.
4. **Human-in-the-loop review**: endpoint trả **đề xuất backlog** cho BA duyệt/chỉnh; chỉ khi duyệt mới sang bước sync.
5. **JIRA Sync agent** (`app/integrations/jira/`):
   - JIRA REST API v3 (token/OAuth, secret ở Key Vault).
   - **Idempotent**: external key (requirement id) chống tạo trùng.
   - **Dry-run mode**: in danh sách thao tác trước khi ghi thật.
   - Field mapping cấu hình được (project, issuetype, epic link, components, labels, custom fields).
   - Audit log mọi thao tác ghi (người duyệt, payload, kết quả).
6. **Change Request Manager** (`app/agents/change_request.py`):
   - Diff ngữ nghĩa requirement mới vs bản released (immutable corpus, Phase 2 version/hash).
   - Output: added/modified/removed + impact + đề xuất tạo/cập nhật issue change request.
7. **RBAC + feature flag**: chỉ vai trò được phép sync JIRA; bật/tắt toàn bộ tính năng qua config.
8. **Orchestration**: cắm các agent vào LangGraph (Phase 8) — Main Agent điều phối, giữ citations xuyên suốt.

## Deliverables
- Agents: requirement_analyzer, work_breakdown, change_request.
- JIRA integration (idempotent + dry-run + audit + field mapping).
- Review API (human-in-the-loop) + feature flag + RBAC.
- Test: phân tích tài liệu mẫu → backlog đề xuất; dry-run JIRA; diff change request.

## Acceptance Criteria
- [ ] Upload requirement đa định dạng → agent trả backlog đề xuất kèm citation đoạn gốc.
- [ ] BA duyệt rồi mới ghi JIRA; không có auto-create khi chưa duyệt.
- [ ] Dry-run liệt kê đúng thao tác; chạy thật idempotent (không tạo trùng).
- [ ] Change Request Manager diff được requirement mới vs release cũ + impact.
- [ ] RBAC chặn user không có quyền sync; feature flag tắt không ảnh hưởng MVP.
- [ ] Mọi thao tác JIRA được audit log.

## Guardrails
- **Human-in-the-loop bắt buộc** trước khi ghi JIRA.
- **Idempotent + dry-run** để tránh spam/trùng issue.
- Token JIRA trong Key Vault; không log secret; tôn trọng **Zero Data Leak**.
- Mỗi task đề xuất phải có citation requirement gốc (truy xuất nguồn).
- Tái dùng RAG multimodal (Phase 2) & multi-agent (Phase 8), không trùng lặp logic.
