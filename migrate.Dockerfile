FROM python:3.10.12-alpine3.18

RUN apk update && \
    pip install --upgrade pip && \
    pip install poetry && \
    rm -rf /var/cache/apk/*

WORKDIR /migrate

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY config.py config.py
COPY alembic ./alembic
COPY alembic.ini alembic.ini

RUN poetry install --without dev,test --no-root

CMD ["poetry", "run", "alembic", "upgrade", "head"]
