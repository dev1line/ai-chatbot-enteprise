#!/usr/bin/env bash
# afterFileEdit — record pending edits to current task changelog
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty')
GENERATION_ID=$(echo "$INPUT" | jq -r '.generation_id // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "Write"')
EDITS=$(echo "$INPUT" | jq -c '.edits // []')

if [[ -z "$FILE_PATH" || "$EDITS" == "[]" ]]; then
  exit 0
fi

# Skip memory/changelog files to avoid recursion
if [[ "$FILE_PATH" == *".agent/memory/"* ]]; then
  exit 0
fi

PAYLOAD=$(jq -n \
  --arg fp "$FILE_PATH" \
  --argjson edits "$EDITS" \
  --arg gid "$GENERATION_ID" \
  --arg tool "$TOOL_NAME" \
  '{file_path: $fp, edits: $edits, generation_id: $gid, tool_name: $tool}')

"$ROOT/.agent/memory/bin/memory-cli" append-edit "$PAYLOAD" >/dev/null 2>&1 || true
exit 0
