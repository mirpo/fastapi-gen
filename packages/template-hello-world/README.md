<div align="center">

# Hello World - FastAPI Learning Template

**Perfect for learning FastAPI fundamentals and starting new projects**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)

</div>

---

## What You'll Build

A complete learning-focused FastAPI application with essential patterns: REST API with CRUD operations, smart configuration management, clean architecture with dependency injection, async processing with background tasks, professional error handling, and health monitoring.

## Quick Start

```bash
# You're already here! Just run:
make start

# Or manually:
uvicorn hello_world.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

## Features

**REST API Fundamentals**
- GET, POST, PUT endpoints with proper validation
- Path parameters, query parameters, and request bodies
- Advanced validation with Pydantic Field constraints

**Configuration Management**
- `dotenv` for simple environment variable loading
- `pydantic-settings` for type-safe configuration
- Dependency injection patterns with `Depends()`

**Production Patterns**
- Background tasks for asynchronous processing
- Custom exception handlers with proper HTTP status codes
- Health check endpoint at `/health`
- Structured logging

**Complete Testing**
- 100% test coverage for all features
- Endpoint and validation testing
- Configuration and background task testing

## API Endpoints

### Core
```http
GET  /                    # Hello world
GET  /health              # Health check with timestamp
```

### Configuration Examples
```http
GET  /version-pydantic-settings  # Pydantic Settings demo
GET  /version-dotenv             # Python-dotenv demo
GET  /config                     # Dependency injection demo
```

### CRUD Operations
```http
POST /items/              # Create item with validation
GET  /items/{item_id}     # Read item with query params
PUT  /items/{item_id}     # Update item
```

### Advanced Features
```http
GET  /error-example       # Custom exception handling
POST /send-notification/  # Background task example
```

## Development Commands

| Command      | Description                                  |
| ------------ | -------------------------------------------- |
| `make start` | Run app in development mode with auto-reload |
| `make test`  | Run comprehensive test suite                 |
| `make lint`  | Run code quality checks with Ruff            |

## Project Structure

```
hello_world/
├── src/
│   └── hello_world/
│       ├── __init__.py
│       └── main.py      # Main FastAPI application
├── tests/
│   ├── test_main.py     # Comprehensive test suite
│   └── __init__.py
├── pyproject.toml       # Project configuration (uv)
├── .env_dev             # Environment variables
├── Makefile             # Development commands
├── .gitignore
└── README.md            # This file
```
