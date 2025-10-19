.PHONY: init lint start test download

PORT=8000
HOST=127.0.0.1

MODEL_URL=https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf
OUTPUT_FILE=./models/SmolLM2-135M-Instruct-Q4_K_M.gguf

init: requirements.txt download
	test -d venv || python3 -m venv venv
	. venv/bin/activate; \
	pip install --upgrade pip; \
	if [ "$$(uname)" = "Darwin" ]; then \
		echo "Building llama-cpp-python with ARM-safe flags (macOS)"; \
		CFLAGS="-march=armv8.2-a+simd" \
		CXXFLAGS="-march=armv8.2-a+simd" \
		pip install --no-cache-dir --force-reinstall llama-cpp-python==0.3.16; \
		grep -v '^llama-cpp-python' requirements.txt | pip install --no-cache-dir -r /dev/stdin; \
	else \
		echo "Installing normally (non-macOS)"; \
		pip install --no-cache-dir -r requirements.txt; \
	fi; \
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
	wget -O $(OUTPUT_FILE) $(MODEL_URL)

download: check-curl
