# Full UV Monorepo Migration - Simplified UV-Native Architecture

## Executive Summary

This document outlines the migration of `fastapi-gen` to a **true UV monorepo** with UV-native templates. The key insight: templates are proper UV projects that are bundled directly into the CLI wheel using hatch's `include` directive. **No sync scripts needed.**

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Current vs Target State](#current-vs-target-state)
3. [Key Design Decisions](#key-design-decisions)
4. [Detailed Migration Plan](#detailed-migration-plan)
5. [Benefits](#benefits)
6. [User Experience Changes](#user-experience-changes)
7. [Testing Strategy](#testing-strategy)
8. [Timeline](#timeline)

## Architecture Overview

### The Core Concept

**Templates are UV projects, bundled as-is into the CLI wheel.**

- Templates live in `packages/template-*/` as proper UV projects
- Hatch includes them: `include = ["src", "packages/template-*"]`
- CLI copies entire template package to user's directory
- Users get UV-native projects with `pyproject.toml`
- **No sync scripts, no flattening, no transformation**

### Structure

```
fastapi-gen/
├── pyproject.toml              # Workspace root + CLI package (combined)
├── uv.lock                     # Single lockfile for all dependencies
├── README.md
├── Makefile                    # Monorepo commands
├── .github/
│   └── workflows/
│       └── test.yml
├── src/
│   └── cli/                    # CLI package code
│       ├── __init__.py
│       └── __main__.py
└── packages/                   # Template packages (workspace members)
    ├── template-hello-world/
    │   ├── pyproject.toml      # Full UV project config
    │   ├── README.md
    │   ├── src/
    │   │   └── hello_world/
    │   │       ├── __init__.py
    │   │       └── main.py
    │   └── tests/
    │       ├── __init__.py
    │       └── test_main.py
    ├── template-advanced/
    │   ├── pyproject.toml
    │   ├── README.md
    │   ├── src/
    │   │   └── advanced/
    │   │       └── main.py
    │   └── tests/
    ├── template-nlp/
    ├── template-langchain/
    └── template-llama/
```

## Current vs Target State

### Current State

**Structure:**
```
fastapi-gen/
├── pyproject.toml
├── uv.lock
└── src/
    ├── cli/
    │   └── __main__.py
    └── templates/              # Resources
        ├── hello_world/
        │   ├── main.py         # Flat structure
        │   ├── requirements.txt
        │   ├── Makefile
        │   └── tests/
        └── ...
```

**User experience:**
```bash
fastapi-gen my_app
cd my_app
make init      # Creates venv, pip install
make start     # Activates venv, uvicorn
make test      # Activates venv, pytest
```

### Target State

**Structure:**
```
fastapi-gen/
├── pyproject.toml              # Workspace + CLI
├── uv.lock
├── src/cli/
└── packages/
    ├── template-hello-world/   # Proper package
    │   ├── pyproject.toml      # UV project
    │   ├── src/hello_world/    # Package structure
    │   └── tests/
    └── ...
```

**User experience:**
```bash
fastapi-gen my_app
cd my_app
uv sync          # Install dependencies
uv run start     # Run server (script defined in pyproject.toml)
uv run pytest    # Run tests
```

## Key Design Decisions

### Decision 1: No Sync Script

**Approach:** Use hatch's `include` to bundle template packages directly.

```toml
[tool.hatch.build]
include = [
  "src/cli",
  "packages/template-hello-world",
  "packages/template-advanced",
  "packages/template-nlp",
  "packages/template-langchain",
  "packages/template-llama"
]
```

**Benefits:**
- Simpler build process
- No transformation logic
- Templates are always in sync
- One source of truth

### Decision 2: UV-Native Templates

**Approach:** Generated projects are UV projects with `pyproject.toml` only.

**Template pyproject.toml:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-world-app"
version = "0.1.0"
description = "FastAPI Hello World application"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "python-dotenv==1.1.1",
  "pydantic-settings==2.11.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn hello_world.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
test = "pytest -vv"
```

**Benefits:**
- Modern Python packaging
- No Makefiles needed
- Cleaner dependency management
- Future-proof

### Decision 3: Proper Package Structure

**Approach:** Templates use proper Python package structure.

```
template-hello-world/
├── pyproject.toml
├── src/
│   └── hello_world/        # Package name
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

**Benefits:**
- Better imports
- IDE support
- Proper namespacing
- Testable in monorepo

### Decision 4: Combined Root pyproject.toml

**Approach:** Root pyproject.toml is both workspace root AND CLI package.

```toml
[project]
name = "fastapi-gen"
# ... CLI package config

[tool.uv.workspace]
members = [
  "packages/template-hello-world",
  "packages/template-advanced",
  # ...
]
```

**Benefits:**
- Simpler structure
- Single version source (hatch-vcs)
- CLI is the publishable artifact

## Detailed Migration Plan

### Phase 1: Create Packages Structure

**Goal:** Restructure repository with `packages/` directory for templates.

#### 1.1 Create Directory Structure

```bash
mkdir -p packages/template-hello-world/src/hello_world/tests
mkdir -p packages/template-advanced/src/advanced/tests
mkdir -p packages/template-nlp/src/nlp/tests
mkdir -p packages/template-langchain/src/langchain_app/tests
mkdir -p packages/template-llama/src/llama_app/tests
```

#### 1.2 Move Template Code

For each template (using hello_world as example):

```bash
# Move main.py into package
mv src/templates/hello_world/main.py packages/template-hello-world/src/hello_world/

# Create __init__.py
touch packages/template-hello-world/src/hello_world/__init__.py

# Move tests
mv src/templates/hello_world/tests/* packages/template-hello-world/tests/

# Copy supporting files
cp src/templates/hello_world/README.md packages/template-hello-world/
cp src/templates/hello_world/.env_dev packages/template-hello-world/ 2>/dev/null || true
cp src/templates/hello_world/ruff.toml packages/template-hello-world/ 2>/dev/null || true
```

**Repeat for all templates:** advanced, nlp, langchain, llama

#### 1.3 Keep src/cli/ for CLI Code

```bash
# CLI code stays in src/cli/
# It will be the main package code
```

### Phase 2: Create UV-Native Template Projects

**Goal:** Each template becomes a proper UV project with pyproject.toml.

#### 2.1 Template: hello_world

**File:** `packages/template-hello-world/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hello-world-app"
version = "0.1.0"
description = "FastAPI Hello World application"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "python-dotenv==1.1.1",
  "pydantic-settings==2.11.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn hello_world.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
lint-fix = "ruff check --fix src tests && ruff format src tests"
test = "pytest -vv"

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I"]
```

**File:** `packages/template-hello-world/README.md`

```markdown
# Hello World FastAPI Application

A simple FastAPI application demonstrating basic concepts.

## Setup

```bash
uv sync
```

## Running

```bash
uv run start
```

Visit http://localhost:8000/docs for API documentation.

## Testing

```bash
uv run test
```

## Linting

```bash
uv run lint
```
```

**Update tests:** `packages/template-hello-world/tests/test_main.py`

```python
from fastapi.testclient import TestClient
from hello_world.main import app

client = TestClient(app)

def test_root_200():
    response = client.get("/")
    assert response.is_success
    assert response.json() == {"message": "Hello World"}

def test_health_check_200():
    response = client.get("/health")
    assert response.is_success
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert "timestamp" in json_response
```

#### 2.2 Template: advanced

**File:** `packages/template-advanced/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "advanced-fastapi-app"
version = "0.1.0"
description = "Advanced FastAPI application with auth, database, etc."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "python-dotenv==1.1.1",
  "pydantic-settings==2.11.0",
  "sqlalchemy==2.0.44",
  "python-jose[cryptography]==3.5.0",
  "bcrypt==5.0.0",
  "slowapi==0.1.9",
  "python-multipart==0.0.20",
  "websockets==15.0.1",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
  "pytest-asyncio==1.2.0",
]

[project.scripts]
start = "uvicorn advanced.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
lint-fix = "ruff check --fix src tests && ruff format src tests"
test = "pytest -vv"
```

#### 2.3 Template: nlp

**File:** `packages/template-nlp/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "nlp-fastapi-app"
version = "0.1.0"
description = "FastAPI application with NLP capabilities"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "transformers[torch]==4.57.1",
  "sentence-transformers==5.1.1",
  "pydantic-settings==2.11.0",
  "torch==2.9.0",
  "accelerate==1.11.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn nlp.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
test = "pytest -vv"
```

#### 2.4 Template: langchain

**File:** `packages/template-langchain/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "langchain-fastapi-app"
version = "0.1.0"
description = "FastAPI application with LangChain integration"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "transformers[torch]==4.57.1",
  "pydantic-settings==2.11.0",
  "torch==2.9.0",
  "langchain==1.0.1",
  "langchain-community==0.4",
  "langchain-huggingface==1.0.0",
  "accelerate==1.11.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "pytest-asyncio==1.2.0",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn langchain_app.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
test = "pytest -vv"
```

#### 2.5 Template: llama

**File:** `packages/template-llama/pyproject.toml`

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "llama-fastapi-app"
version = "0.1.0"
description = "FastAPI application with local LLM (llama.cpp)"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
  "llama-cpp-python==0.3.16",
  "pydantic-settings==2.11.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn llama_app.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
test = "pytest -vv"
download-model = "python -c 'from llama_app.main import download_model; download_model()'"
```

### Phase 3: Update Root Workspace Configuration

**Goal:** Configure workspace and CLI package in root pyproject.toml.

#### 3.1 Update Root pyproject.toml

**File:** `pyproject.toml`

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "fastapi-gen"
dynamic = ["version"]
description = "Set up a modern REST API by running one command."
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
keywords = [
  "fastapi",
  "cli",
  "generator",
  "uv",
  "template",
]
authors = [
  { name = "Miroslav Pokrovskii", email = "miroslavpokrovskiy@gmail.com" },
]
classifiers = [
  "Intended Audience :: Information Technology",
  "Intended Audience :: System Administrators",
  "Intended Audience :: Developers",
  "Operating System :: OS Independent",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Topic :: Software Development :: Libraries",
  "Topic :: Software Development :: Code Generators",
  "Topic :: Software Development",
  "Typing :: Typed",
  "Development Status :: 4 - Beta",
  "Environment :: Console",
  "Framework :: FastAPI",
  "License :: OSI Approved :: MIT License",
]
dependencies = [
  "click==8.3.0",
  "colorama==0.4.6",
  "importlib_resources==6.5.2",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "coverage[toml]==7.11.0",
]

[project.urls]
Documentation = "https://github.com/mirpo/fastapi-gen#readme"
Issues = "https://github.com/mirpo/fastapi-gen/issues"
Source = "https://github.com/mirpo/fastapi-gen"

[project.scripts]
fastapi-gen = "cli.__main__:main"

[tool.hatch.version]
source = "vcs"

[tool.hatch.build]
include = [
  "src/cli/**/*.py",
  "packages/template-hello-world/**/*",
  "packages/template-advanced/**/*",
  "packages/template-nlp/**/*",
  "packages/template-langchain/**/*",
  "packages/template-llama/**/*",
]
exclude = [
  "**/__pycache__",
  "**/*.pyc",
  "**/.venv",
  "**/venv",
  "**/.pytest_cache",
  "**/.ruff_cache",
  "**/*.egg-info",
  "**/uv.lock",
  "**/.git",
]

[tool.hatch.build.targets.wheel]
sources = ["src"]
packages = ["src/cli"]

[tool.hatch.build.targets.wheel.force-include]
"packages/template-hello-world" = "cli/templates/template-hello-world"
"packages/template-advanced" = "cli/templates/template-advanced"
"packages/template-nlp" = "cli/templates/template-nlp"
"packages/template-langchain" = "cli/templates/template-langchain"
"packages/template-llama" = "cli/templates/template-llama"

[tool.uv.workspace]
members = [
  "packages/template-hello-world",
  "packages/template-advanced",
  "packages/template-nlp",
  "packages/template-langchain",
  "packages/template-llama",
]

[tool.black]
target-version = ["py311"]
line-length = 120

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["ALL"]
ignore = [
  "ANN",
  "D",
  "S105", "S106", "S107",
  "C901", "PLR0911", "PLR0912", "PLR0913", "PLR0915",
  "PTH",
  "S603", "S607",
  "S101",
  "PLR2004",
  "COM812",
]
```

### Phase 4: Update CLI Logic

**Goal:** Update CLI to copy template packages and rename them.

#### 4.1 Update CLI Code

**File:** `src/cli/__main__.py`

```python
import os
import re
import shutil
import subprocess
import sys
from importlib import resources
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

try:
    __version__ = version("fastapi-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

_pattern = r"^[a-zA-Z0-9_]+$"
_choices = ["hello_world", "advanced", "nlp", "langchain", "llama"]

# Template name mapping
_template_map = {
    "hello_world": ("template-hello-world", "hello_world"),
    "advanced": ("template-advanced", "advanced"),
    "nlp": ("template-nlp", "nlp"),
    "langchain": ("template-langchain", "langchain_app"),
    "llama": ("template-llama", "llama_app"),
}


def is_valid_name(name) -> bool:
    return re.match(_pattern, name) is not None


def copy_template(template_dir: Path, dest_path: Path):
    """Recursively copy template directory, excluding dev artifacts."""
    exclude_patterns = {
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        ".git",
        "uv.lock",
    }

    for item in template_dir.iterdir():
        if item.name in exclude_patterns:
            continue

        dest_item = dest_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, ignore=shutil.ignore_patterns(*exclude_patterns))
        else:
            shutil.copy2(item, dest_item)


def rename_package_in_pyproject(pyproject_path: Path, new_name: str):
    """Rename the package in pyproject.toml."""
    content = pyproject_path.read_text()

    # Replace name field
    content = re.sub(
        r'name\s*=\s*"[^"]+',
        f'name = "{new_name}',
        content,
        count=1
    )

    pyproject_path.write_text(content)


def update_scripts_in_pyproject(pyproject_path: Path, old_module: str, new_module: str):
    """Update script module names in pyproject.toml."""
    content = pyproject_path.read_text()

    # Replace module names in scripts
    content = content.replace(f"{old_module}.", f"{new_module}.")

    pyproject_path.write_text(content)


def rename_src_directory(dest_path: Path, old_name: str, new_name: str):
    """Rename the src/{old_name} directory to src/{new_name}."""
    old_src = dest_path / "src" / old_name
    new_src = dest_path / "src" / new_name

    if old_src.exists():
        old_src.rename(new_src)


def update_imports_in_tests(tests_dir: Path, old_module: str, new_module: str):
    """Update import statements in test files."""
    if not tests_dir.exists():
        return

    for test_file in tests_dir.glob("*.py"):
        if test_file.name == "__init__.py":
            continue

        content = test_file.read_text()
        content = content.replace(f"from {old_module}.", f"from {new_module}.")
        content = content.replace(f"import {old_module}", f"import {new_module}")
        test_file.write_text(content)


@click.command()
@click.option("-t", "--template", default="hello_world", type=click.Choice(_choices), help="template")
@click.argument("name")
@click.version_option(version=__version__, prog_name="fastapi-gen")
def main(name: str, template: str):
    """This script creates new FastAPI project with NAME using TEMPLATE."""
    if not is_valid_name(name):
        click.echo(f"Error. Invalid name {name}. Name must match: {_pattern}")
        sys.exit(1)

    click.echo(f"Creating new project: '{name}' using template '{template}'...")

    dest_path = Path.cwd() / name
    if dest_path.exists():
        click.echo(f"Error. Folder {dest_path} already exists.")
        sys.exit(1)

    # Get template info
    template_package_name, template_module_name = _template_map[template]

    # Get template directory from installed package
    try:
        template_files = resources.files("cli").joinpath("templates").joinpath(template_package_name)
    except (FileNotFoundError, AttributeError):
        click.echo(f"Error. Template {template} not found in installation.")
        sys.exit(1)

    # Create destination directory
    dest_path.mkdir(parents=True)

    # Copy template
    click.echo("Copying template files...")
    copy_template(Path(template_files), dest_path)

    # Rename package in pyproject.toml
    pyproject_path = dest_path / "pyproject.toml"
    if pyproject_path.exists():
        click.echo(f"Renaming package to '{name}'...")
        rename_package_in_pyproject(pyproject_path, name)
        update_scripts_in_pyproject(pyproject_path, template_module_name, name)

    # Rename src directory
    click.echo(f"Renaming module to '{name}'...")
    rename_src_directory(dest_path, template_module_name, name)

    # Update imports in tests
    tests_dir = dest_path / "tests"
    if tests_dir.exists():
        update_imports_in_tests(tests_dir, template_module_name, name)

    # Initialize git repository
    os.chdir(dest_path)
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # Git might not be available

    # Success message
    welcome_message = f"""
{click.style("Success!", fg="green", bold=True)} Created {name} at {dest_path}

Inside that directory, you can run several commands:

    {click.style("uv sync", fg="blue", bold=True)}
    Install dependencies

    {click.style("uv run start", fg="blue", bold=True)}
    Start the development server

    {click.style("uv run test", fg="blue", bold=True)}
    Run tests

    {click.style("uv run lint", fg="blue", bold=True)}
    Run linter

We suggest that you begin by typing:

    {click.style(f"cd {name}", fg="blue", bold=True)}
    {click.style("uv sync", fg="blue", bold=True)}
    {click.style("uv run start", fg="blue", bold=True)}

Then open {click.style("http://localhost:8000/docs", fg="cyan")} to see your API.

{click.style("Happy hacking!", fg="yellow", blink=True, bold=True)}
"""
    click.echo(welcome_message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Phase 5: Update CI/CD and Documentation

#### 5.1 Update GitHub Actions

**File:** `.github/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  lint-and-test-monorepo:
    name: Lint and Test Monorepo
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest]
        python-version: ["3.12", "3.13"]

    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0  # Need full history for hatch-vcs

      - name: Set up uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: ${{ matrix.python-version }}
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Install dependencies
        run: uv sync

      - name: Lint CLI
        run: uv run ruff check src/cli

      - name: Test templates in monorepo
        run: |
          uv run pytest packages/template-hello-world/tests -v
          uv run pytest packages/template-advanced/tests -v
          uv run pytest packages/template-nlp/tests -v
          uv run pytest packages/template-langchain/tests -v
          uv run pytest packages/template-llama/tests -v

      - name: Build CLI package
        run: uv build

      - name: Upload wheel artifact
        uses: actions/upload-artifact@v4
        with:
          name: wheel-${{ matrix.os }}-py${{ matrix.python-version }}
          path: dist/*.whl

  test-generated-projects:
    name: Test Generated Projects
    needs: lint-and-test-monorepo
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest]
        python-version: ["3.12"]
        template: [hello_world, advanced, nlp, langchain, llama]

    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Set up uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync

      - name: Generate project from ${{ matrix.template }}
        run: |
          uv run fastapi-gen test_${{ matrix.template }} --template ${{ matrix.template }}

      - name: Test generated project
        run: |
          cd test_${{ matrix.template }}
          uv sync
          uv run lint
          uv run test
```

#### 5.2 Update Root Makefile

**File:** `Makefile`

```makefile
.PHONY: install lint lint-fix test test-all test-templates build clean

# Install all workspace dependencies
install:
	uv sync

# Lint CLI code
lint:
	uv run ruff check src/cli

# Lint and fix
lint-fix:
	uv run ruff check --fix src/cli
	uv run ruff format src/cli

# Test CLI (if we add CLI tests)
test:
	@echo "CLI tests would go here"

# Test all templates in monorepo
test-templates:
	@echo "Testing hello_world..."
	uv run pytest packages/template-hello-world/tests -v
	@echo "Testing advanced..."
	uv run pytest packages/template-advanced/tests -v
	@echo "Testing nlp..."
	uv run pytest packages/template-nlp/tests -v
	@echo "Testing langchain..."
	uv run pytest packages/template-langchain/tests -v
	@echo "Testing llama..."
	uv run pytest packages/template-llama/tests -v

# Test everything
test-all: test test-templates

# Build CLI package
build:
	uv build

# Clean artifacts
clean:
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Run specific template locally
run-hello:
	cd packages/template-hello-world && uv run start

run-advanced:
	cd packages/template-advanced && uv run start

run-nlp:
	cd packages/template-nlp && uv run start

run-langchain:
	cd packages/template-langchain && uv run start

run-llama:
	cd packages/template-llama && uv run start
```

#### 5.3 Update README.md

Add development section to README:

```markdown
## Development

This project uses a UV workspace monorepo structure.

### Setup

```bash
# Clone repository
git clone https://github.com/mirpo/fastapi-gen.git
cd fastapi-gen

# Install all dependencies
uv sync
```

### Project Structure

```
fastapi-gen/
├── src/cli/              # CLI package code
└── packages/             # Template packages (workspace members)
    ├── template-hello-world/
    ├── template-advanced/
    ├── template-nlp/
    ├── template-langchain/
    └── template-llama/
```

### Development Workflow

#### Working on Templates

```bash
# Navigate to template
cd packages/template-hello-world

# Run tests
uv run test

# Run locally
uv run start

# Lint
uv run lint
```

#### Testing CLI

```bash
# From root
uv run fastapi-gen my_app --template hello_world

# Test generated project
cd my_app
uv sync
uv run start
```

#### Running All Tests

```bash
# Test all templates
make test-templates

# Test everything
make test-all
```

### Building

```bash
# Build CLI package
make build

# Output: dist/fastapi_gen-*.whl

# Test installation
pip install dist/fastapi_gen-*.whl
fastapi-gen test_app
```

### Release Process

1. Update version: `git tag v1.2.3`
2. Run tests: `make test-all`
3. Build: `make build`
4. Publish: `uv publish`
```

#### 5.4 Create CONTRIBUTING.md

**File:** `CONTRIBUTING.md`

```markdown
# Contributing to fastapi-gen

## Monorepo Structure

fastapi-gen uses a UV workspace monorepo where:
- CLI code lives in `src/cli/`
- Templates are workspace members in `packages/template-*/`
- All templates are bundled into the CLI wheel

## Adding a New Template

### 1. Create Template Package

```bash
mkdir -p packages/template-mytemplate/src/mytemplate/tests
```

### 2. Create pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mytemplate-app"
version = "0.1.0"
description = "My custom FastAPI template"
requires-python = ">=3.11"
dependencies = [
  "fastapi==0.119.1",
  "uvicorn==0.38.0",
]

[dependency-groups]
dev = [
  "ruff==0.14.1",
  "pytest==8.4.2",
  "httpx==0.28.1",
]

[project.scripts]
start = "uvicorn mytemplate.main:app --reload --host 127.0.0.1 --port 8000"
lint = "ruff check src tests"
test = "pytest -vv"
```

### 3. Create Template Code

- `src/mytemplate/main.py`: FastAPI application
- `tests/test_main.py`: Tests
- `README.md`: Template documentation

### 4. Add to Workspace

Edit root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = [
  # ... existing templates
  "packages/template-mytemplate",
]

[tool.hatch.build.targets.wheel.force-include]
# ... existing templates
"packages/template-mytemplate" = "cli/templates/template-mytemplate"
```

### 5. Update CLI

Edit `src/cli/__main__.py`:

```python
_choices = ["hello_world", "advanced", "nlp", "langchain", "llama", "mytemplate"]

_template_map = {
    # ... existing mappings
    "mytemplate": ("template-mytemplate", "mytemplate"),
}
```

### 6. Test

```bash
# Sync dependencies
uv sync

# Test template in monorepo
cd packages/template-mytemplate
uv run test

# Test CLI generation
cd ../..
uv run fastapi-gen test_mytemplate --template mytemplate
cd test_mytemplate
uv sync && uv run test
```

## Testing

### Test Template in Monorepo

```bash
cd packages/template-mytemplate
uv run pytest -v
```

### Test Generated Project

```bash
uv run fastapi-gen test_app --template mytemplate
cd test_app
uv sync
uv run test
```

## Code Style

We use Ruff:

```bash
make lint      # Check
make lint-fix  # Fix
```

## Pull Request Process

1. Create branch: `git checkout -b feature/my-feature`
2. Make changes to templates or CLI
3. Run tests: `make test-all`
4. Commit: `git commit -m "feat: add feature"`
5. Push and create PR
```

## Benefits

### For Developers

✅ **True UV Monorepo** - Proper workspace with single lockfile
✅ **No Sync Scripts** - Templates bundled directly by hatch
✅ **Easy Testing** - Test templates without generating projects
✅ **Better IDE Support** - Proper packages with imports
✅ **Shared Dependencies** - Dev tools shared across workspace

### For Users

✅ **Modern Tooling** - UV-native projects
✅ **Simpler Commands** - `uv sync`, `uv run start`
✅ **Better DX** - Project scripts in pyproject.toml
✅ **Future-Proof** - UV is the future of Python

### For Maintenance

✅ **Easier Updates** - Modify templates as packages
✅ **Better CI** - Fast monorepo tests
✅ **Clear Structure** - Proper separation of concerns
✅ **Type Safety** - Proper Python packages

## User Experience Changes

### Before (Traditional)

```bash
fastapi-gen my_app
cd my_app
make init      # Creates venv, pip install -r requirements.txt
make start     # Activates venv, uvicorn
make test      # Activates venv, pytest
make lint      # Activates venv, ruff
```

### After (UV-Native)

```bash
fastapi-gen my_app
cd my_app
uv sync        # Install from pyproject.toml
uv run start   # Run server (script in pyproject.toml)
uv run test    # Run tests
uv run lint    # Run linter
```

**Key differences:**
- No `Makefile` or `requirements.txt`
- All config in `pyproject.toml`
- Use `uv` instead of `make`
- Cleaner, more standard Python workflow

## Testing Strategy

### 1. Monorepo Tests

```bash
# Test all templates in monorepo
make test-templates

# Fast, runs in single environment
```

### 2. Integration Tests

```bash
# Generate projects and test them
uv run fastapi-gen test_hello --template hello_world
cd test_hello && uv sync && uv run test
```

### 3. CI/CD

- Lint CLI code
- Test all templates in monorepo (parallel)
- Build wheel
- Test generated projects (parallel matrix)

## Migration Timeline

**Day 1: Structure**
- Create `packages/` directories
- Move template code into package structure
- Create template pyproject.toml files

**Day 2: Configuration**
- Update root pyproject.toml (workspace + build)
- Remove Makefiles from templates
- Add project scripts to template pyproject.toml

**Day 3: CLI Updates**
- Update CLI logic for package copying
- Handle package renaming
- Test CLI locally

**Day 4: CI/CD & Docs**
- Update GitHub Actions
- Update README and CONTRIBUTING
- Create root Makefile

**Day 5: Testing & Release**
- Full integration testing
- Fix any issues
- Build and test wheel
- Tag and release

## Rollback Plan

If migration fails:

1. Revert to pre-migration commit: `git reset --hard <commit>`
2. Or checkout tag: `git checkout pre-migration`
3. Original structure is preserved in git history

## Success Criteria

- [ ] UV workspace syncs without errors
- [ ] All template tests pass in monorepo
- [ ] CLI builds successfully
- [ ] Wheel includes all template files
- [ ] Generated projects work with UV
- [ ] CI/CD passes all tests
- [ ] Documentation is complete
- [ ] Users can easily transition to UV

## Conclusion

This migration simplifies the architecture significantly:

1. **No sync scripts** - Hatch handles bundling
2. **UV-native templates** - Users get modern projects
3. **Proper monorepo** - True workspace structure
4. **Better DX** - Both for developers and users

The result is a cleaner, more maintainable codebase that generates modern Python projects using UV.
