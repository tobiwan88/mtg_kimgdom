FROM ghcr.io/astral-sh/uv:0.11.3-python3.14-trixie

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN uv sync --no-dev --no-editable

EXPOSE 5001

CMD ["uv", "run", "mtg-kingdom"]
