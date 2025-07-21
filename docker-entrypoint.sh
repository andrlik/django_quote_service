#!/usr/bin/env bash
set -eo pipefail

python -m manage migrate --noinput --skip-checks

uvicorn --port 8000 config.asgi.application
