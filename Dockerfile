FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /bin/uv

RUN apk add --no-cache \
    python3-dev \
    postgresql-dev \
    gcc \
    musl-dev

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /axis-api

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev


FROM python:3.13-alpine AS final

RUN apk add --no-cache libpq

WORKDIR /axis-api

ENV FLASK_ENV=production \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python src/app.py"]
