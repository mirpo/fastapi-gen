# FastApi Gen

Create production-ready FastAPI applications with modern best practices - from simple APIs to LLM-enabled applications, all without build configuration.

<a href="https://github.com/mirpo/fastapi-gen/actions/workflows/test.yml?query=workflow%3Atest+event%3Apush+branch%main" target="_blank"><img src="https://github.com/mirpo/fastapi-gen/actions/workflows/test.yml/badge.svg?branch=main" alt="Test"></a>
<a href="https://pypi.org/project/fastapi-gen" target="_blank"><img src="https://img.shields.io/pypi/v/fastapi-gen?color=%2334D058&label=pypi%20package" alt="Package version"></a>
<a href="https://pypi.org/project/fastapi-gen" target="_blank"><img src="https://img.shields.io/pypi/pyversions/fastapi-gen.svg?color=%2334D058" alt="Supported Python versions"></a>

---

FastApi Gen works on macOS and Linux.<br>
If something doesn’t work, please [file an issue](https://github.com/mirpo/fastapi-gen/issues/new).

## Quick Overview

```console
pip3 install fastapi-gen
fastapi-gen my_app
cd my_app
make start-dev
```

or 

```console
pipx run fastapi-gen my_app
cd my_app
make start-dev
```

If you've previously installed `fastapi-gen` globally via `pip3 install fastapi-gen`, we recommend you reinstall the package using `pip3 install --upgrade --force-reinstall fastapi-gen` or `pipx upgrade fastapi-gen` to ensure that you use the latest version.

Then open http://localhost:8000/docs to see your app OpenAPI documentation.

## Available Templates

### 📚 **Hello World** (Default) - Complete FastAPI Learning Template
- ✅ **REST API fundamentals** - GET/POST/PUT operations with proper validation
- ✅ **Configuration management** - Both `pydantic-settings` and `dotenv` examples
- ✅ **Dependency injection** - Clean architecture patterns with `Depends()`
- ✅ **Background tasks** - Asynchronous processing with logging
- ✅ **Custom exception handling** - Professional error responses
- ✅ **Input validation** - Advanced Pydantic Field constraints
- ✅ **Health monitoring** - Built-in health check endpoint
- ✅ **Comprehensive tests** - Complete test coverage for all features

*Perfect for learning FastAPI or starting new projects* • [View Template Features →](src/templates/hello_world/README.md)

### 🚀 **Advanced** - Production-Ready Template
Complete template with enterprise-grade features and patterns:
- ✅ **JWT Authentication** - User registration, login, and protected routes
- ✅ **Database Integration** - SQLAlchemy 2.0 with async support (SQLite/PostgreSQL)
- ✅ **Rate Limiting** - DDoS protection with configurable limits per endpoint
- ✅ **Caching System** - In-memory caching with Redis integration ready
- ✅ **WebSocket Support** - Real-time communication and messaging
- ✅ **File Upload** - Secure file handling with validation and cloud storage ready
- ✅ **Enhanced Security** - CORS, input validation, and production-ready patterns
- ✅ **Comprehensive Tests** - Authentication, CRUD, WebSocket, and integration tests

*Perfect for production applications requiring advanced features* • [View Template Features →](src/templates/advanced/README.md)

### 🤖 **NLP** - Natural Language Processing
Natural language processing template with examples for local Hugging Face models:
- Text summarization, named-entity recognition, and LLM text generation
- Production-ready model serving patterns

### 🔗 **Langchain** - Production-Ready LLM Integration  
Modern LangChain template with enterprise-grade features:
- ✅ **Optimized Model Loading** - Startup caching and efficient memory management
- ✅ **Modern LangChain Patterns** - Updated imports and best practices
- ✅ **Flexible API Design** - Both REST and request body endpoints with Pydantic models
- ✅ **Smart Configuration** - Auto device detection (CPU/GPU) and configurable parameters
- ✅ **Production Monitoring** - Health checks, logging, and error handling
- ✅ **Real Service Testing** - Comprehensive tests using actual model inference
- ✅ **Text Generation & QA** - Dual endpoints for different LLM use cases
- ✅ **Backward Compatibility** - Maintains existing GET endpoints while adding modern POST APIs

### 🦙 **Llama** - Local Llama Models
Template using llama.cpp and llama-cpp-python:
- Local Llama 2 model integration for question answering
- Optimized for performance and memory usage

*Important notes*:
- Langchain template requires hardware to run and will automatically download required models, be patient.
- Llama template will download around 4GB model from Hugginface and >4GB of RAM.

Each template includes not only code, but also **tests**.

### Get Started Immediately

You **don’t** need to install or configure dependencies like FastAPI, Pydantic, or Pytest.<br>
They are preconfigured and hidden so that you can focus on the code.

Create a project, and you’re good to go.

**What you get out of the box:**
- 🔧 **Zero configuration** - Ready-to-run development environment
- 📝 **Production patterns** - Industry-standard project structure  
- 🧪 **Testing setup** - Comprehensive test suites with examples
- 🔍 **Code quality** - Linting and formatting with Ruff
- 📚 **Documentation** - Auto-generated OpenAPI docs
- 🐳 **Deployment ready** - Makefile with common commands

## Creating an App

**You’ll need to have Python 3.12+ or later version on your local development machine**. We recommend using the latest LTS version. You can use [pyenv](https://github.com/pyenv/pyenv) (macOS/Linux) to switch Python versions between different projects.

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
