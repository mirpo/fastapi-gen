.PHONY: lint lint-fix test install

install:
	uv sync

lint:
	uv run ruff check src/cli

lint-fix:
	uv run ruff check --fix src

test:
	@echo "Phase 1: No root tests yet. Template tests will be added in later phases."
