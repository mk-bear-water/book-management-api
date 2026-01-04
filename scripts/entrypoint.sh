#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"
