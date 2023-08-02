.PHONY: init lint start test

PORT=8000
HOST=127.0.0.1

init: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	test -d .git || git init || true

lint:
	. venv/bin/activate && black --check src
	. venv/bin/activate && ruff check src

test:
	. venv/bin/activate && pytest .

start:
	. venv/bin/activate && uvicorn main:app --reload --host $(HOST) --port $(PORT)
