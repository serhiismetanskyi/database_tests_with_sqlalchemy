FROM python:3.10.12-alpine3.18

RUN apk update && \
    pip install --upgrade pip && \
    pip install poetry && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY config.py config.py
COPY src ./src
COPY tests ./tests
COPY logger.ini logger.ini

RUN poetry install --with dev,test --no-root

CMD ["poetry", "run", "pytest", "-s"]
