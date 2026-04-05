FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN uv sync --no-dev --no-editable

EXPOSE 5001

CMD ["uv", "run", "mtg-kingdom"]
