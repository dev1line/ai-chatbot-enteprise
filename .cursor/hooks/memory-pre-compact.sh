#!/usr/bin/env bash
# preCompact — summarize changelog before context window compaction
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

"$ROOT/.agent/memory/bin/memory-cli" reconcile >/dev/null 2>&1 || true
"$ROOT/.agent/memory/bin/memory-cli" summarize --force >/dev/null 2>&1 || true

exit 0
