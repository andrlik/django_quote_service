ARG APP_NAME=django_quote_service
ARG APP_PATH=/app
ARG PYTHON_VERSION=3.10.4
ARG POETRY_VERSION=1.1.13

# Stage: Staging
FROM python:$PYTHON_VERSION as staging
ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./manage.py ./pytest.ini ./.pylintrc ./
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
RUN poetry install

ENV DJANGO_DEBUG=True \
    DJANGO_SETTINGS_MODULE=config.settings.local \
    DATABASE_URL=postgres://daniel@192.168.7.31:5432/django_quote_service

ENTRYPOINT ["poetry", "run"]
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]

# Stage: production
FROM staging as production
ARG APP_NAME
ARG APP_PATH

WORKDIR $APP_PATH
RUN poetry install --no-dev

ENV DJANGO_DEBUG=False \
    DJANGO_SETTINGS_MODULE=config.settings.production

RUN poetry run python manage.py collectstatic --noinput
RUN poetry run python manage.py compress
RUN poetry run python manage.py collectstatic --noinput

ENTRYPOINT ["poetry", "run"]
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080"]


