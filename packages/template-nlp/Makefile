.PHONY: install start start-ci test lint lint-fix

install:
	uv sync

start:
	uv run uvicorn nlp.main:app --reload

start-ci:
	uv run uvicorn nlp.main:app --workers 1

test:
	uv run pytest

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

lint-fix:
	uv run ruff check --fix src tests
	uv run ruff format src tests
