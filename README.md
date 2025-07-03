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
# Install
pip install fastapi-gen

# Create your app
fastapi-gen my_app

# Run it
cd my_app && make start
```

**Or use pipx for one-time execution:**
```bash
pipx run fastapi-gen my_app
cd my_app && make start
```

**That's it!** Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your OpenAPI documentation.

> **Platform Support:** Works on macOS and Linux | [Report Issues](https://github.com/mirpo/fastapi-gen/issues/new)

## Why FastAPI Gen?

<div align="center">

| **Focus on Code** | **Production Ready** | **Testing Included** | **Zero Config** |
|:---:|:---:|:---:|:---:|
| Skip boilerplate setup | Enterprise patterns | Real test coverage | Ready-to-run templates |

</div>

---

## Templates Overview

<details>
<summary><strong>Hello World</strong> - Perfect for Learning FastAPI</summary>

**Best for:** Learning FastAPI fundamentals and starting new projects

**Key Features:**
- **REST API Fundamentals** - Complete CRUD with validation
- **Configuration Management** - Both pydantic-settings & dotenv
- **Dependency Injection** - Clean architecture with `Depends()`
- **Background Tasks** - Async processing with logging
- **Exception Handling** - Professional error responses
- **Input Validation** - Advanced Pydantic constraints
- **Health Monitoring** - Built-in health endpoints
- **Complete Tests** - 100% test coverage

[📖 View Details →](src/templates/hello_world/README.md)

</details>

<details>
<summary><strong>Advanced</strong> - Enterprise Production Template</summary>

**Best for:** Production applications with enterprise features

**Key Features:**
- **JWT Authentication** - Registration, login, protected routes
- **Database Integration** - SQLAlchemy 2.0 async (SQLite/PostgreSQL)
- **Rate Limiting** - DDoS protection per endpoint
- **Caching System** - In-memory + Redis integration ready
- **WebSocket Support** - Real-time communication
- **File Upload** - Secure handling + cloud storage ready
- **Enhanced Security** - CORS, validation, production patterns
- **Full Test Suite** - Auth, CRUD, WebSocket, integration

[📖 View Details →](src/templates/advanced/README.md)

</details>

<details>
<summary><strong>NLP</strong> - Comprehensive AI Language Processing</summary>

**Best for:** AI applications with natural language processing

**Key Features:**
- **8 NLP Capabilities** - Summarization, NER, generation, QA, embeddings, sentiment, classification, similarity
- **Production Architecture** - Startup model loading, device auto-detection
- **Smart Configuration** - Environment-based config, multiple models
- **Performance Optimized** - Model caching, concurrent handling, hardware acceleration
- **Production Monitoring** - Health checks, model status, logging
- **Real AI Testing** - Actual model inference validation

[📖 View Details →](src/templates/nlp/README.md)

</details>

<details>
<summary><strong>LangChain</strong> - Modern LLM Integration</summary>

**Best for:** Applications using LangChain for LLM workflows

**Key Features:**
- **Optimized Loading** - Startup caching, memory management
- **Modern Patterns** - Latest LangChain best practices
- **Smart Config** - Auto device detection (CPU/GPU)
- **Production Ready** - Health checks, monitoring, error handling
- **Real Testing** - Actual model inference tests
- **Dual Endpoints** - Text generation & question answering

[📖 View Details →](src/templates/langchain/README.md)

</details>

<details>
<summary><strong>Llama</strong> - Local LLM Powerhouse</summary>

**Best for:** Local LLM inference with llama-cpp-python

**Key Features:**
- **Local LLM Focus** - Optimized for Gemma/Llama GGUF models
- **GPU Acceleration** - Auto GPU detection, configurable layers
- **Advanced Config** - Context windows, threading, performance tuning
- **Production Ready** - Lifecycle management, health monitoring
- **Real Testing** - Actual model inference validation
- **Easy Setup** - Auto model download, optimized defaults

> **Requirements:** ~4GB model download + 4GB+ RAM

[📖 View Details →](src/templates/llama/README.md)

</details>

---

## Template Comparison

| Template | Best For | Complexity | AI/ML | Database | Auth |
|----------|----------|------------|--------|----------|------|
| **Hello World** | Learning, Simple APIs | ⭐ | ❌ | ❌ | ❌ |
| **Advanced** | Production Apps | ⭐⭐⭐ | ❌ | ✅ | ✅ |
| **NLP** | AI Text Processing | ⭐⭐⭐⭐ | ✅ | ❌ | ❌ |
| **LangChain** | LLM Workflows | ⭐⭐⭐⭐ | ✅ | ❌ | ❌ |
| **Llama** | Local LLM | ⭐⭐⭐⭐⭐ | ✅ | ❌ | ❌ |

## What You Get Out of the Box

<div align="center">

**Zero Configuration** • **Production Patterns** • **Complete Testing** • **Code Quality** • **Auto Documentation** • **Deployment Ready**

</div>

**Focus on Your Code, Not Setup**

All dependencies (FastAPI, Pydantic, Pytest, etc.) are preconfigured. Just create and run:

```bash
fastapi-gen my_app    # Create
cd my_app            # Enter  
make start           # Run!
```

**Every Template Includes:**
- **Ready-to-run** development environment
- **Industry-standard** project structure
- **Comprehensive** test suites with examples
- **Ruff** linting and formatting
- **Auto-generated** OpenAPI documentation
- **Makefile** with common development commands

## Creating an App

**You'll need to have Python 3.12+ or later version on your local development machine**. We recommend using the latest LTS version. You can use [pyenv](https://github.com/pyenv/pyenv) (macOS/Linux) to switch Python versions between different projects.

### Basic template

```console
pip3 install fastapi-gen
fastapi-gen my_app
```

or

```console
pip3 install fastapi-gen
fastapi-gen my_app --template hello_world
```

### Advanced template

```console
pip3 install fastapi-gen
fastapi-gen my_app --template advanced
```

### NLP template

```console
pip install fastapi-gen
fastapi-gen my_app --template nlp
```

### Langchain template

```console
pip install fastapi-gen
fastapi-gen my_app --template Langchain
```

### Llama template

```console
pip install fastapi-gen
fastapi-gen my_app --template llama
```

Inside the newly created project, you can run some built-in commands:

### `make start`

Runs the app in development mode.<br>
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`

Runs tests.<br>
By default, runs tests related to files changed since the last commit.

## License

`fastapi-gen` is distributed under the terms of the [MIT](https://github.com/mirpo/fastapi-gen/blob/main/LICENSE) license.