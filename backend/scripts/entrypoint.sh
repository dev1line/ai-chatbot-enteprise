#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] APP_ENV=${APP_ENV:-local}"

# Đồng bộ schema vào DB (dev local). Phase 7 sẽ dùng migrate deploy.
echo "[entrypoint] prisma db push..."
prisma db push --schema=prisma/schema.prisma --accept-data-loss || {
  echo "[entrypoint] WARN: prisma db push failed (DB chưa sẵn sàng?)"
}

echo "[entrypoint] starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
