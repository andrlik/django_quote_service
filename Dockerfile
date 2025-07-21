# syntax=docker/dockerfile:1.9
FROM python:3.13-slim-bookworm AS build

SHELL ["sh", "-exc"]

### Build prep

# Ensure apt-get doesn't open a menu on you.
ENV DEBIAN_FRONTEND=noninteractive

# Dependencies for environment
RUN <<EOT
apt-get update -qy
apt-get install -qyy optipng jpegoptim
EOT

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /usr/local/bin/

WORKDIR /app

# Tell uv to ignore warnings about hard links, target venv, and byte-compile.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PYTHONUNBUFFERED=1


 ### End build prep

 # Sync dependencies without the application itself.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

# Install application
COPY . /app
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev \
    uv pip install pip \
    uv run -m spacy download en_core_web_sm

# Compress and collect staticfiles for whitenoise
RUN <<EOT
bash -c /app/.venv/bin/python -m manage collectstatic --noinput --skip-checks
bash -c /app/.venv/bin/python -m manage compress --follow-links
bash -c /app/.venv/bin/python -m manage collectstatic --noinput --skip-checks
EOT

######################################################################
FROM python:3.13-slim-bookworm
SHELL ["sh", "-exc"]
# Ensure apt-get doesn't open a menu on you.
ENV DEBIAN_FRONTEND=noninteractive
# Dependencies for environment
RUN <<EOT
apt-get update -qy
apt-get install -qyy optipng jpegoptim
EOT

RUN <<EOT
groupadd -r app
useradd -r -d /app -g app -N app
EOT

ENTRYPOINT ["/app/docker-entrypoint.sh"]
STOPSIGNAL SIGINT

# Clean up
RUN <<EOT
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

COPY docker-entrypoint.sh /app

COPY --from=build --chown=app:app /app /app

USER app
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH \
    DJANGO_SETTINGS_MODULE=config.production.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN <<EOT
python -V
python -Im site
python -Ic 'import django_quote_service'
EOT
