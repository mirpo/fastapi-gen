<div align="center">

# Advanced - Enterprise FastAPI Template

**Production-ready FastAPI with enterprise-grade features**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)](https://jwt.io)

</div>

---

## What You'll Build

A complete enterprise-grade FastAPI application with JWT authentication, database integration, rate limiting, caching, WebSocket support, and secure file upload handling.

## Quick Start

```bash
# You're already here! Just run:
make start

# Or manually:
uvicorn main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

## Enterprise Features

**JWT Authentication System**
- User registration with password hashing (bcrypt)
- Login with JWT token generation and validation
- Protected routes with Bearer token authentication
- Token management with expiration

**Database Integration**
- SQLAlchemy 2.0 with async support
- Auto migrations (tables created on startup)
- User and Product models ready to extend
- Proper connection and session management

**Rate Limiting & Security**
- Per-endpoint rate limits with slowapi
- DDoS protection
- CORS configuration
- Input validation and secure error responses

**Performance & Caching**
- In-memory caching for development
- Redis-ready integration
- Strategic cache keys for products and users
- TTL management and cache invalidation

**Real-Time Features**
- WebSocket connection management
- Message broadcasting
- Graceful error handling
- Extensible for chat rooms

**File Upload System**
- Type validation (images, PDFs, text)
- 5MB size limit
- Secure storage with timestamped filenames
- Cloud storage ready (S3/GCS comments included)

## API Endpoints

### Authentication
```http
POST /auth/register     # User registration
POST /auth/login        # User login (returns JWT)
GET  /auth/me           # Get current user (protected)
```

### Database Operations
```http
POST /products/         # Create product (protected, cached)
GET  /products/         # List products (cached, rate limited)
GET  /products/{id}     # Get product (cached)
```

### File Operations
```http
POST /upload/           # File upload (protected, rate limited)
```

### Real-Time
```http
WebSocket /ws           # WebSocket endpoint
```

### Core
```http
GET  /                  # Hello world
GET  /health            # Enhanced health check
```

## Development Commands

| Command      | Description                                  |
| ------------ | -------------------------------------------- |
| `make start` | Run app in development mode with auto-reload |
| `make test`  | Run comprehensive test suite                 |
| `make lint`  | Run code quality checks with Ruff            |

## Configuration

Create `.env_dev` file:
```bash
API_VERSION=1.0.0
SECRET_KEY=your-secret-key-for-jwt-tokens
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

For production with PostgreSQL:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
uv pip install asyncpg
```

## Testing

Run comprehensive test suite covering authentication, CRUD, rate limiting, WebSocket, and file upload:

```bash
make test
```

## Project Structure

```
advanced/
├── src/
│   └── advanced/
│       ├── __init__.py
│       └── main.py      # Main FastAPI app with all features
├── tests/
│   ├── test_main.py     # Comprehensive test suite
│   └── __init__.py
├── pyproject.toml       # Project configuration (uv)
├── Makefile            # Development commands
├── .gitignore
└── README.md           # This file

# Auto-generated at runtime:
├── uploads/             # File upload directory
└── app.db              # SQLite database
```
