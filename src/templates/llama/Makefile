.PHONY: install sync lint lint-fix test start build clean update download

PORT=8000
HOST=127.0.0.1

MODEL_URL=https://huggingface.co/bartowski/SmolLM2-135M-Instruct-GGUF/resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf
OUTPUT_FILE=./models/SmolLM2-135M-Instruct-Q4_K_M.gguf

install: download
	CMAKE_ARGS="-DLLAMA_METAL=OFF -DGGML_METAL=OFF -DGGML_BLAS=OFF -DGGML_CUBLAS=OFF -DGGML_OPENMP=OFF -DGGML_NATIVE=OFF" \
	FORCE_CMAKE=1 \
	python3 -m pip wheel --no-cache-dir --force-reinstall llama-cpp-python -w ./wheels

	uv sync --group dev --find-links ./wheels
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
