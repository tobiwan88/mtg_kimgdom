FROM ghcr.io/astral-sh/uv:0.11.3-python3.14-trixie-slim

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src/ ./src/

RUN uv sync --no-dev --no-editable

EXPOSE 5001

CMD ["uv", "run", "gunicorn", "mtg_kimgdom.app:app", "--bind", "0.0.0.0:5001", "--workers", "2"]
