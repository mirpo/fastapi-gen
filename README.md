<div align="center">
  
# FastAPI Gen

**Create production-ready FastAPI applications in seconds**

*From simple APIs to LLM-enabled applications, all without build configuration.*

<p align="center">
  <a href="https://github.com/mirpo/fastapi-gen/actions/workflows/test.yml?query=workflow%3Atest+event%3Apush+branch%main">
    <img src="https://github.com/mirpo/fastapi-gen/actions/workflows/test.yml/badge.svg?branch=main" alt="Test Status">
  </a>
  <a href="https://pypi.org/project/fastapi-gen">
    <img src="https://img.shields.io/pypi/v/fastapi-gen?color=%2334D058&label=pypi" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/fastapi-gen">
    <img src="https://img.shields.io/pypi/pyversions/fastapi-gen.svg?color=%2334D058" alt="Python versions">
  </a>
  <a href="https://pypi.org/project/fastapi-gen">
    <img src="https://img.shields.io/pypi/dm/fastapi-gen?color=blue" alt="Downloads">
  </a>
  <a href="https://github.com/mirpo/fastapi-gen/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </a>
</p>

</div>

## Quick Start

Get a fully functional FastAPI app running in **30 seconds**:

```bash
# Recommended: using uvx (no installation needed)
uvx fastapi-gen my_app
cd my_app && make start
```

**Or install with uv:**
```bash
uv tool install fastapi-gen
fastapi-gen my_app
cd my_app && make start
```

**Or use pip:**
```bash
pip install fastapi-gen
fastapi-gen my_app
cd my_app && make start
```

**That's it!** Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your OpenAPI documentation.

> **Platform Support:** Works on macOS and Linux | [Report Issues](https://github.com/mirpo/fastapi-gen/issues/new)

## Why FastAPI Gen?

**Focus on Code** - Skip boilerplate setup and start building
**Production Ready** - Enterprise patterns and best practices built-in
**Testing Included** - Real test coverage from day one
**Zero Config** - Ready-to-run templates that just work

---

## Templates Overview

<details>
<summary><strong>Hello World</strong> - Perfect for Learning FastAPI</summary>

**Best for:** Learning FastAPI fundamentals and starting new projects

**Key Features:**
- REST API fundamentals with complete CRUD
- Configuration management (pydantic-settings & dotenv)
- Dependency injection and clean architecture
- Background tasks and exception handling
- Input validation and health monitoring
- Complete test coverage

[View Details →](packages/template-hello-world/README.md)

</details>

<details>
<summary><strong>Advanced</strong> - Enterprise Production Template</summary>

**Best for:** Production applications with enterprise features

**Key Features:**
- JWT authentication with registration and login
- Database integration with SQLAlchemy 2.0 async
- Rate limiting and caching system
- WebSocket support and file upload
- Enhanced security and CORS configuration
- Full test suite

[View Details →](packages/template-advanced/README.md)

</details>

<details>
<summary><strong>NLP</strong> - Comprehensive AI Language Processing</summary>

**Best for:** AI applications with natural language processing

**Key Features:**
- 8 NLP capabilities: summarization, NER, generation, QA, embeddings, sentiment, classification, similarity
- Production architecture with startup model loading
- Smart configuration and device auto-detection
- Performance optimized with model caching
- Real AI testing with actual inference

[View Details →](packages/template-nlp/README.md)

</details>

<details>
<summary><strong>LangChain</strong> - Modern LLM Integration</summary>

**Best for:** Applications using LangChain for LLM workflows

**Key Features:**
- Optimized loading with startup caching
- Modern LangChain patterns and best practices
- Smart config with auto device detection
- Production ready with health checks
- Dual endpoints: text generation and question answering

[View Details →](packages/template-langchain/README.md)

</details>

<details>
<summary><strong>Llama</strong> - Local LLM Powerhouse</summary>

**Best for:** Local LLM inference with llama-cpp-python

**Key Features:**
- Local LLM focus optimized for Gemma/Llama GGUF models
- GPU acceleration with auto detection
- Advanced config for context windows and threading
- Production ready with lifecycle management
- Easy setup with auto model download

> **Requirements:** ~4GB model download + 4GB+ RAM

[View Details →](packages/template-llama/README.md)

</details>

---

## Template Comparison

| Template        | Best For              | Complexity | AI/ML | Database | Auth |
| --------------- | --------------------- | ---------- | ----- | -------- | ---- |
| **Hello World** | Learning, Simple APIs | Basic      | No    | No       | No   |
| **Advanced**    | Production Apps       | Medium     | No    | Yes      | Yes  |
| **NLP**         | AI Text Processing    | Advanced   | Yes   | No       | No   |
| **LangChain**   | LLM Workflows         | Advanced   | Yes   | No       | No   |
| **Llama**       | Local LLM             | Advanced   | Yes   | No       | No   |

## What You Get Out of the Box

<div align="center">

**Zero Configuration** • **Production Patterns** • **Complete Testing** • **Code Quality** • **Auto Documentation** • **Deployment Ready**

</div>

**Focus on Your Code, Not Setup**

All dependencies (FastAPI, Pydantic, Pytest, etc.) are preconfigured. Just create and run:

```bash
fastapi-gen my_app   # Create
cd my_app            # Enter  
make start           # Run!
```

**Every Template Includes:**
- Ready-to-run development environment
- Industry-standard project structure
- Comprehensive test suites with examples
- Ruff linting and formatting
- Auto-generated OpenAPI documentation
- Makefile with common development commands

## Installation & Usage

**You'll need to have Python 3.11+ or later version on your local development machine**. We recommend using the latest version. You can use [uv](https://docs.astral.sh/uv/) for Python version management and project workflows.

### Choose Your Template

```bash
# Default (hello_world)
uvx fastapi-gen my_app

# Or specify a template
uvx fastapi-gen my_app --template <template-name>
```

Available templates: `hello_world`, `advanced`, `nlp`, `langchain`, `llama`

### Built-in Commands

Inside the newly created project, you can run:

### `make start`

Runs the app in development mode.<br>
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`

Runs tests.<br>
By default, runs tests related to files changed since the last commit.

## License

`fastapi-gen` is distributed under the terms of the [MIT](https://github.com/mirpo/fastapi-gen/blob/main/LICENSE) license.