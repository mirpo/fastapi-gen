.PHONY: lint lint-fix format test install

install:
	uv sync

lint:
	uv run ruff check src/cli
	uv run ruff format --check src/cli

lint-fix:
	uv run ruff check --fix src
	uv run ruff format src

test:
	@echo "Phase 1: No root tests yet. Template tests will be added in later phases."
