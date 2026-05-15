.PHONY: lint lint-fix format test install check-deps

install:
	uv sync

lint:
	uv run ruff check src/cli packages/*/src packages/*/tests packages/*/pyproject.toml
	uv run ruff format --check src/cli packages/*/src packages/*/tests

lint-fix:
	uv run ruff check --fix src/cli packages/*/src packages/*/tests packages/*/pyproject.toml
	uv run ruff format src/cli packages/*/src packages/*/tests

test:
	uv run pytest tests/

check-deps:
	uv run python scripts/check_dep_sync.py
