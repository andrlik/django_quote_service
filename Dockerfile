ARG APP_NAME=django_quote_service
ARG APP_PATH=/app
ARG PYTHON_VERSION=3.12.0

# Stage: Staging
FROM python:$PYTHON_VERSION as staging
ARG APP_NAME
ARG APP_PATH

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Install uv
RUN python -m pip install --upgrade uv pip

WORKDIR $APP_PATH
COPY ./pyproject.toml ./manage.py ./Justfile ./requirements.lock ./requirements-dev.lock ./
COPY ./bin ./bin
COPY ./config ./config
COPY ./locale ./locale
COPY ./staticfiles ./staticfiles
COPY ./$APP_NAME ./$APP_NAME

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
RUN python -m uv pip install --system -r requirements.lock
RUN python -m spacy download en_core_web_trf

ENV DJANGO_DEBUG=False \
    DJANGO_SETTINGS_MODULE=config.settings.production

RUN python manage.py collectstatic --noinput
RUN python manage.py compress
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python", "-m"]
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]
