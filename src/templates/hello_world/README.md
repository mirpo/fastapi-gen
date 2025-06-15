# Getting Started with FastApi Gen

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen).

## Features

This template includes examples of:
1. **Environment Configuration**: `dotenv` and `pydantic-settings`
2. **HTTP Methods**: GET / POST / PUT with proper status codes
3. **Data Validation**: Pydantic models with Field constraints
4. **CORS Support**: Cross-origin request handling
5. **Logging**: Structured logging with application lifecycle
6. **Health Check**: `/health` endpoint for monitoring
7. **Error Handling**: Custom exception handlers
8. **API Documentation**: OpenAPI with organized tags
9. **Testing**: Comprehensive test suite with edge cases

## API Endpoints

- `GET /` - Hello World message
- `GET /health` - Health check endpoint
- `GET /version-pydantic-settings` - Environment variables via pydantic-settings
- `GET /version-dotenv` - Environment variables via dotenv
- `POST /items/` - Create item with validation
- `PUT /items/{item_id}` - Update item by ID
- `GET /items/{item_id}` - Read item by ID with optional query parameter

## Available Scripts

In the project directory, you can run:

### `make init`

Sets up the project by creating a virtual environment and installing dependencies from requirements.txt.
Also initializes git repository if not already present.

### `make start`

Runs the app in development mode on http://127.0.0.1:8000.
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`

Runs the test suite using pytest with verbose output.

### `make lint`

Runs code linting using ruff to check code quality and style.
