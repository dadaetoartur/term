FROM python:3.12-slim as build_env
RUN apt update && apt install -y curl

ENV POETRY_HOME="/opt/poetry" \
    POETRY_URL="https://install.python-poetry.org" \
    POETRY_VERSION=1.5.1

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL $POETRY_URL | python3 -
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry export --only main -f requirements.txt -o /app/requirements.txt

FROM python:3.12-slim
RUN apt update && apt install -y gcc curl

COPY --from=build_env /app/requirements.txt /app/requirements.txt

WORKDIR /app
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    pip install --no-cache-dir -r requirements.txt

# Transfer './alembic' and alembic configurations for upgrade the database
COPY ./alembic ./alembic
COPY alembic.ini ./

# Transfer './artifacts' files for xml_schema_processor
COPY ./artifacts ./artifacts

COPY ./service ./service

CMD ["gunicorn", "--config", "service/gunicorn_config.py", "service.main:app"]
