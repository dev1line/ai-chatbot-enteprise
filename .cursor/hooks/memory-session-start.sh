#!/usr/bin/env bash
# sessionStart — inject task memory summary into agent context
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // .conversation_id // empty')
COMPOSER_MODE=$(echo "$INPUT" | jq -r '.composer_mode // "agent"')

"$ROOT/.agent/memory/bin/memory-cli" init >/dev/null 2>&1 || true

# Reconcile any pending edits from prior session
"$ROOT/.agent/memory/bin/memory-cli" reconcile >/dev/null 2>&1 || true

CONTEXT=$("$ROOT/.agent/memory/bin/memory-cli" context 2>/dev/null || echo '{"additional_context":""}')
ADDITIONAL=$(echo "$CONTEXT" | jq -r '.additional_context // empty')

if [[ -z "$ADDITIONAL" ]]; then
  ADDITIONAL="## Task memory\nNo active task changelog. Mention a task id (e.g. PH01-T3) to start tracking."
fi

BLOCK="## Memory Changelog (auto-injected)
$ADDITIONAL

---
Composer mode: $COMPOSER_MODE
Session: $SESSION_ID"

jq -n --arg ctx "$BLOCK" '{"additional_context": $ctx}'
exit 0
