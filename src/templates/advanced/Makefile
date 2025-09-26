.PHONY: install sync lint lint-fix test start build clean update

PORT=8000
HOST=127.0.0.1

install:
	uv sync --group dev
	test -d .git || git init || true

sync:
	uv sync --group dev

lint:
	uv run ruff check tests main.py

lint-fix:
	uv run ruff check --fix tests main.py

test:
	uv run pytest -vv .

start:
	uv run uvicorn main:app --reload --host $(HOST) --port $(PORT)

build:
	uv build

clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .ruff_cache/

update:
	uv sync --upgrade

init: install
