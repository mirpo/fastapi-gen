.PHONY: install start start-ci test lint lint-fix download

MODEL_URL=https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf
OUTPUT_FILE=./models/SmolLM2-135M-Instruct-Q4_K_M.gguf

install: download
	uv sync

start:
	uv run uvicorn llama_app.main:app --reload

start-ci:
	uv run uvicorn llama_app.main:app --workers 1

test:
	uv run pytest

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

lint-fix:
	uv run ruff check --fix src tests
	uv run ruff format src tests

download:
	@mkdir -p models
	@if command -v curl &> /dev/null; then \
		echo "Downloading model with curl..."; \
		curl -L $(MODEL_URL) -o $(OUTPUT_FILE); \
	elif command -v wget &> /dev/null; then \
		echo "Downloading model with wget..."; \
		wget -O $(OUTPUT_FILE) $(MODEL_URL); \
	else \
		echo "Error: Neither curl nor wget is installed."; \
		exit 1; \
	fi
