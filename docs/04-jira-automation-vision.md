# 04 — Tầm nhìn: AI Agent phân tích Requirement & tự động hoá JIRA

> Định hướng dài hạn: hệ thống AI Agent hỗ trợ **BA (Business Analyst)** phân tích tài liệu requirement khách hàng, tạo task trên **JIRA**, và quản lý **Change Request**.

## 1. Mục tiêu

- Giảm công sức thủ công của BA khi đọc/bóc tách requirement.
- Chuẩn hoá việc tạo backlog (epic → story → task → sub-task) trên JIRA.
- Theo dõi & quản lý **change request** dựa trên kho tài liệu released (immutable).
- Luôn có **human-in-the-loop**: agent đề xuất, người duyệt mới ghi.

## 2. Luồng nghiệp vụ (high-level)

```
[Tài liệu requirement KH]  (PDF/Word/Excel/ảnh — đa định dạng)
        │  (dùng pipeline multimodal ở docs/03)
        ▼
[Requirement Analyzer Agent]
   - Trích xuất yêu cầu, ràng buộc, acceptance criteria
   - Phát hiện mơ hồ / thiếu thông tin → đặt câu hỏi cho BA
        ▼
[Work Breakdown Agent]
   - Bóc tách Epic → Story → Task → Sub-task
   - Gắn estimate, priority, acceptance criteria, labels
        ▼
[BA Review (human-in-the-loop)]  ← BẮT BUỘC duyệt/chỉnh
        ▼
[JIRA Sync Agent]
   - Tạo/cập nhật issue qua JIRA REST API
   - Map field (project, issuetype, epic link, components)
        ▼
[Change Request Manager]
   - So sánh requirement mới vs bản released (immutable corpus)
   - Liệt kê thay đổi, đánh giá impact, đề xuất cập nhật issue
```

## 3. Các Agent đề xuất (mở rộng Multi-Agent ở Phase 8)

| Agent | Trách nhiệm |
|---|---|
| **Requirement Analyzer** | Đọc tài liệu đa định dạng, trích xuất requirement có cấu trúc, phát hiện gap/mâu thuẫn |
| **Work Breakdown** | Chuyển requirement → backlog (epic/story/task), estimate, acceptance criteria |
| **JIRA Sync** | Tạo/cập nhật issue qua API, idempotent (tránh tạo trùng), dry-run trước |
| **Change Request Manager** | Diff requirement vs released docs, impact analysis, đề xuất change |

## 4. Tích hợp JIRA

- **API**: JIRA Cloud REST API v3 (hoặc Data Center) qua token/OAuth.
- **Idempotency**: gắn external key (vd requirement id) để không tạo trùng issue.
- **Field mapping** cấu hình được: project key, issue type, epic link, components, labels, custom fields.
- **Dry-run mode**: in ra danh sách thao tác sẽ thực hiện trước khi ghi thật.
- **Audit**: log mọi thao tác ghi JIRA (ai duyệt, payload, kết quả).

## 5. Quản lý Change Request

- Tận dụng kho **immutable** (docs/03): mỗi release có version + hash.
- Khi có requirement/tài liệu mới → **diff ngữ nghĩa** với bản released gần nhất.
- Output: danh sách thay đổi (added/modified/removed), impact (module/issue liên quan), đề xuất tạo/cập nhật issue change request.

## 6. Guardrails & rủi ro

- **Human-in-the-loop bắt buộc** trước khi ghi JIRA (không auto-create không kiểm soát).
- **Idempotent + dry-run** để tránh spam/trùng issue.
- **RBAC**: chỉ vai trò được phép mới sync JIRA.
- **Bảo mật**: token JIRA trong Key Vault; không log secret; tôn trọng Zero Data Leak.
- **Truy xuất nguồn**: mỗi task đề xuất phải dẫn chiếu đoạn requirement gốc (citation).

## 7. Phụ thuộc

- Cần **Phase 2 (multimodal)** để đọc tài liệu requirement đa định dạng.
- Cần **Phase 8 (multi-agent)** làm khung orchestration.
- Triển khai chi tiết: xem `prompts/phase-09-jira-requirement-agent/prompt.md`.
