# FastAPI Quality

A FastAPI project with comprehensive code quality tools.

## Features

- FastAPI web framework
- Code quality tools: Ruff, Mypy, Bandit
- Pre-commit hooks
- GitHub Actions CI

## Quick Start

```bash
# Install dependencies
uv sync --extra dev

# Run development server
uv run uvicorn src.fastapi_quality.main:app --reload

# Run tests
uv run pytest tests/ -v

# Run quality checks
uv run ruff check .
uv run ruff format .
uv run mypy src/
uv run bandit -r src/
```

## Documentation

See [docs/usage.md](docs/usage.md) for detailed usage instructions.
