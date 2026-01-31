#!/bin/sh
set -e

echo "[entrypoint] Starting backend..."

# Optional: skip sanity checks if SKIP_SANITY_CHECK=1
if [ "${SKIP_SANITY_CHECK:-0}" != "1" ]; then
  echo "[entrypoint] Running sanity checks..."
  python /app/scripts/sanity_check.py || true
fi

# Optional: skip migrations if SKIP_DB_MIGRATIONS=1
if [ "${SKIP_DB_MIGRATIONS:-0}" != "1" ]; then
  echo "[entrypoint] Applying database migrations..."
  alembic -c /app/alembic.ini upgrade head || echo "[entrypoint] Migration failed (continuing)"
fi

APP_HOST="${BACKEND_HOST:-0.0.0.0}"
APP_PORT="${BACKEND_PORT:-8000}"
APP_ENV="${ENVIRONMENT:-development}"

echo "[entrypoint] Starting uvicorn on ${APP_HOST}:${APP_PORT} (${APP_ENV})"

if [ "$APP_ENV" = "development" ]; then
  exec python -m uvicorn main:app --host "$APP_HOST" --port "$APP_PORT" --reload
else
  exec python -m uvicorn main:app --host "$APP_HOST" --port "$APP_PORT"
fi
