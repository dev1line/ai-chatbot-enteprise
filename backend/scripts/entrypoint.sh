#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] APP_ENV=${APP_ENV:-local}"

# Sync the schema into the DB (local dev). Phase 7 will use migrate deploy.
echo "[entrypoint] prisma db push..."
prisma db push --schema=prisma/schema.prisma --accept-data-loss || {
  echo "[entrypoint] WARN: prisma db push failed (DB not ready yet?)"
}

echo "[entrypoint] starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
