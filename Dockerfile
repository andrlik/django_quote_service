ARG APP_NAME=django_quote_service
ARG APP_PATH=/app
ARG PYTHON_VERSION=3.12.3

# Stage: staging
FROM python:$PYTHON_VERSION-slim as staging
ARG APP_NAME
ARG APP_PATH

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR $APP_PATH
COPY ./pyproject.toml ./manage.py ./Justfile ./requirements.lock ./requirements-dev.lock ./
COPY ./bin ./bin
COPY ./config ./config
COPY ./locale ./locale
COPY ./$APP_NAME ./$APP_NAME

RUN mkdir staticfiles && apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential \
    && python -m pip install --no-cache-dir --upgrade uv pip setuptools build \
    && python -m uv pip install --no-cache-dir --system -r requirements.lock \
    && python -m spacy download en_core_web_trf --no-cache-dir \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove gcc build-essential

# Stage: development
FROM staging as development
ARG APP_NAME
ARG APP_PATH

# Install project in editable mode
WORKDIR $APP_PATH
RUN python -m uv pip install --system -r requirements-dev.lock

ENV DJANGO_DEBUG=True \
    DJANGO_SETTINGS_MODULE=config.settings.local \
    DATABASE_URL=postgres://daniel@192.168.7.31:5432/django_quote_service

ENTRYPOINT ["python", "-m"]
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

# Stage: production
FROM staging as production
ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH

ENV DJANGO_DEBUG=False \
    DJANGO_SETTINGS_MODULE=config.settings.production

RUN python manage.py collectstatic --noinput \
    && python manage.py compress \
    && python manage.py collectstatic --noinput

# ENTRYPOINT ["python", "-m"]
CMD ["daphne", "-p", "8080", "-b", "0.0.0.0", "config.asgi:application"]
