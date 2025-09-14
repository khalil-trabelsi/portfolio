#!/bin/bash
set -e

echo "=== DBInitialisation ==="
mkdir -p instance

flask db upgrade

flask init-db

echo "=== Starting app ==="
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level info