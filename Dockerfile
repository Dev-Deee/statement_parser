FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "statement_parser.main:app", "--host", "0.0.0.0", "--port", "8000"]