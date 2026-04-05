# MTG Commander Kingdom

Self-hosted web app for playing **Advanced Kingdoms**, the hidden-role EDH variant. Players join via a shared link and each see only their own secret role.
Based on the rules from https://www.reddit.com/r/EDH/comments/1mz2y6o/edh_variant_advanced_kingdoms_casual_commander/ 

## Install & run

```bash
uv pip install git+https://github.com/tobiwan88/mtg_kimgdom.git
mtg-kingdom
```

Open `http://localhost:5001`.

## Development

```bash
git clone https://github.com/tobiwan88/mtg_kimgdom.git
cd mtg_kimgdom
uv sync --group dev
uv run pre-commit install
uv run mtg-kingdom
```

| Tool | Command |
|------|---------|
| Lint & format | `uv run ruff check . && uv run ruff format .` |
| Type check | `uv run ty check` |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `5001` | Port the app listens on |
| `MAX_SESSIONS` | `20` | Max concurrent games; oldest is dropped when limit is reached |
