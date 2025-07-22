#!/usr/bin/env bash
set -eo pipefail

python -m manage migrate --noinput --skip-checks

uvicorn --host 0.0.0.0 --port 8000 config.asgi:application
