#!/usr/bin/env bash
# stop — finalize session, reconcile accept/discard, emit follow-up if needed
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INPUT=$(cat)

REASON=$(echo "$INPUT" | jq -r '.reason // .status // empty')

OUT=$("$ROOT/.agent/memory/bin/memory-cli" stop --reason "$REASON" 2>/dev/null || echo '{}')
FOLLOWUP=$(echo "$OUT" | jq -r '.followup_message // empty')

if [[ -n "$FOLLOWUP" ]]; then
  jq -n --arg msg "$FOLLOWUP" '{"followup_message": $msg}'
else
  echo '{}'
fi
exit 0
