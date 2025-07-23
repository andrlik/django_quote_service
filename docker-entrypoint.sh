#!/usr/bin/env bash
set -eo pipefail

export PYTHONUNBUFFERED=1

python -m manage migrate --noinput --skip-checks
python -m manage collectstatic --noinput --skip-checks

uvicorn --host 0.0.0.0 --port 8000 --proxy-headers config.asgi:application
