#!/usr/bin/env bash
# sessionEnd — archive session, ensure summary exists
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INPUT=$(cat)

REASON=$(echo "$INPUT" | jq -r '.reason // empty')

"$ROOT/.agent/memory/bin/memory-cli" reconcile >/dev/null 2>&1 || true
"$ROOT/.agent/memory/bin/memory-cli" summarize >/dev/null 2>&1 || true
"$ROOT/.agent/memory/bin/memory-cli" stop --reason "$REASON" >/dev/null 2>&1 || true

exit 0
