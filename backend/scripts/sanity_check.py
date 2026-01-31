"""Sanity checks for required env vars and database connectivity.

Run at container startup to fail fast with clear messaging.
"""
from __future__ import annotations

import os
import sys
import time
from typing import List

try:
    import psycopg2
except ImportError:
    # If psycopg2 not available, skip DB check
    psycopg2 = None

REQUIRED_VARS: List[str] = ["DATABASE_URL", "SECRET_KEY", "BACKEND_HOST", "BACKEND_PORT"]
MAX_WAIT_SECONDS = int(os.getenv("DB_WAIT_TIMEOUT", "30"))


def main() -> None:
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        sys.stderr.write(f"[sanity] Missing required env vars: {', '.join(missing)}\n")
        sys.exit(1)

    if not psycopg2:
        print("[sanity] psycopg2 not available, skipping DB check")
        print("[sanity] Env checks passed")
        return

    db_url = os.environ["DATABASE_URL"]
    deadline = time.time() + MAX_WAIT_SECONDS

    while True:
        try:
            with psycopg2.connect(db_url, connect_timeout=5) as conn:
                conn.cursor().execute("SELECT 1")
            print("[sanity] Database reachable")
            break
        except Exception as exc:  # noqa: BLE001 - we want to surface exact DB error
            if time.time() > deadline:
                sys.stderr.write(f"[sanity] Database unreachable within {MAX_WAIT_SECONDS}s: {exc}\n")
                sys.exit(2)
            print("[sanity] Waiting for database to become ready...")
            time.sleep(3)

    print("[sanity] Env and DB checks passed")


if __name__ == "__main__":
    main()
