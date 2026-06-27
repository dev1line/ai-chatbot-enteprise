# Rule 05 — Memory Changelogs

> Bổ sung cho `03-task-management.md`. Agent **PHẢI** tuân thủ khi làm việc với task.

## Nguyên tắc

1. **Một task = một changelog** tại `.agent/memory/changelogs/<TASK_ID>.changelog.json`.
2. Khi bắt đầu task mới, **luôn** đề cập task id trong prompt (vd: `PH01-T3`) để hook tự tạo/switch changelog.
3. Đọc summary tại `.agent/memory/summaries/<TASK_ID>.summary.md` (nếu có) trước khi đọc changelog đầy đủ.
4. Không chỉnh sửa trực tiếp file trong `.agent/memory/` trừ khi user yêu cầu.

## Khi implement

1. Claim task trong `.agent/tasks/` (Assignee + `in_progress`).
2. Ghi task id trong message đầu tiên → hook tạo changelog.
3. Mỗi thay đổi file được ghi tự động qua `afterFileEdit` (status `pending`).
4. Sau khi user review diff:
   - **Accept** (giữ thay đổi): reconcile tự mark `accepted`.
   - **Discard** (revert): reconcile tự mark `discarded`.
5. Khi hoàn thành checklist → cập nhật task `review`/`done` + chạy `memory-cli summarize`.

## Context injection

`sessionStart` inject memory summary vào agent context. Ưu tiên thông tin từ summary thay vì đọc lại toàn bộ lịch sử chat.

## Manual commands

```bash
.agent/memory/bin/memory-cli reconcile
.agent/memory/bin/memory-cli accept <entry_id> --update-task-status review
.agent/memory/bin/memory-cli discard <entry_id>
.agent/memory/bin/memory-cli summarize --force
```

## Không làm

- Không tạo nhiều changelog cho cùng một task id.
- Không xóa entries đã `accepted` (chỉ summarize).
- Không commit secrets vào changelog previews.
