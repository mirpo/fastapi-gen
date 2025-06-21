# Advanced FastAPI Template

This project was bootstrapped with [FastApi Gen](https://github.com/mirpo/fastapi-gen).

## Features Included

This advanced template demonstrates comprehensive FastAPI features and production-ready patterns:

### Core Features (from hello_world)
1. **Configuration Management**
   - `dotenv` - Environment variable loading from .env files
   - `pydantic-settings` - Type-safe configuration with Pydantic
   - Dependency injection - Clean configuration management with `Depends()`

2. **HTTP Operations**
   - GET / POST / PUT - Complete CRUD operations
   - Path and query parameters - URL parameter handling
   - Request/response models - Type-safe JSON handling

3. **Basic Advanced Features**
   - Health check endpoint - `/health` with timestamp for monitoring
   - Background tasks - Asynchronous task processing with logging
   - Custom exception handlers - Custom error responses with proper HTTP status codes
   - Input validation - Advanced Pydantic Field validation with constraints

### Advanced Features (New)

#### 🔐 Authentication & Security
4. **JWT Authentication**
   - User registration and login endpoints
   - Password hashing with bcrypt
   - JWT token generation and validation
   - Protected routes with bearer token authentication

5. **Rate Limiting**
   - `slowapi` integration for DDoS protection
   - Different limits per endpoint (health: 10/min, login: 5/min)
   - Configurable rate limiting with Redis support ready

#### 🗄️ Database Integration
6. **SQLAlchemy 2.0 with Async Support**
   - SQLite database for development (PostgreSQL ready)
   - Async database operations
   - User and Product models with relationships
   - Automatic table creation on startup

7. **Database Models**
   - `User` model with authentication fields
   - `Product` model for CRUD operations
   - Extensible model structure with comments for scaling

#### ⚡ Performance & Caching
8. **In-Memory Caching**
   - Simple dictionary-based caching for development
   - Redis integration ready with detailed migration comments
   - Cache keys and TTL management
   - Product listing and detail caching

#### 🔄 Real-Time Features
9. **WebSocket Support**
   - Real-time communication endpoint
   - Connection management
   - Message broadcasting
   - Extensible for chat rooms and notifications

#### 📁 File Handling
10. **File Upload**
    - File type validation (images, text, PDF)
    - File size limits (5MB)
    - Secure file storage with timestamped names
    - Cloud storage ready (S3, GCS comments)

#### 🛠️ Production Ready Features
11. **CORS Configuration**
    - Cross-origin resource sharing setup
    - Production-ready with specific domain configuration

12. **Enhanced Health Checks**
    - Database connectivity testing
    - Cache system status
    - Comprehensive system health reporting

13. **Error Handling**
    - Comprehensive HTTP exception handling
    - Custom error responses
    - Validation error standardization

## API Endpoints

### Original Endpoints (hello_world)
- `GET /` - Basic hello world response
- `GET /health` - Enhanced health check with database and cache status
- `GET /version-pydantic-settings` - Configuration via pydantic-settings
- `GET /version-dotenv` - Configuration via dotenv
- `GET /config` - Dependency injection example
- `GET /error-example` - Custom exception handling demo
- `POST /items/` - Create item with validation
- `PUT /items/{item_id}` - Update item
- `GET /items/{item_id}` - Read item with optional query params
- `POST /send-notification/` - Background task example

### New Advanced Endpoints

#### Authentication
- `POST /auth/register` - User registration with validation
- `POST /auth/login` - User login with JWT token response
- `GET /auth/me` - Get current user profile (protected)

#### Products (CRUD with caching)
- `POST /products/` - Create product (protected, cached)
- `GET /products/` - List products with pagination (cached, rate limited)
- `GET /products/{product_id}` - Get product by ID (cached)

#### File Operations
- `POST /upload/` - File upload with validation (protected, rate limited)

#### Real-Time
- `WebSocket /ws` - WebSocket endpoint for real-time communication

## Extension Points

This template is designed for easy extension. Key areas with detailed comments:

### 🔄 Database Migration
- **PostgreSQL**: Replace SQLite with PostgreSQL for production
- **Migrations**: Add Alembic for database schema migrations
- **Relationships**: Extend models with foreign keys and relationships

### 🔐 Enhanced Authentication
- **Role-Based Access Control (RBAC)**: Add user roles and permissions
- **OAuth Integration**: Add GitHub, Google, Facebook login
- **Two-Factor Authentication**: Implement TOTP/SMS verification
- **Session Management**: Add session storage and invalidation

### ⚡ Caching & Performance
- **Redis Integration**: Replace in-memory cache with Redis
- **Distributed Caching**: Scale across multiple servers
- **Query Optimization**: Add database query caching
- **Response Compression**: Add gzip compression middleware

### 🔄 Real-Time Features
- **Chat Rooms**: Extend WebSocket for multi-room support
- **User Presence**: Track online/offline status
- **Message Persistence**: Store messages in database
- **Push Notifications**: Integrate with mobile push services

### 📁 File & Media
- **Cloud Storage**: Integrate with AWS S3, Google Cloud Storage
- **Image Processing**: Add resize, compression, format conversion
- **CDN Integration**: Serve files through CDN
- **File Metadata**: Store file information in database

### 🛠️ Production Features
- **Monitoring**: Add Prometheus metrics and Grafana dashboards
- **Logging**: Structured logging with correlation IDs
- **Tracing**: Distributed tracing with OpenTelemetry
- **Docker**: Containerization for easy deployment

## Available Scripts

In the project directory, you can run:

### `make start`
Runs the app in development mode.  
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`
Runs the comprehensive test suite covering:
- Authentication flows
- CRUD operations
- Rate limiting
- WebSocket functionality
- File uploads
- Error handling
- Integration tests

### `make lint`
Runs code linting with ruff to ensure code quality.

## Development Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create `.env_dev` file with:
   ```
   API_VERSION=1.0.0
   SECRET_KEY=your-secret-key-for-jwt
   ```

3. **Run the application:**
   ```bash
   make start
   # or
   uvicorn main:app --reload
   ```

4. **Run tests:**
   ```bash
   make test
   # or
   pytest
   ```

## Database

The template uses SQLite for development. The database file (`app.db`) will be created automatically when you first run the application.

For production, consider migrating to PostgreSQL by:
1. Updating `DATABASE_URL` in main.py
2. Installing PostgreSQL driver: `pip install asyncpg`
3. Setting up database migrations with Alembic

## Security Considerations

- Change `SECRET_KEY` in production
- Configure CORS for specific domains
- Use environment variables for sensitive data
- Set up proper rate limiting with Redis
- Implement API key authentication for service-to-service calls
- Add input sanitization for file uploads
- Use HTTPS in production

## Performance Optimization

- Replace in-memory cache with Redis
- Add database connection pooling
- Implement query optimization
- Add response compression
- Use CDN for static files
- Monitor with APM tools

This template provides a solid foundation for building production-ready FastAPI applications with room for extensive customization and scaling.