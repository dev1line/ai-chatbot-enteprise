# Memory Changelogs — Per-task agent context

Hệ thống **memory changelogs** ghi nhận ngữ cảnh theo từng task, tích hợp Cursor hooks để tự động cập nhật khi agent chỉnh sửa file và khi user accept/discard thay đổi.

## Cấu trúc

```
.agent/memory/
├── README.md                          ← bạn đang đọc
├── index.json                         ← registry các changelog theo task_id
├── current-task.json                  ← task đang active trong session
├── changelogs/
│   ├── CHANGELOG-template.json
│   └── PH01-T3.changelog.json         ← một file / một task
├── summaries/
│   └── PH01-T3.summary.md             ← bản tóm tắt tối ưu context
├── lib/
│   └── memory_store.py
└── bin/
    └── memory-cli                     ← CLI cho hooks & agent
```

## Vòng đời

```
todo → in_progress → review → done
         ↑ changelog_state: active | summarized | paused
         ↑ entry status: pending → accepted | discarded
```

### Mỗi task = một changelog

- Khi prompt chứa `PH<NN>-T<n>` (vd: `PH01-T3`), hook `beforeSubmitPrompt` tự **switch** sang changelog tương ứng.
- Task mới → tạo file `.agent/memory/changelogs/PH01-T3.changelog.json`.
- Nếu task ở `todo`, tự chuyển sang `in_progress` trong `.agent/tasks/`.

### Accept / Discard (reconcile)

Cursor **chưa có** hook native cho nút Accept/Discard. Cơ chế reconcile dựa trên nội dung file:

| Trạng thái file trên disk | Entry status |
|---------------------------|--------------|
| Khớp `new_hash`           | `accepted`   |
| Khớp `old_hash` (revert)  | `discarded`  |
| Khác cả hai               | `accepted` (partial) |

Reconcile chạy tự động tại: `beforeSubmitPrompt`, `preCompact`, `stop`, `sessionEnd`.

Manual override:

```bash
.agent/memory/bin/memory-cli accept e001 --update-task-status review
.agent/memory/bin/memory-cli discard e002
.agent/memory/bin/memory-cli reconcile
```

## Cursor hooks (`.cursor/hooks.json`)

| Hook | Script | Hành vi |
|------|--------|---------|
| `sessionStart` | `memory-session-start.sh` | Inject summary vào `additional_context` |
| `beforeSubmitPrompt` | `memory-before-prompt.sh` | Detect task, tạo/switch changelog, reconcile |
| `afterFileEdit` | `memory-after-edit.sh` | Ghi entry `pending` cho mỗi edit |
| `preCompact` | `memory-pre-compact.sh` | Summarize trước khi compact context |
| `stop` | `memory-stop.sh` | Reconcile + follow-up nếu còn pending |
| `sessionEnd` | `memory-session-end.sh` | Archive + summarize |

## Summary (tối ưu context)

Khi changelog có ≥12 entries hoặc ≥6000 ký tự JSON, hệ thống tạo `.agent/memory/summaries/<TASK>.summary.md`.

- `sessionStart` inject summary thay vì toàn bộ changelog.
- `preCompact` force summarize trước khi Cursor compact context window.

## CLI

```bash
# Khởi tạo
.agent/memory/bin/memory-cli init

# Detect task từ text
.agent/memory/bin/memory-cli detect-task "Implement PH01-T3 repository pattern"

# Switch / tạo changelog
.agent/memory/bin/memory-cli switch-task PH01-T3

# Xem context sẽ inject
.agent/memory/bin/memory-cli context

# Summarize thủ công
.agent/memory/bin/memory-cli summarize --force
```

## Quy tắc cho agent

Xem `.agent/rules/05-memory-changelogs.md`.
