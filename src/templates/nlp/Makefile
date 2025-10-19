.PHONY: init lint start test

PORT=8000
HOST=127.0.0.1

init: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel; \
	pip cache purge; \
	pip install --no-cache-dir -r requirements.txt
	test -d .git || git init || true

lint:
	. venv/bin/activate && ruff check tests main.py

test:
	. venv/bin/activate && DEVICE=cpu CI=true pytest -vv .

start:
	. venv/bin/activate && uvicorn main:app --reload --host $(HOST) --port $(PORT)
