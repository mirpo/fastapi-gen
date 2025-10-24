.PHONY: install start test lint lint-fix

install:
	uv sync

start:
	uv run uvicorn nlp.main:app --reload

test:
	uv run pytest

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

lint-fix:
	uv run ruff check --fix src tests
	uv run ruff format src tests
