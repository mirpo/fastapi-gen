<div align="center">

# 📚 Hello World - FastAPI Learning Template

**Perfect for learning FastAPI fundamentals and starting new projects**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-purple.svg)](https://pydantic.dev)

</div>

---

## 🎯 What You'll Build

A **complete learning-focused FastAPI application** with all essential patterns:

🌐 **Real REST API** → CRUD operations with proper validation  
⚙️ **Smart Configuration** → Environment management done right  
🔄 **Clean Architecture** → Dependency injection patterns  
📋 **Async Processing** → Background tasks with logging  
🛡️ **Error Handling** → Professional error responses  
💊 **Health Monitoring** → Production-ready health checks

## ⚡ Quick Start in 30 Seconds

```bash
# You're already here! Just run:
make start

# Or manually:
uvicorn main:app --reload
```

🚀 **Open:** [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

## ✨ Features Included

<details>
<summary><strong>🌐 REST API Fundamentals</strong></summary>

**Complete CRUD operations with modern validation:**
- ✅ **GET** endpoints with path and query parameters
- ✅ **POST** endpoints with request body validation
- ✅ **PUT** endpoints for updates
- ✅ **Advanced validation** with Pydantic Field constraints

</details>

<details>
<summary><strong>⚙️ Configuration Management</strong></summary>

**Two approaches to environment configuration:**
- ✅ **`dotenv`** - Simple environment variable loading from `.env` files
- ✅ **`pydantic-settings`** - Type-safe configuration with Pydantic
- ✅ **Dependency injection** - Clean configuration management with `Depends()`

</details>

<details>
<summary><strong>🔄 Advanced FastAPI Patterns</strong></summary>

**Production-ready patterns and practices:**
- ✅ **Background tasks** - Asynchronous task processing with logging
- ✅ **Custom exception handlers** - Professional error responses with proper HTTP status codes
- ✅ **Health check endpoint** - `/health` with timestamp for monitoring
- ✅ **Dependency injection** - Clean architecture patterns

</details>

<details>
<summary><strong>🧪 Complete Testing Suite</strong></summary>

**100% test coverage for all features:**
- ✅ **Endpoint testing** - All REST operations tested
- ✅ **Validation testing** - Error cases and edge conditions
- ✅ **Configuration testing** - Environment and dependency injection
- ✅ **Background task testing** - Async operation validation

</details>

## 📡 API Endpoints

### Core Endpoints
```http
GET  /                    # Hello world response
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

## 🛠️ Development Commands

<details>
<summary><strong>Available Make Commands</strong></summary>

| Command | Description |
|---------|-------------|
| `make start` | 🚀 Run app in development mode with auto-reload |
| `make test` | 🧪 Run comprehensive test suite |
| `make lint` | 🔍 Run code quality checks with Ruff |

</details>

## 🎓 Learning Guide

### 1. **Start with Configuration** 📖
Explore how environment variables work:
- Check out `/config` endpoint for dependency injection
- Compare `/version-pydantic-settings` vs `/version-dotenv`
- Look at `main.py` to see both approaches

### 2. **Master CRUD Operations** 🔧
Practice REST API fundamentals:
- Create items via `POST /items/`
- Retrieve with `GET /items/{id}?q=optional`
- Update with `PUT /items/{id}`

### 3. **Understand Async Patterns** ⚡
Learn background processing:
- Try `POST /send-notification/` 
- Watch the logs for async task execution
- Study the background task implementation

### 4. **Explore Error Handling** 🛡️
See professional error responses:
- Visit `/error-example` endpoint
- Check how custom exceptions work
- Review the exception handler implementation

### 5. **Run the Tests** 🧪
See comprehensive testing in action:
```bash
make test
# Study the test files to learn testing patterns
```

## 📁 Project Structure

```
hello_world/
├── main.py              # Main FastAPI application
├── tests/
│   ├── test_main.py     # Comprehensive test suite
│   └── __init__.py
├── requirements.txt     # Dependencies
├── Makefile            # Development commands
└── README.md           # This file
```

## 🚀 Next Steps

### Ready to Level Up?

1. **🔨 Customize the API** - Add your own endpoints and models
2. **📊 Add a Database** - Try the [Advanced template](../advanced/README.md) for SQLAlchemy integration
3. **🤖 Add AI Features** - Explore [NLP](../nlp/README.md), [LangChain](../langchain/README.md), or [Llama](../llama/README.md) templates
4. **🚀 Deploy to Production** - Use the patterns learned here in real applications

### Learn More FastAPI
- 📚 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🎓 [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- 💡 [Pydantic Documentation](https://pydantic.dev/)

---

<div align="center">

**Perfect for learning FastAPI or starting new projects** 💯

*Ready for production features? Check out the [🚀 Advanced template](../advanced/README.md)*

</div>