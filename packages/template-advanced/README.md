<div align="center">

# Advanced - Enterprise FastAPI Template

**Production-ready FastAPI with enterprise-grade features**

*This project was bootstrapped with [FastAPI Gen](https://github.com/mirpo/fastapi-gen)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)](https://jwt.io)
[![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-blue.svg)](https://fastapi.tiangolo.com/advanced/websockets/)

</div>

---

## What You'll Build

A **complete enterprise-grade FastAPI application** ready for production:

**JWT Authentication** → Secure user registration & login  
**Database Integration** → SQLAlchemy 2.0 with async support  
**Rate Limiting** → DDoS protection per endpoint  
**Caching System** → Performance optimization ready  
**WebSocket Support** → Real-time communication  
**File Upload** → Secure file handling with validation  

## Quick Start in 30 Seconds

```bash
# You're already here! Just run:
make start

# Or manually:
uvicorn main:app --reload
```

**Open:** [http://localhost:8000/docs](http://localhost:8000/docs) to see your interactive API documentation.

## Enterprise Features

<details>
<summary><strong>JWT Authentication System</strong></summary>

**Complete authentication workflow:**
- ✅ **User Registration** - Secure user creation with password hashing
- ✅ **User Login** - JWT token generation and validation
- ✅ **Protected Routes** - Bearer token authentication
- ✅ **Password Security** - bcrypt hashing with salt
- ✅ **Token Management** - JWT creation, validation, and expiration

**Try it:**
1. Register: `POST /auth/register`
2. Login: `POST /auth/login` 
3. Access protected: `GET /auth/me` (with Bearer token)

</details>

<details>
<summary><strong>Database Integration</strong></summary>

**Modern async database patterns:**
- ✅ **SQLAlchemy 2.0** - Latest async ORM patterns
- ✅ **Auto Migrations** - Database tables created on startup
- ✅ **User & Product Models** - Ready-to-extend data models
- ✅ **Async Operations** - Non-blocking database calls
- ✅ **Connection Management** - Proper session handling

**Database Models:**
- `User` - Authentication and profile data
- `Product` - CRUD operations with caching

</details>

<details>
<summary><strong>Rate Limiting & Security</strong></summary>

**Production-ready security:**
- ✅ **Per-Endpoint Limits** - Different limits per route
- ✅ **DDoS Protection** - slowapi integration
- ✅ **CORS Configuration** - Cross-origin request handling
- ✅ **Input Validation** - Comprehensive request validation
- ✅ **Error Handling** - Secure error responses

**Rate Limits:**
- Health check: 10 requests/minute
- Authentication: 5 requests/minute
- File upload: 3 requests/minute

</details>

<details>
<summary><strong>Performance & Caching</strong></summary>

**Optimized for speed:**
- ✅ **In-Memory Caching** - Fast development caching
- ✅ **Redis Ready** - Easy Redis integration
- ✅ **Cache Keys** - Strategic caching for products
- ✅ **TTL Management** - Time-based cache expiration
- ✅ **Cache Invalidation** - Smart cache clearing

**Cached Endpoints:**
- Product listings and details
- User profile data
- Health check responses

</details>

<details>
<summary><strong>Real-Time Features</strong></summary>

**WebSocket communication:**
- ✅ **Connection Management** - Handle multiple clients
- ✅ **Message Broadcasting** - Real-time updates
- ✅ **Error Handling** - Graceful connection failures
- ✅ **Extensible Design** - Ready for chat rooms

**Try WebSocket:**
- Connect to: `ws://localhost:8000/ws`
- Send messages for real-time echo

</details>

<details>
<summary><strong>File Upload System</strong></summary>

**Secure file handling:**
- ✅ **Type Validation** - Images, PDFs, text files
- ✅ **Size Limits** - 5MB maximum file size
- ✅ **Secure Storage** - Timestamped filenames
- ✅ **Cloud Ready** - S3/GCS integration comments
- ✅ **Error Handling** - Invalid file rejection

**Supported Files:**
- Images: PNG, JPG, JPEG, GIF
- Documents: PDF, TXT
- Size limit: 5MB

</details>

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

### Core Features
```http
GET  /                  # Hello world
GET  /health            # Enhanced health check
```

### Learning Examples (from Hello World)
```http
GET  /version-pydantic-settings  # Configuration examples
GET  /config                     # Dependency injection
POST /send-notification/         # Background tasks
```

## Development Commands

<details>
<summary><strong>Available Make Commands</strong></summary>

| Command | Description |
|---------|-------------|
| `make start` | Run app in development mode with auto-reload |
| `make test` | Run comprehensive test suite |
| `make lint` | Run code quality checks with Ruff |

</details>

## Configuration

### Environment Variables

Create `.env_dev` file:
```bash
API_VERSION=1.0.0
SECRET_KEY=your-secret-key-for-jwt-tokens
DATABASE_URL=sqlite+aiosqlite:///./app.db
```

### Database Setup

The app automatically creates SQLite database on startup. For production:

```bash
# PostgreSQL example
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
pip install asyncpg
```

## Testing Strategy

**Comprehensive test coverage:**
- ✅ **Authentication Tests** - Registration, login, protected routes
- ✅ **CRUD Tests** - Database operations and validation
- ✅ **Rate Limiting Tests** - Endpoint protection validation
- ✅ **WebSocket Tests** - Real-time communication
- ✅ **File Upload Tests** - Validation and security
- ✅ **Integration Tests** - End-to-end workflows

```bash
make test
# See detailed test results with coverage
```

## Project Structure

```
advanced/
├── main.py              # Main FastAPI app with all features
├── tests/
│   ├── test_main.py     # Comprehensive test suite
│   └── __init__.py
├── uploads/             # File upload directory
├── app.db              # SQLite database (auto-created)
├── requirements.txt     # Dependencies
├── Makefile            # Development commands
└── README.md           # This file
```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` to cryptographically secure value
- [ ] Configure CORS for specific domains only
- [ ] Set up Redis for distributed caching
- [ ] Use PostgreSQL for production database
- [ ] Enable HTTPS in production
- [ ] Set up proper rate limiting with Redis backend
- [ ] Configure file upload limits based on infrastructure

### Performance Optimization

- [ ] Replace in-memory cache with Redis
- [ ] Add database connection pooling
- [ ] Implement query optimization
- [ ] Add response compression middleware
- [ ] Use CDN for file uploads
- [ ] Set up monitoring with APM tools

### Infrastructure

- [ ] Set up Docker containers
- [ ] Configure load balancing
- [ ] Add database migrations with Alembic
- [ ] Set up CI/CD pipelines
- [ ] Configure monitoring and logging
- [ ] Implement backup strategies

## Learning Path

### Mastering Enterprise Features

1. **Authentication Flow**
   - Register a new user via API
   - Login and copy the JWT token
   - Use Bearer token to access `/auth/me`
   - Explore the JWT token structure

2. **Database Operations**
   - Create products via `POST /products/`
   - Notice caching behavior on repeated requests
   - Explore SQLAlchemy models in `main.py`

3. **Rate Limiting**
   - Make rapid requests to test limits
   - See how different endpoints have different limits
   - Check error responses for rate limit violations

4. **Real-Time Communication**
   - Connect to WebSocket endpoint
   - Send messages and see real-time responses
   - Test multiple client connections

5. **File Uploads**
   - Upload different file types
   - Test file size limits
   - Explore secure file storage patterns

## Extension Points

<details>
<summary><strong>Enhanced Authentication</strong></summary>

**Ready for:**
- Role-based access control (RBAC)
- OAuth integration (GitHub, Google, Facebook)
- Two-factor authentication (TOTP/SMS)
- Session management and invalidation

</details>

<details>
<summary><strong>Database Scaling</strong></summary>

**Ready for:**
- PostgreSQL migration
- Alembic database migrations  
- Model relationships and foreign keys
- Query optimization and indexing

</details>

<details>
<summary><strong>Performance Scaling</strong></summary>

**Ready for:**
- Redis distributed caching
- Database connection pooling
- Response compression
- CDN integration for files

</details>

<details>
<summary><strong>Real-Time Scaling</strong></summary>

**Ready for:**
- Multi-room chat systems
- User presence tracking
- Message persistence
- Push notification integration

</details>

## Next Steps

### Ready for AI Integration?

- **Add NLP Features** - Try the [NLP template](../nlp/README.md) for text processing
- **LLM Integration** - Explore [LangChain template](../langchain/README.md) for AI workflows  
- **Local LLM** - Check out [Llama template](../llama/README.md) for local inference

### Learn More Enterprise Patterns
- [FastAPI Advanced User Guide](https://fastapi.tiangolo.com/advanced/)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)

---

<div align="center">

**Production-ready FastAPI with enterprise features**

*Need simpler setup? Try the [Hello World template](../hello_world/README.md)*

</div>