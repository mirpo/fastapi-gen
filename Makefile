.PHONY: install sync lint lint-fix test build clean update

install:
	uv sync --extra dev

sync:
	uv sync --extra dev

lint:
	uv run ruff check .
	uv run ruff format --check --diff .

lint-fix:
	uv run ruff check --fix src
	uv run ruff format .

test:
	uv run pytest

build:
	uv build

clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .ruff_cache/

update:
	uv sync --upgrade
