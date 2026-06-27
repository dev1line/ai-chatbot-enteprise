#!/usr/bin/env python3
"""Memory changelog store — per-task context tracking for Cursor agent sessions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MEMORY_ROOT = Path(__file__).resolve().parents[1]
CHANGELOGS_DIR = MEMORY_ROOT / "changelogs"
SUMMARIES_DIR = MEMORY_ROOT / "summaries"
INDEX_PATH = MEMORY_ROOT / "index.json"
CURRENT_TASK_PATH = MEMORY_ROOT / "current-task.json"
AGENT_ROOT = MEMORY_ROOT.parent
TASKS_DIR = AGENT_ROOT / "tasks"

TASK_ID_RE = re.compile(r"\bPH(\d{2})-T(\d+)\b", re.IGNORECASE)
SUMMARY_ENTRY_THRESHOLD = 12
SUMMARY_CHAR_THRESHOLD = 6000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    CHANGELOGS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def preview(text: str, limit: int = 200) -> str:
    text = text.replace("\r\n", "\n")
    if len(text) <= limit:
        return text
    return text[:limit] + "…"


def changelog_path(task_id: str) -> Path:
    return CHANGELOGS_DIR / f"{task_id.upper()}.changelog.json"


def summary_path(task_id: str) -> Path:
    return SUMMARIES_DIR / f"{task_id.upper()}.summary.md"


def load_index() -> dict[str, Any]:
    ensure_dirs()
    return read_json(INDEX_PATH, {"changelogs": [], "current_task_id": None}) or {
        "changelogs": [],
        "current_task_id": None,
    }


def save_index(index: dict[str, Any]) -> None:
    write_json(INDEX_PATH, index)


def load_current_task() -> dict[str, Any]:
    ensure_dirs()
    return read_json(CURRENT_TASK_PATH, {}) or {}


def save_current_task(data: dict[str, Any]) -> None:
    write_json(CURRENT_TASK_PATH, data)


def detect_task_id(text: str) -> str | None:
    match = TASK_ID_RE.search(text or "")
    if not match:
        return None
    return f"PH{match.group(1)}-T{match.group(2)}"


def find_tasks_file(task_id: str) -> Path | None:
    phase = task_id[2:4]
    for path in TASKS_DIR.glob(f"phase-{phase}-*.tasks.md"):
        return path
    return None


def read_task_status(task_id: str) -> str | None:
    tasks_file = find_tasks_file(task_id)
    if not tasks_file or not tasks_file.exists():
        return None
    task_num = task_id.split("-T")[-1]
    section_re = re.compile(
        rf"###\s+T{task_num}\s+—.*?\n- \*\*Status:\*\*\s+(\w+)",
        re.DOTALL,
    )
    text = tasks_file.read_text(encoding="utf-8")
    match = section_re.search(text)
    return match.group(1) if match else None


def update_task_status_in_file(task_id: str, new_status: str) -> bool:
    tasks_file = find_tasks_file(task_id)
    if not tasks_file or not tasks_file.exists():
        return False
    task_num = task_id.split("-T")[-1]
    text = tasks_file.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(###\s+T{task_num}\s+—[^\n]*\n(?:.*?\n)*?- \*\*Status:\*\*\s+)\w+",
        re.DOTALL,
    )
    updated, count = pattern.subn(rf"\g<1>{new_status}", text, count=1)
    if count == 0:
        return False
    tasks_file.write_text(updated, encoding="utf-8")
    return True


def new_changelog(
    task_id: str,
    *,
    session_id: str | None = None,
    conversation_id: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    task_id = task_id.upper()
    path = changelog_path(task_id)
    if path.exists() and not force:
        changelog = read_json(path, {})
        changelog["updated_at"] = utc_now()
        if session_id:
            changelog["session_id"] = session_id
        if conversation_id:
            changelog["conversation_id"] = conversation_id
        write_json(path, changelog)
        return changelog

    task_status = read_task_status(task_id) or "todo"
    changelog: dict[str, Any] = {
        "task_id": task_id,
        "phase": task_id[2:4],
        "status": task_status,
        "changelog_state": "active",
        "session_id": session_id,
        "conversation_id": conversation_id,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "entries": [],
        "context_notes": [],
    }
    write_json(path, changelog)

    index = load_index()
    if task_id not in index.get("changelogs", []):
        index.setdefault("changelogs", []).append(task_id)
    index["current_task_id"] = task_id
    save_index(index)

    save_current_task(
        {
            "task_id": task_id,
            "changelog_path": str(path.relative_to(AGENT_ROOT.parent)),
            "session_id": session_id,
            "conversation_id": conversation_id,
            "activated_at": utc_now(),
        }
    )
    return changelog


def get_changelog(task_id: str | None = None) -> dict[str, Any] | None:
    if not task_id:
        current = load_current_task()
        task_id = current.get("task_id") or load_index().get("current_task_id")
    if not task_id:
        return None
    path = changelog_path(task_id.upper())
    if not path.exists():
        return None
    return read_json(path)


def save_changelog(changelog: dict[str, Any]) -> None:
    changelog["updated_at"] = utc_now()
    write_json(changelog_path(changelog["task_id"]), changelog)


def next_entry_id(changelog: dict[str, Any]) -> str:
    return f"e{len(changelog.get('entries', [])) + 1:03d}"


def append_file_edit(
    *,
    file_path: str,
    edits: list[dict[str, str]],
    generation_id: str | None = None,
    tool_name: str | None = None,
) -> dict[str, Any] | None:
    changelog = get_changelog()
    if not changelog:
        return None

    entries = changelog.setdefault("entries", [])
    for edit in edits:
        old_s = edit.get("old_string", "")
        new_s = edit.get("new_string", "")
        entry = {
            "id": next_entry_id(changelog),
            "type": "file_edit",
            "status": "pending",
            "file_path": file_path,
            "old_hash": content_hash(old_s),
            "new_hash": content_hash(new_s),
            "old_preview": preview(old_s),
            "new_preview": preview(new_s),
            "generation_id": generation_id,
            "tool_name": tool_name,
            "timestamp": utc_now(),
        }
        entries.append(entry)

    save_changelog(changelog)
    return changelog


def reconcile_pending() -> dict[str, Any]:
    changelog = get_changelog()
    if not changelog:
        return {"accepted": 0, "discarded": 0, "pending": 0}

    accepted = discarded = pending = 0
    for entry in changelog.get("entries", []):
        if entry.get("status") != "pending" or entry.get("type") != "file_edit":
            continue

        file_path = Path(entry["file_path"])
        if not file_path.is_absolute():
            file_path = AGENT_ROOT.parent / file_path

        if not file_path.exists():
            entry["status"] = "discarded"
            entry["resolved_at"] = utc_now()
            entry["resolution"] = "file_missing"
            discarded += 1
            continue

        current_hash = content_hash(file_path.read_text(encoding="utf-8", errors="replace"))
        if current_hash == entry.get("new_hash"):
            entry["status"] = "accepted"
            entry["resolved_at"] = utc_now()
            entry["resolution"] = "content_matches_new"
            accepted += 1
        elif current_hash == entry.get("old_hash"):
            entry["status"] = "discarded"
            entry["resolved_at"] = utc_now()
            entry["resolution"] = "content_reverted_to_old"
            discarded += 1
        else:
            entry["status"] = "accepted"
            entry["resolved_at"] = utc_now()
            entry["resolution"] = "content_modified_partial"
            accepted += 1

    save_changelog(changelog)
    pending = sum(1 for e in changelog.get("entries", []) if e.get("status") == "pending")
    return {"accepted": accepted, "discarded": discarded, "pending": pending}


def set_entry_status(entry_id: str, status: str) -> bool:
    changelog = get_changelog()
    if not changelog:
        return False
    for entry in changelog.get("entries", []):
        if entry.get("id") == entry_id:
            entry["status"] = status
            entry["resolved_at"] = utc_now()
            entry["resolution"] = f"manual_{status}"
            save_changelog(changelog)
            return True
    return False


def set_changelog_state(state: str) -> None:
    changelog = get_changelog()
    if not changelog:
        return
    changelog["changelog_state"] = state
    save_changelog(changelog)


def append_context_note(note: str, source: str = "agent") -> None:
    changelog = get_changelog()
    if not changelog:
        return
    changelog.setdefault("context_notes", []).append(
        {"text": note, "source": source, "timestamp": utc_now()}
    )
    save_changelog(changelog)


def build_summary(changelog: dict[str, Any]) -> str:
    task_id = changelog["task_id"]
    lines = [
        f"# Memory Summary — {task_id}",
        "",
        f"- **Task status:** {changelog.get('status', 'unknown')}",
        f"- **Changelog state:** {changelog.get('changelog_state', 'active')}",
        f"- **Updated:** {changelog.get('updated_at', '')}",
        "",
        "## Accepted changes",
    ]

    accepted = [e for e in changelog.get("entries", []) if e.get("status") == "accepted"]
    discarded = [e for e in changelog.get("entries", []) if e.get("status") == "discarded"]
    pending = [e for e in changelog.get("entries", []) if e.get("status") == "pending"]

    if accepted:
        for entry in accepted[-8:]:
            if entry.get("type") == "file_edit":
                lines.append(f"- `{entry.get('file_path')}` — {entry.get('new_preview', '')[:120]}")
    else:
        lines.append("- (none yet)")

    lines.extend(["", "## Discarded / reverted"])
    if discarded:
        for entry in discarded[-4:]:
            lines.append(f"- `{entry.get('file_path')}` ({entry.get('resolution', '')})")
    else:
        lines.append("- (none)")

    if pending:
        lines.extend(["", "## Pending review"])
        for entry in pending:
            lines.append(f"- `{entry.get('file_path')}` — awaiting accept/discard")

    notes = changelog.get("context_notes", [])
    if notes:
        lines.extend(["", "## Context notes"])
        for note in notes[-6:]:
            lines.append(f"- {note.get('text', '')}")

    lines.extend(
        [
            "",
            "## Agent instructions",
            "- Treat this summary as authoritative task memory.",
            "- On new task: a new changelog file is created automatically.",
            "- Pending entries are reconciled on accept (file matches new) or discard (reverted).",
        ]
    )
    return "\n".join(lines)


def maybe_summarize(force: bool = False) -> str | None:
    changelog = get_changelog()
    if not changelog:
        return None

    entries = changelog.get("entries", [])
    total_chars = sum(len(json.dumps(e)) for e in entries)
    if not force and len(entries) < SUMMARY_ENTRY_THRESHOLD and total_chars < SUMMARY_CHAR_THRESHOLD:
        return None

    summary = build_summary(changelog)
    path = summary_path(changelog["task_id"])
    path.write_text(summary, encoding="utf-8")

    changelog["changelog_state"] = "summarized"
    changelog["summary_path"] = str(path.relative_to(AGENT_ROOT.parent))
    changelog["summarized_at"] = utc_now()
    save_changelog(changelog)
    return summary


def get_session_context() -> str:
    changelog = get_changelog()
    if not changelog:
        return ""

    task_id = changelog["task_id"]
    summary_file = summary_path(task_id)
    if summary_file.exists():
        return summary_file.read_text(encoding="utf-8")

    pending = sum(1 for e in changelog.get("entries", []) if e.get("status") == "pending")
    accepted = sum(1 for e in changelog.get("entries", []) if e.get("status") == "accepted")
    return (
        f"## Active task memory ({task_id})\n"
        f"- Status: {changelog.get('status')}\n"
        f"- Changelog: {changelog.get('changelog_state')}\n"
        f"- Entries: {accepted} accepted, {pending} pending\n"
        f"- Read full changelog: `.agent/memory/changelogs/{task_id}.changelog.json`"
    )


def handle_stop(reason: str | None = None) -> dict[str, str]:
    reconcile_pending()
    summary = maybe_summarize(force=False)
    changelog = get_changelog()
    if changelog:
        if reason in ("completed", None):
            changelog["changelog_state"] = "active"
        elif reason in ("aborted", "user_close"):
            changelog["changelog_state"] = "paused"
        save_changelog(changelog)

    followup = ""
    if changelog:
        pending = sum(1 for e in changelog.get("entries", []) if e.get("status") == "pending")
        if pending:
            followup = (
                f"Memory: {pending} changelog entries still pending reconciliation "
                f"for {changelog['task_id']}. Run reconcile on next prompt."
            )
        elif summary:
            followup = f"Memory summary updated for {changelog['task_id']}."
    return {"followup_message": followup} if followup else {}


def cmd_init(_: argparse.Namespace) -> int:
    ensure_dirs()
    write_json(
        INDEX_PATH,
        read_json(INDEX_PATH, {"changelogs": [], "current_task_id": None}),
    )
    print(json.dumps({"ok": True, "memory_root": str(MEMORY_ROOT)}))
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    task_id = detect_task_id(args.text)
    print(json.dumps({"task_id": task_id}))
    return 0


def cmd_create(args: argparse.Namespace) -> int:
    changelog = new_changelog(
        args.task_id,
        session_id=args.session_id,
        conversation_id=args.conversation_id,
        force=args.force,
    )
    print(json.dumps(changelog))
    return 0


def cmd_get_current(_: argparse.Namespace) -> int:
    print(json.dumps({"current": load_current_task(), "index": load_index()}))
    return 0


def cmd_append_edit(args: argparse.Namespace) -> int:
    payload = json.loads(args.payload)
    changelog = append_file_edit(
        file_path=payload["file_path"],
        edits=payload.get("edits", []),
        generation_id=payload.get("generation_id"),
        tool_name=payload.get("tool_name"),
    )
    print(json.dumps({"ok": bool(changelog), "task_id": changelog.get("task_id") if changelog else None}))
    return 0


def cmd_reconcile(_: argparse.Namespace) -> int:
    result = reconcile_pending()
    print(json.dumps(result))
    return 0


def cmd_accept(args: argparse.Namespace) -> int:
    ok = set_entry_status(args.entry_id, "accepted")
    if ok and args.update_task_status:
        changelog = get_changelog()
        if changelog:
            update_task_status_in_file(changelog["task_id"], args.update_task_status)
            changelog["status"] = args.update_task_status
            save_changelog(changelog)
    print(json.dumps({"ok": ok}))
    return 0


def cmd_discard(args: argparse.Namespace) -> int:
    ok = set_entry_status(args.entry_id, "discarded")
    print(json.dumps({"ok": ok}))
    return 0


def cmd_summarize(args: argparse.Namespace) -> int:
    summary = maybe_summarize(force=args.force)
    print(json.dumps({"summarized": summary is not None, "length": len(summary or "")}))
    return 0


def cmd_context(_: argparse.Namespace) -> int:
    print(json.dumps({"additional_context": get_session_context()}))
    return 0


def cmd_switch(args: argparse.Namespace) -> int:
    task_id = args.task_id.upper()
    changelog = new_changelog(task_id, session_id=args.session_id, conversation_id=args.conversation_id)
    status = read_task_status(task_id)
    if status == "todo":
        update_task_status_in_file(task_id, "in_progress")
        changelog["status"] = "in_progress"
    save_changelog(changelog)
    print(json.dumps(changelog))
    return 0


def cmd_stop(args: argparse.Namespace) -> int:
    print(json.dumps(handle_stop(args.reason)))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent memory changelog CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    p_detect = sub.add_parser("detect-task")
    p_detect.add_argument("text")
    p_detect.set_defaults(func=cmd_detect)

    p_create = sub.add_parser("create-changelog")
    p_create.add_argument("task_id")
    p_create.add_argument("--session-id")
    p_create.add_argument("--conversation-id")
    p_create.add_argument("--force", action="store_true")
    p_create.set_defaults(func=cmd_create)

    sub.add_parser("get-current").set_defaults(func=cmd_get_current)

    p_append = sub.add_parser("append-edit")
    p_append.add_argument("payload")
    p_append.set_defaults(func=cmd_append_edit)

    sub.add_parser("reconcile").set_defaults(func=cmd_reconcile)

    p_accept = sub.add_parser("accept")
    p_accept.add_argument("entry_id")
    p_accept.add_argument("--update-task-status")
    p_accept.set_defaults(func=cmd_accept)

    p_discard = sub.add_parser("discard")
    p_discard.add_argument("entry_id")
    p_discard.set_defaults(func=cmd_discard)

    p_sum = sub.add_parser("summarize")
    p_sum.add_argument("--force", action="store_true")
    p_sum.set_defaults(func=cmd_summarize)

    sub.add_parser("context").set_defaults(func=cmd_context)

    p_switch = sub.add_parser("switch-task")
    p_switch.add_argument("task_id")
    p_switch.add_argument("--session-id")
    p_switch.add_argument("--conversation-id")
    p_switch.set_defaults(func=cmd_switch)

    p_stop = sub.add_parser("stop")
    p_stop.add_argument("--reason")
    p_stop.set_defaults(func=cmd_stop)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
