.PHONY: lint lint-fix format test install

install:
	uv sync

lint:
	uv run ruff check src/cli packages/*/src packages/*/tests packages/*/pyproject.toml
	uv run ruff format --check src/cli packages/*/src packages/*/tests

lint-fix:
	uv run ruff check --fix src/cli packages/*/src packages/*/tests packages/*/pyproject.toml
	uv run ruff format src/cli packages/*/src packages/*/tests

test:
	@echo "Phase 1: No root tests yet. Template tests will be added in later phases."
