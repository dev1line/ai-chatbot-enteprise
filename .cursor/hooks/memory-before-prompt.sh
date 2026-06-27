#!/usr/bin/env bash
# beforeSubmitPrompt — detect new task, switch changelog, reconcile accept/discard
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INPUT=$(cat)

PROMPT=$(echo "$INPUT" | jq -r '.prompt // .text // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // .conversation_id // empty')
CONVERSATION_ID=$(echo "$INPUT" | jq -r '.conversation_id // empty')

# Reconcile pending file edits (accept = content matches new, discard = reverted)
"$ROOT/.agent/memory/bin/memory-cli" reconcile >/dev/null 2>&1 || true

TASK_JSON=$("$ROOT/.agent/memory/bin/memory-cli" detect-task "$PROMPT" 2>/dev/null || echo '{"task_id":null}')
TASK_ID=$(echo "$TASK_JSON" | jq -r '.task_id // empty')

if [[ -n "$TASK_ID" ]]; then
  CURRENT=$("$ROOT/.agent/memory/bin/memory-cli" get-current 2>/dev/null || echo '{}')
  CURRENT_TASK=$(echo "$CURRENT" | jq -r '.current.task_id // empty')

  if [[ "$CURRENT_TASK" != "$TASK_ID" ]]; then
    # New task → create/switch changelog file
    "$ROOT/.agent/memory/bin/memory-cli" switch-task "$TASK_ID" \
      --session-id "$SESSION_ID" \
      --conversation-id "$CONVERSATION_ID" >/dev/null 2>&1 || true
  fi
fi

exit 0
