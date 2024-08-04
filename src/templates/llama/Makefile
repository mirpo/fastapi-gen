.PHONY: init lint start test download

PORT=8000
HOST=127.0.0.1

MODEL_URL=https://huggingface.co/unsloth/gemma-2-it-GGUF/resolve/main/gemma-2-2b-it.q8_0.gguf
OUTPUT_FILE=./models/gemma-2-2b-it.q8_0.gguf

init: requirements.txt download
	test -d venv || python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	test -d .git || git init || true

lint:
	. venv/bin/activate && ruff check tests main.py

test:
	. venv/bin/activate && pytest -vv .

start:
	. venv/bin/activate && uvicorn main:app --reload --host $(HOST) --port $(PORT)

check-curl:
	@if command -v curl &> /dev/null; then \
		echo "curl is installed."; \
		make download-curl; \
	else \
		make check-wget; \
	fi

check-wget:
	@if command -v wget &> /dev/null; then \
		echo "wget is installed."; \
		make download-wget; \
	else \
		echo "Neither curl nor wget is installed. Please install either one of them."; \
		exit 1; \
	fi

download-curl:
	curl -L $(MODEL_URL) -o $(OUTPUT_FILE) 

download-wget:
	wget -L $(OUTPUT_FILE) -O $(MODEL_URL)

download: check-curl
