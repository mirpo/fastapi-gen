# Getting Started with FastApi Gen

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen).

## Features Included

This template demonstrates various FastAPI features and best practices:

### Configuration Management
1. **`dotenv`** - Environment variable loading from .env files
2. **`pydantic-settings`** - Type-safe configuration with Pydantic
3. **Dependency injection** - Clean configuration management with `Depends()`

### HTTP Operations
4. **GET / POST / PUT** - Complete CRUD operations
5. **Path and query parameters** - URL parameter handling
6. **Request/response models** - Type-safe JSON handling

### Advanced Features
7. **Health check endpoint** - `/health` with timestamp for monitoring
8. **Background tasks** - Asynchronous task processing with logging
9. **Custom exception handlers** - Custom error responses with proper HTTP status codes
10. **Input validation** - Advanced Pydantic Field validation with constraints

### API Endpoints

- `GET /` - Basic hello world response
- `GET /health` - Health check with timestamp
- `GET /version-pydantic-settings` - Configuration via pydantic-settings
- `GET /version-dotenv` - Configuration via dotenv
- `GET /config` - Dependency injection example
- `GET /error-example` - Custom exception handling demo
- `POST /items/` - Create item with validation
- `PUT /items/{item_id}` - Update item
- `GET /items/{item_id}` - Read item with optional query params
- `POST /send-notification/` - Background task example

## Available Scripts

In the project directory, you can run:

### `make start`

Runs the app in development mode.<br>
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`

Runs tests with comprehensive coverage for all endpoints and features.

### `make lint`

Runs code linting with ruff to ensure code quality.
